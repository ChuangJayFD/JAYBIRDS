/**
 * fetch_analytics.js
 * GitHub Actions上で実行。GA4 Data APIからデータを取得し
 * analytics_data.json に書き出す。認証情報はすべて環境変数から取得。
 */

const { BetaAnalyticsDataClient } = require('@google-analytics/data');
const fs = require('fs');

const KEY_JSON  = process.env.GA4_SERVICE_ACCOUNT_KEY;
const PROP_ID   = process.env.GA4_PROPERTY_ID;

if (!KEY_JSON || !PROP_ID) {
  console.error('Missing required env vars: GA4_SERVICE_ACCOUNT_KEY, GA4_PROPERTY_ID');
  process.exit(1);
}

const credentials = JSON.parse(KEY_JSON);
const property    = `properties/${PROP_ID}`;
const client      = new BetaAnalyticsDataClient({ credentials });

async function report({ dimensions = [], metrics, dateRanges, orderBys, limit }) {
  const [res] = await client.runReport({
    property,
    dimensions: dimensions.map(n => ({ name: n })),
    metrics:    metrics.map(n => ({ name: n })),
    dateRanges,
    ...(orderBys ? { orderBys } : {}),
    ...(limit    ? { limit }    : {}),
  });
  return res;
}

function toRows(res) {
  if (!res.rows) return [];
  return res.rows.map(row => ({
    d: (row.dimensionValues || []).map(v => v.value),
    m: (row.metricValues   || []).map(v => Number(v.value)),
  }));
}

function toSummary(res) {
  if (!res.rows || !res.rows[0]) return { sessions: 0, users: 0, pageviews: 0 };
  const v = res.rows[0].metricValues;
  return {
    sessions:  Number(v[0].value),
    users:     Number(v[1].value),
    pageviews: Number(v[2].value),
  };
}

async function main() {
  const METRICS_SUMMARY = ['sessions', 'totalUsers', 'screenPageViews'];
  const DESC_SESSIONS   = [{ metric: { metricName: 'sessions' },        desc: true  }];
  const DESC_PV         = [{ metric: { metricName: 'screenPageViews' }, desc: true  }];
  const ASC_DATE        = [{ dimension: { dimensionName: 'date' },      desc: false }];

  const [weekly, monthly, daily, countries, pages, userType] = await Promise.all([
    report({ metrics: METRICS_SUMMARY, dateRanges: [{ startDate: '7daysAgo',  endDate: 'today' }] }),
    report({ metrics: METRICS_SUMMARY, dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }] }),
    report({
      dimensions: ['date'],
      metrics:    ['sessions', 'totalUsers'],
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      orderBys:   ASC_DATE,
    }),
    report({
      dimensions: ['country'],
      metrics:    ['sessions'],
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      orderBys:   DESC_SESSIONS,
      limit:      10,
    }),
    report({
      dimensions: ['pageTitle', 'pagePath'],
      metrics:    ['screenPageViews'],
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
      orderBys:   DESC_PV,
      limit:      10,
    }),
    report({
      dimensions: ['newVsReturning'],
      metrics:    ['sessions'],
      dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }],
    }),
  ]);

  const data = {
    updated:   new Date().toISOString(),
    weekly:    toSummary(weekly),
    monthly:   toSummary(monthly),
    daily:     toRows(daily),
    countries: toRows(countries),
    pages:     toRows(pages),
    userType:  toRows(userType),
  };

  fs.writeFileSync('analytics_data.json', JSON.stringify(data, null, 2), 'utf8');
  console.log('Saved analytics_data.json');
  console.log('Weekly:', data.weekly);
  console.log('Monthly:', data.monthly);
}

main().catch(err => { console.error(err); process.exit(1); });
