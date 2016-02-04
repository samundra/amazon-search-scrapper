import codecs
import csv
import os
from urllib2 import URLError
from bs4 import BeautifulSoup
from product import Product
from unicode_writer import UnicodeWriter
from datetime import datetime

import sys


class Page:
    def set_title(self, title):
        self.title = title
        return self

    def set_url(self, url):
        self.url = url
        return self

    def set_data(self, data):
        self.data = data
        return self

    def get_data(self):
        return self.data

    def get_title(self):
        return self.title

    def navigate(self, url):
        try:
            self.product.set_url(url)
            self.product.scrape()

            return self

        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code

    def scrap(self):
        soup = BeautifulSoup(self.get_data(), "lxml")
        results = soup.select("#s-results-list-atf .s-access-detail-page")

        for result in results:
            product_link = result.get("href")
            self.product_links.append(product_link)

        self.save_to_unicode(self.outfile, ["url", "title", "sale-price", "short-description"])

        self.save_product_links_to_csv()

        # self.crawl_product_pages()

    def save_product_links_to_csv(self):
        with open("LED-Shop-and-Garage-Bulb.csv", "ab+") as outfile:
            for link in self.product_links:
                outfile.write(str(link) + "\n")

    def crawl_product_pages(self):
        for link in self.product_links:
            self.navigate(link)

            url = self.product.get_url()
            title = self.product.get_title()
            sale_price = self.product.get_sale_price()
            short_description = self.product.get_short_description()

            self.save_to_unicode(self.outfile, [url, title, sale_price, short_description])

            # #TODO Remove this exit code
            # sys.exit(0)

    def get_pagination_link(self):
        soup = BeautifulSoup(self.get_data(), "lxml")

        pagination_links = soup.select("#pagnNextLink")

        for next_page_link in pagination_links:
            link = next_page_link.get("href")
            return link
        pass

    def get_max_pagination_num(self):
        soup = BeautifulSoup(self.get_data(), "lxml")
        max_page_number = soup.select(".pagnDisabled")

        for page_number in max_page_number:
            self.max_page_number = page_number.get_text()
            return self.max_page_number

    def save_to_unicode(self, csv_filename, row):
        try:
            with codecs.open(csv_filename, 'ab+') as file_obj:
                wr = UnicodeWriter(file_obj)
                wr.writerow(row)
        except AttributeError as e:
            print e.code
            print e.message

    def set_response(self, response):
        self.response = response
        pass

    def set_out_file(self, filename):
        path = 'Data'
        outfile = filename + str(datetime.now().strftime('%Y-%m-%d %H_%M_%S')) + ".csv"
        outfile = os.path.join(path, outfile)
        self.outfile = outfile

    def __init__(self):
        self.url = None
        self.title = None
        self.data = None
        # self.b = BeautifulSoup()
        self.product_links = []
        self.response = None
        self.product = Product()
        self.pagination_links = []
        self.max_page_number = None
        self.outfile = "out_"
