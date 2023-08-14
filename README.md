Himachal Pradesh Treasury Data ETL Pipeline
===========================================

This repository contains an ETL (Extract, Transform, Load) pipeline to scrape, preprocess, and load data from the Himachal Pradesh Treasury website. The pipeline is orchestrated using Apache Airflow. The pipeline consists of three main steps: scraping data with Scrapy, preprocessing with Pandas, and writing data to an SQLite database.

Prerequisites
-------------

```
pip install requirements.txt
```

Pipeline Components
-------------------

1. Extraction

Scrapy Spider: A Scrapy spider named ```hp_treasury``` is used to scrape data from the website (https://himkosh.nic.in/eHPOLTIS/PublicReports/wfrmBudgetAllocationbyFD.aspx). The scraped data is saved to a CSV file.

2. Transformation

Preprocessing Script: The ```preprocessing.py``` script performs data preprocessing on the scraped data. It handles missing values, renames columns, and splits columns for improved organization.

3. Loading

Database Write Script: The write_db.py script reads the preprocessed data CSV file and writes it to a SQLite database named ```assignment.sqlite```.

4. Orchestration
   
Airflow DAG: The data pipeline is orchestrated using an Apache Airflow DAG named ```hp_pipeline``` It schedules the Scrapy spider, preprocessing script, and database write script to run sequentially.




