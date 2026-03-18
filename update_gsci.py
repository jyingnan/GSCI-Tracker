import os
import json
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# 1. Authentication via GitHub Secrets
try:
    key_json = json.loads(os.environ.get('GCP_SERVICE_ACCOUNT_KEY'))
    credentials = service_account.Credentials.from_service_account_info(key_json)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
except Exception as e:
    print(f"Authentication Error: {e}")
    exit(1)

# 2. Determine Update Range
csv_file = 'gsci_data.csv'
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 10:
    df_old = pd.read_csv(csv_file)
    df_old['date'] = pd.to_datetime(df_old['date'])
    last_date = df_old['date'].max().strftime('%Y%m%d')
    print(f"Existing data found. Updating from {last_date}...")
else:
    df_old = pd.DataFrame()
    last_date = '20150301' 
    print("No existing data. Performing full historical fetch...")

# 3. SQL Query (GSCI Methodology)
# GSCI = (Sum of |Goldstein| * NumSources) / Total_Daily_Sources
query = f"""
WITH daily_raw AS (
  SELECT 
    SQLDATE,
    SUM(NumSources) AS total_sources,
    SUM(IF(GoldsteinScale < 0, ABS(GoldsteinScale) * NumSources, 0)) AS gsci_numerator
  FROM `gdelt-bq.gdeltv2.events`
  WHERE SQLDATE >= {last_date}
  GROUP BY SQLDATE
)
SELECT 
  FORMAT_DATE('%Y-%m-%d', CAST(PARSE_DATE('%Y%m%d', CAST(SQLDATE AS STRING)) AS DATE)) AS date,
  SAFE_DIVIDE(gsci_numerator, total_sources) AS gsci
FROM daily_raw
ORDER BY date ASC
"""

# 4. Execution and Merging
print("Querying BigQuery...")
df_new = client.query(query).to_dataframe()

if not df_new.empty:
    df_new['date'] = pd.to_datetime(df_new['date'])
    if not df_old.empty:
        df_final = pd.concat([df_old, df_new]).drop_duplicates(subset=['date']).sort_values('date')
    else:
        df_final = df_new
    
    df_final['date'] = df_final['date'].dt.strftime('%Y-%m-%d')
    df_final.to_csv(csv_file, index=False)
    print(f"Update successful. Added {len(df_new)} new observations.")
else:
    print("No new data found.")
