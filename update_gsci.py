import os
import json
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# 1. 认证
key_json = json.loads(os.environ.get('GCP_SERVICE_ACCOUNT_KEY'))
credentials = service_account.Credentials.from_service_account_info(key_json)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# 2. 查询最近 7 天的数据
query = """
SELECT 
    FORMAT_DATE('%Y-%m-%d', CAST(PARSE_DATE('%Y%m%d', CAST(SQLDATE AS STRING)) AS DATE)) as date,
    SUM(ABS(GoldsteinScale) * NumSources) / AVG(TotalDailyEvents) as gsci
FROM (
    SELECT SQLDATE, GoldsteinScale, NumSources,
    COUNT(*) OVER(PARTITION BY SQLDATE) as TotalDailyEvents
    FROM `gdelt-intl.full.events`
    WHERE _PARTITIONTIME >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
    AND GoldsteinScale < 0
)
GROUP BY date ORDER BY date
"""

df_new = client.query(query).to_dataframe()

# 3. 合并旧数据并保存
try:
    df_old = pd.read_csv('gsci_data.csv')
    df_final = pd.concat([df_old, df_new]).drop_duplicates(subset=['date']).sort_values('date')
except:
    df_final = df_new

df_final.to_csv('gsci_data.csv', index=False)
