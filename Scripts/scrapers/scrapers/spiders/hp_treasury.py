from scrapy import Spider
from scrapy import FormRequest
from scrapy import Request
import csv
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='hp_treasury.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BudgetSpider(Spider):
    name = 'hp_treasury'

    def start_requests(self):
        url = "https://himkosh.nic.in/eHPOLTIS/PublicReports/wfrmBudgetAllocationbyFD.aspx"
        yield Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info("Starting the parsing process...")
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

    def parse_results(self, response):
        self.logger.info("Parsing results...")
        heads = response.xpath('//table//tr[@class="success"]//td//text()').extract()
        column_names = response.xpath('//table//tr[@class="warning"]//td//text()').extract()
        all_data_rows = response.xpath('//table//tbody//tr')

        filepath = "/home/akash/airflow/akash_assignment-main/data/treasury_data.csv"
        try:
            with open(filepath, 'w+') as output_file:
                writer = csv.writer(output_file, delimiter=',')
                writer.writerow(heads)     # writes the contents of the table headers list as a single row in the CSV file separated by comma
                writer.writerow(column_names) # writes the contents of the column names list as a single row
                for row in all_data_rows:
                    clean_data = []
                    cells = row.xpath('.//td')        # extracts all the table data elements from the current row
                    for cell in cells:
                        text = cell.xpath('.//text()').get()  # extracts text contents from the current cell
                        if text is not None:
                            clean_data.append(text)        # checks if the extracted text is not empty, if not it is appended to the clean_data
                        if text is None:                   # checks if the extracted text is empty an empty string is appended to the clean_data
                            clean_data.append('')
                    writer.writerow(clean_data)
            self.logger.info("Data extraction and writing to CSV completed.")
        except Exception as error:
            self.logger.error(f"An error occurred: {error}")
