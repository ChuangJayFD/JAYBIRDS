/**
 * fetch_analytics.js
 * GitHub Actions上で実行。GA4 Data APIからデータを取得し
 * analytics_data.json に書き出す。認証情報はすべて環境変数から取得。
 */

const { BetaAnalyticsDataClient } = require('@google-analytics/data');
const fs = require('fs');

const KEY_JSON = process.env.GA4_SERVICE_ACCOUNT_KEY;
const PROP_ID  = process.env.GA4_PROPERTY_ID;

if (!KEY_JSON || !PROP_ID) {
  console.error('Missing required env vars: GA4_SERVICE_ACCOUNT_KEY, GA4_PROPERTY_ID');
  process.exit(1);
}

const credentials = JSON.parse(KEY_JSON);
const property    = `properties/${PROP_ID}`;
const client      = new BetaAnalyticsDataClient({ credentials });

/** ディメンションなしの集計レポート。複数 dateRange を一括取得し dateRange ディメンションで分離する */
async function summaryReport(metrics, dateRanges) {
  const [res] = await client.runReport({
    property,
    metrics:    metrics.map(n => ({ name: n })),
    dateRanges,
    dimensions: [{ name: 'dateRange' }],
  });
  return res;
}

/** ディメンションあり汎用レポート */
async function dimReport({ dimensions, metrics, dateRange, orderBys, limit }) {
  const [res] = await client.runReport({
    property,
    dimensions: dimensions.map(n => ({ name: n })),
    metrics:    metrics.map(n => ({ name: n })),
    dateRanges: [dateRange],
    ...(orderBys ? { orderBys } : {}),
    ...(limit    ? { limit }    : {}),
  });
  return res;
}

function toRows(res) {
  if (!res || !res.rows) return [];
  return res.rows.map(row => ({
    d: (row.dimensionValues || []).map(v => v.value),
    m: (row.metricValues   || []).map(v => Number(v.value)),
  }));
}

function extractSummary(rows, dateRangeLabel) {
  const row = rows.find(r => r.d[0] === dateRangeLabel);
  if (!row) return { sessions: 0, users: 0, pageviews: 0 };
  return {
    sessions:  row.m[0],
    users:     row.m[1],
    pageviews: row.m[2],
  };
}

async function main() {
  const METRICS_SUMMARY = ['sessions', 'totalUsers', 'screenPageViews'];
  const DATE_7D  = { startDate: '7daysAgo',  endDate: 'today' };
  const DATE_30D = { startDate: '30daysAgo', endDate: 'today' };

  // ===== 週次・月次サマリーを1回のAPIコールで取得（dateRange ディメンションで分離） =====
  // GA4は複数 dateRange を指定すると date_range_0, date_range_1 として結果を返す
  console.log('Fetching weekly/monthly summary...');
  const summaryRes = await summaryReport(METRICS_SUMMARY, [DATE_7D, DATE_30D]);
  const summaryRows = toRows(summaryRes);
  console.log('Summary rows:', JSON.stringify(summaryRows));

  const weekly  = extractSummary(summaryRows, 'date_range_0');
  const monthly = extractSummary(summaryRows, 'date_range_1');
  console.log('Weekly (7d):', weekly);
  console.log('Monthly (30d):', monthly);

  // ===== 日別トレンド（30日間） =====
  console.log('Fetching daily trend...');
  const dailyRes = await dimReport({
    dimensions: ['date'],
    metrics:    ['sessions', 'totalUsers'],
    dateRange:  DATE_30D,
    orderBys:   [{ dimension: { dimensionName: 'date' }, desc: false }],
    limit:      31,
  });

  // ===== 国・地域 TOP10 =====
  console.log('Fetching countries...');
  const countriesRes = await dimReport({
    dimensions: ['country'],
    metrics:    ['sessions'],
    dateRange:  DATE_30D,
    orderBys:   [{ metric: { metricName: 'sessions' }, desc: true }],
    limit:      10,
  });

  // ===== 人気ページ TOP10 =====
  console.log('Fetching pages...');
  const pagesRes = await dimReport({
    dimensions: ['pageTitle', 'pagePath'],
    metrics:    ['screenPageViews'],
    dateRange:  DATE_30D,
    orderBys:   [{ metric: { metricName: 'screenPageViews' }, desc: true }],
    limit:      10,
  });

  // ===== 新規 / リピーター =====
  console.log('Fetching user type...');
  const userTypeRes = await dimReport({
    dimensions: ['newVsReturning'],
    metrics:    ['sessions'],
    dateRange:  DATE_30D,
  });

  const data = {
    updated:   new Date().toISOString(),
    weekly,
    monthly,
    daily:     toRows(dailyRes),
    countries: toRows(countriesRes),
    pages:     toRows(pagesRes),
    userType:  toRows(userTypeRes),
  };

  fs.writeFileSync('analytics_data.json', JSON.stringify(data, null, 2), 'utf8');
  console.log('Saved analytics_data.json successfully.');
}

main().catch(err => { console.error(err); process.exit(1); });
