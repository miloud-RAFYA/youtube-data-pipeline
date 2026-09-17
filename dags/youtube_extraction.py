import sys
from datetime import datetime, timedelta

sys.path.insert(0, "/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from src.ingestion.youtube_api import (
    extract_channel,
    extract_videos,
    extract_video_details,
    generate_videos_json,
)


default_args = {
    "owner": "youtube-pipeline",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "email_on_failure": False,
    "email_on_retry": False,
}


with DAG(
    dag_id="youtube_extraction",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="0 2 * * *",
    catchup=False,
    tags=["youtube", "extraction"],
) as dag:

    get_channel = PythonOperator(
        task_id="get_channel",
        python_callable=extract_channel,
    )

    get_videos = PythonOperator(
        task_id="get_videos",
        python_callable=extract_videos,
    )

    get_video_details = PythonOperator(
        task_id="get_video_details",
        python_callable=extract_video_details,
    )

    generate_json = PythonOperator(
        task_id="generate_json",
        python_callable=generate_videos_json,
    )

    trigger_datawarehouse = TriggerDagRunOperator(
        task_id="trigger_datawarehouse",
        trigger_dag_id="youtube_datawarehouse",
        wait_for_completion=False,
    )

    get_channel >> get_videos >> get_video_details >> generate_json >> trigger_datawarehouse