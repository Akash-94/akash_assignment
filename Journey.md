Overview of Orchestrating a Data Pipeline: My Journey
=====================================================

Day 1 - Data Mining/Web Scraping
--------------------------------

On the first day, I delved into web scraping techniques to gather data. Due to my limited prior experience, I opted for Scrapy, a widely-used framework in the open-source community (Ref - https://medium.com/codex/the-top-10-open-source-web-scraping-tools-in-2022-ede0134a00d).
I referred to various resources to grasp the concepts and functionalities of web scraping. As I progressed, I gained the workings of Scrapy's spider module, which enabled me to navigate through pages and extract the desired data. However, my initial attempts at extracting data from an HP treasury portal posed challenges.

Reasons for Challenges

1. I overlooked the need to make a POST request to access the results page.
2. The portal was in .aspx format, and I missed the fact that the URL didn't change when navigating to the results page (by entering details manually).

To overcome these hurdles, I conducted some studies to address these issues. Eventually, I successfully navigated to the result page and accessed the desired data.

References

https://medium.com/@simranpandey97/web-scraper-for-aspx-form-based-webpages-b8828085e4a2

https://github.com/simran-pandey/Scrapy-and-BeautifulSoup-web-scraper-for-ASP.NET-webpages.git

https://youtu.be/jTKL2qTw2Rc

Day 2-3 - Parsing Results
-------------------------

During these days, I focused on extracting data from the result page, which proved to be a challenge. I struggled with accessing the table and its elements due to improper use of CSS selectors and XPath. To resolve this, I employed the Google Chrome extension ```SelectorsHub```, which assisted in selecting the correct XPath.

Eventually, I managed to extract all 7000+ rows of data into a single column. Next, I tackled writing this data into a CSV file. The table headers and column names were initially written to the first two rows of the CSV. I intended to remove these rows so no data manipulation was done.

To separate the data into distinct rows and columns, I initialized an empty list called ```clean_data```. I iterated through completed rows, then iterated through cells within each row, appending ```clean_data``` with text if present or an empty string if not.

Day 4 - Data Preprocessing
--------------------------

After successfully extracting the data in the desired format, data preprocessing became straightforward. Using the Pandas module, I imported the CSV file, skipping the unnecessary first row and table header. I then dropped the initial two rows, which were column headers and a grand total. This led to auto-named columns (0, 1, 2...), which I renamed in further process.

I addressed the ```DmdCd``` column using forward fill, and filtered out rows containing ```Total```. I then split and renamed the ```DmdCd``` and ```HOA``` columns based on the '-' delimiter, discarding empty columns and reordering the columns using list indexing.

With all transformations complete, I generated a clean dataset and wrote it to a new CSV file, ready for database loading. 

SQlite3 was used to write the CSV data into the database. A demo database ```assignment.db``` was created and a connection to that database was established. Data was written to the with parameter ```if_exists ='replace'``` (to replace with new data in the table).

Day 5 - Airflow
---------------

On this day, I orchestrated the pipeline to run daily at 10:30 AM with ```dag_id = hp_pipeline``` I employed the BashOperator to execute DAGs.

The pipeline involved three main tasks:

1. Scraping Task: Using a Scrapy spider, data was scraped from a website.
2. Preprocessing Task: Scraped data underwent cleaning and transformation.
3. Write to DB Task: Processed data was written to a SQLite3 database.

Throughout DAG run process, I encountered challenges, such as dealing with absolute paths using the ```os``` module in DAGs. Despite this, I successfully established a functional data pipeline (Using full path), ready to automate the process daily.
