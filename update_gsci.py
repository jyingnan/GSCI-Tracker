import os
import json
import pandas as pd
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2 import service_account

# 1. Authentication via GitHub Secrets
try:
    # 假设环境变量中存储了 JSON 密钥字符串
    key_json = json.loads(os.environ.get('GCP_SERVICE_ACCOUNT_KEY'))
    credentials = service_account.Credentials.from_service_account_info(key_json)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
except Exception as e:
    print(f"Authentication Error: {e}")
    exit(1)

# 2. Define Date Range
# 设定起始日期
start_date = '20150301' 
# 获取昨天的日期 (YYYYMMDD)，确保数据完整性
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

print(f"Fetching data from {start_date} to {yesterday} (Yesterday)...")

# 3. SQL Query (GSCI Methodology)
# 增加 total_sources 栏位，并限制日期到昨天
query = f"""
WITH daily_raw AS (
  SELECT 
    SQLDATE,
    SUM(NumSources) AS total_sources,
    SUM(IF(GoldsteinScale < 0, ABS(GoldsteinScale) * NumSources, 0)) AS gsci_numerator
  FROM `gdelt-bq.gdeltv2.events`
  WHERE SQLDATE >= {start_date} AND SQLDATE <= {yesterday}
  GROUP BY SQLDATE
)
SELECT 
  FORMAT_DATE('%Y-%m-%d', CAST(PARSE_DATE('%Y%m%d', CAST(SQLDATE AS STRING)) AS DATE)) AS date,
  total_sources,
  SAFE_DIVIDE(gsci_numerator, total_sources) AS gsci
FROM daily_raw
ORDER BY date ASC
"""

# 4. Execution and Saving (Overwrite Mode)
csv_file = 'gsci_data.csv'

print("Querying BigQuery... This may take a moment.")
try:
    df_new = client.query(query).to_dataframe()

    if not df_new.empty:
        # 直接储存为 CSV，不读取旧档，实现完全覆盖
        # 格式化日期确保输出美观
        df_new.to_csv(csv_file, index=False)
        print(f"Update successful. File '{csv_file}' has been overwritten.")
        print(f"Total rows saved: {len(df_new)}")
        print(f"Latest data point: {df_new['date'].max()}")
    else:
        print("No data found for the specified range.")

except Exception as e:
    print(f"An error occurred during query or saving: {e}")
