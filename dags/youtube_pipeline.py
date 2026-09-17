import sys
from datetime import datetime

sys.path.insert(0, "/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from src.ingestion.youtube_api import extract_youtube_data
from src.database.staging_storage import load_raw_data_to_staging
from src.transformation.transform_channels import transform_channels
from src.transformation.transform_videos import transform_videos
from src.database.core_storage import (
    save_channels_to_core,
    save_videos_to_core,
    get_channel_id,
)


def transform_and_load_channels():
    df = transform_channels()
    save_channels_to_core(df)


def transform_and_load_videos():
    df = transform_videos()
    channel_id = get_channel_id()
    save_videos_to_core(df, channel_id)


default_args = {
    "owner": "youtube-pipeline",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "email_on_failure": False,
    "email_on_retry": False,
}
with DAG(
    dag_id="youtube_data_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="0 2 * * *",
    catchup=False,
    tags=["youtube", "data-pipeline"],
) as dag:

    extract_youtube = PythonOperator(
        task_id="extract_youtube",
        python_callable=extract_youtube_data,
    )

    load_staging = PythonOperator(
        task_id="load_staging",
        python_callable=load_raw_data_to_staging,
    )

    transform_load_channels = PythonOperator(
        task_id="transform_load_channels",
        python_callable=transform_and_load_channels,
    )

    transform_load_videos = PythonOperator(
        task_id="transform_load_videos",
        python_callable=transform_and_load_videos,
    )

    extract_youtube >> load_staging

    load_staging >> [
        transform_load_channels,
        transform_load_videos,
    ]
    
print("miloud")