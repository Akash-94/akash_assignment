
from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator


DEFAULT_ARGS = {
    'owner': 'airflow',
    'start_date': datetime.today().replace(day=1),
    'concurrency': 1
}

with DAG('hp_pipeline',
         default_args=DEFAULT_ARGS,
         schedule_interval='30 10 * * *',  # the timezone is UTC here.
         catchup=False
         ) as dag:

    SCRAPING_TASK = BashOperator(
        task_id = 'scrape',
        bash_command = 'cd /home/akash/airflow/akash_assignment-main/Scripts/scrapers/scrapers/spiders && scrapy crawl hp_treasury'
    )
    PREPROCESSING_TASK = BashOperator(
        task_id = 'preprocessing',
        bash_command = 'cd /home/akash/airflow/akash_assignment-main/Scripts && python3 preprocessing.py'
    )
    WRITE_DB = BashOperator(
        task_id = 'write_db',
        bash_command = 'cd /home/akash/airflow/akash_assignment-main/Scripts && python3 write_db.py'
    )

SCRAPING_TASK.set_downstream(PREPROCESSING_TASK)
PREPROCESSING_TASK.set_downstream(WRITE_DB)

