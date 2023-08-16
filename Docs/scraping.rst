Scraping - HP Treasury Spider
=============================

This Scrapy spider collects budget allocation data from the HP Treasury website (https://himkosh.nic.in/).
It navigates through the required pages, fills in a form, and extracts data.

Usage
-----
1. Install Scrapy using

.. code-block:: python

   pip install scrapy

2. Start scrapy project

.. code-block:: python

   scrapy startproject BudgetSpider

3. Create spider

.. code-block:: python

   scrapy genspider hp_treasury himkosh.nic.in

4. Run the spider using

.. code-block:: python

   scrapy crawl hp_treasury


Scraping
--------

**Budget Spider**

The module ```BudgetSpider``` contains a Scrapy Spider named ```hp_treasury``` that is designed to scrape budget allocation data from the Himachal Pradesh Treasury website.

.. code-block:: python

        class BudgetSpider(Spider):
            name = 'hp_treasury'

**Start Requests**

The spider starts by sending a request to the specified URL and receives a response.

.. code-block:: python

        def start_requests(self):
            url = "https://himkosh.nic.in/eHPOLTIS/PublicReports/wfrmBudgetAllocationbyFD.aspx"
            yield Request(url=url, callback=self.parse)

**Parsing**

Upon receiving the response, the spider extracts and sends the necessary post data to retrieve budget data for a specific date range.

.. code-block:: python

        def parse(self, response):
            post_data = {
                'ctl00$MainContent$txtFromDate': '01/04/2018',
                'ctl00$MainContent$txtQueryDate': '31/03/2022',
                'ctl00$MainContent$hdnMinDate': '01/04/2016',
                'ctl00$MainContent$hdnMaxDate': '07/08/2023',
                'ctl00$MainContent$ddlQuery': 'DmdCd,HOA',
                'ctl00$MainContent$txtDemand': '',
                'ctl00$MainContent$txtHOD': '',
                'ctl00$MainContent$txtMajor': '',
                'ctl00$MainContent$txtSubmajor': '',
                'ctl00$MainContent$txtMinor': '',
                'ctl00$MainContent$rbtUnit': '0',
                'ctl00$MainContent$btnGetdata': 'View Data'
            }
            yield FormRequest.from_response(response, url=response.url, formdata=post_data, callback=self.parse_results)

**Parsing Results**

The function parses the results page, extracts budget allocation data, cleans it, and writes it to a CSV file.

.. code-block:: python

        def parse_results(self, response):
            heads = response.xpath('//table//tr[@class="success"]//td//text()').extract()
            column_names = response.xpath('//table//tr[@class="warning"]//td//text()').extract()
            all_data_rows = response.xpath('//table//tbody//tr')
    
            filepath = "../../data/treasury_data.csv"
            try:
                with open(filepath, 'w+') as output_file:
                    writer = csv.writer(output_file, delimiter=',')
                    writer.writerow(heads)  # writes the contents of the table headers list as a single row in the CSV file separated by comma
                    writer.writerow(column_names)  # writes the contents of the column names list as a single row 
                    
                    for row in all_data_rows:
                        clean_data = []
                        cells = row.xpath('.//td')  # extracts all the table data elements from the current row 
                        
                        for cell in cells:
                            text = cell.xpath('.//text()').get()  # extracts text contents from the current cell 
                            if text is not None:
                                clean_data.append(text)     # checks if the extracted text is not empty, if not it is appended to the clean_data
                            if text is None:                # checks if the extracted text is empty an empty string is appended to the clean_data
                                clean_data.append('')
                        writer.writerow(clean_data)
                        
                            
            except Exception as error:
                self.logger.error(f"An error occurred: {error}")
Args

    response (Response): The response object from the FormRequest.

Note

    This method uses XPath selectors to extract data from the HTML response.
