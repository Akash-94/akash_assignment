
Airflow DAG Documentation: HP Data Pipeline
-------------------------------------------

Overview
---------
The HP Data Pipeline is an Airflow Directed Acyclic Graph (DAG) that automates the process of scraping, preprocessing, and writing data to a database using the Airflow platform. This DAG performs these tasks sequentially, ensuring a streamlined data processing workflow.

Prerequisites
-------------

1. **Airflow Installation**

Apache airflow can be installed using the command shown below

.. code-block:: python

    pip install "apache-airflow[celery]==2.6.3" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.6.3/constraints-3.7.txt"

Upon running these commands, Airflow will create the ```airflow.cfg``` file with the defaults that are sufficient to run airflow. One can override defaults using environment variables, see Configuration Reference (https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html). 

2. **Airflow Database**

Airflow uses a database to store its metadata. The database is configured in the 'airflow.cfg' file and one has to initialize the database. Use the following command.

.. code-block:: python

        airflow db init
        airflow db upgrade

3. **Airflow - Create User**

Create user attributes such as username, role, e-mail, first name, last name, and password.

.. code-block:: python

        airflow users create --role admin --username admin --email admin --firstname admin --lastname admin --password admin


Creating and Running a DAG (Example)
------------------------------------

1. **Create a Directory**

Create a directory to store DAG scripts. For example, create a directory named dags within Airflow project directory.

.. code-block:: python

    ~$ mkdir AIRFLOW_HOME
    ~$ cd AIRFLOW_HOME

    ~/AIRFLOW_HOME$ mkdir dags
    ~/AIRFLOW_HOME$ cd dags

2. **Write a DAG Script**

Inside the dags directory, create a Python script for the DAG with dummy tasks

.. code-block:: python

   ~/AIRFLOW_HOME/dags$ nano demo_dag.py

3. **Start Airflow Scheduler**

To execute a DAG, the airflow scheduler needs to be running. Run the following command from the command line to start the scheduler.

.. code-block:: python

   airflow scheduler

4. **Start Airflow Web Server**

To monitor and manage the DAGs through the Airflow web interface, one has to the web server. Run the following command from the command line to start the web server.

.. code-block:: python

   airflow webserver

5. **Access Airflow UI**

Open a web browser and go to http://localhost:8080 to access the Airflow web interface and search for demo_dag listed on the UI.

6. **Trigger the DAG**

On the Airflow UI, locate demo_dag and click the "Trigger DAG" button to manually trigger its execution.

HP Data Pipeline Description:
-----------------------------
The HP Data Pipeline DAG consists of three main tasks:

Scraping Task (scrape)

The scraping task is responsible for initiating the data scraping process using a web scraping script. It invokes the ```scrapy crawl hp_treasury``` command to scrape data from a specified website.
The scraping task initiates subsequent processing steps by providing the raw data for further analysis.

Preprocessing Task (preprocessing)

Once the data is scraped, the preprocessing task is executed. It performs data pre-processing and transformation on the scraped data to make it suitable for analysis and storage.
The preprocessing task invokes the python ```preprocessing.py``` command, which applies data transformations, cleaning, and structuring to the scraped data.

Write to Database Task (write_db)

After the data is preprocessed, the write-to-database task is triggered. It takes the cleaned and transformed data and writes it to a database for persistent storage.
The task invokes the Python ```write_db.py``` command, which connects to the database and inserts the processed data.


DAG Configurations
------------------
Default Arguments

- Owner: airflow
- Start Date: The start date is set to the current date with the day of the month as 1
- Concurrency: 1 (To ensure tasks are executed sequentially)
- Schedule Interval: '30 10 * * *' (Every day at 10:30 AM UTC)
- Catchup: Disabled (Tasks are not backfilled for past dates)

.. code-block:: python

    DEFAULT_ARGS = {'owner': 'airflow',
                    'start_date': datetime.today().replace(day=1),
                    'concurrency': 1}

    with DAG('hp_pipeline',
             default_args=DEFAULT_ARGS,
             schedule_interval='30 10 * * *',  
             catchup=False) as dag:

Tasks
------
Task 1. `Scrape`: scrapes budget data from a website using a Scrapy spider.

.. code-block:: python

    SCRAPING_TASK = BashOperator(
        task_id = 'scrape',
        bash_command = 'cd /home/akash/airflow/akash_assignment-main/Scripts/scrapers/scrapers/spiders && scrapy crawl hp_treasury'
    )

Task 2: `Preprocessing`: Preprocesses the scraped data to clean and transform it.

.. code-block:: python

   PREPROCESSING_TASK = BashOperator(
        task_id = 'preprocessing',
        bash_command = 'cd /home/akash/airflow/akash_assignment-main/Scripts && python3 preprocessing.py'
    )
    
Task 3. `write_db`: Writes the processed data to a database.

.. code-block:: python

     WRITE_DB = BashOperator(
        task_id = 'write_db',
        bash_command = 'cd /home/akash/airflow/akash_assignment-main/Scripts && python3 write_db.py'
    )


Setting Dependencies
---------------------

The dependencies are set to direct the DAG to run individual tasks in a pre-defined manner. In this case
Scrape task is set to execute first, upon its successful execution preprocessing task is executed, and finally write_db is executed as the last task.

.. code-block:: python

     SCRAPING_TASK.set_downstream(PREPROCESSING_TASK)
     PREPROCESSING_TASK.set_downstream(WRITE_DB)
