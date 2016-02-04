import logging
import os
import csv
import urllib2
from datetime import datetime
from urllib2 import URLError

import sys
from bs4 import BeautifulSoup


class Product:
    """ Parses the website page """

    def __init__(self):
        path = 'Log/Amazon'
        filename = "scraper_" + str(datetime.now().strftime('%Y-%m-%d %H_%M_%S')) + ".txt"
        filename = os.path.join(path, filename)
        logging.basicConfig(filename=filename, level=logging.DEBUG)
        pass

    def set_title(self, title):
        self.title = title

    def set_price(self, price):
        self.price = price
        return self

    def set_sale_price(self, sale_price):
        self.sale_price = sale_price
        return self

    def set_description(self, description):
        self.description = description
        return self

    def set_short_description(self, short_description):
        self.short_description = short_description
        return self

    def set_data(self, data):
        self.data = data
        return self

    def set_logger(self, logger):
        self.logger = logger
        return self

    def set_soup(self, contents):
        self.soup = BeautifulSoup(contents, "lxml")

    def get_data(self):
        return self.data

    def get_info_tuple(self):
        return self.price, self.sale_price, self.short_description, self.description

    def set_asin(self, asin):
        self.asin = asin
        return self

    def set_url(self, url):
        self.url = url
        return self

    def get_asin(self):
        return self.asin

    def get_url(self):
        return self.url

    def get_title(self):
        return self.title

    def get_price(self):
        return self.price

    def get_sale_price(self):
        return self.sale_price

    def get_short_description(self):
        return self.short_description

    def get_full_description(self):
        return self.description

    def parse_title(self):
        logging.info("AMAZON_SCRAPPER: Parsing title")
        # print "AMAZON_SCRAPPER: Parsing title"

        ptitle = self.soup.select("#productTitle")

        for title in ptitle:
            product_title = title.get_text()

            if product_title is None:
                product_title = ""
            self.set_title(product_title)

        return self

    def parse_price(self):
        logging.info("AMAZON_SCRAPPER: Parsing sale price")
        # print "AMAZON_SCRAPPER: Parsing sale price"

        price_block_saleprice = self.soup.select("#priceblock_ourprice")

        price = None
        for sp in price_block_saleprice:
            price = sp.get_text()

        if price is None:
            logging.info("AMAZON_SCRAPPER: Price is Empty, trying #priceblock_ourprice")
            price_block = self.soup.select("#priceblock_ourprice")

            for price in price_block:
                price = price.get_text()

            if price is None:
                sale_price_block = self.soup.select("#priceblock_saleprice")
                for sale_price in sale_price_block:
                    price = sale_price.get_text()

                if price is None:
                    logging.info("AMAZON_SCRAPPER: Our Price is Empty, trying #priceblock_dealprice")
                    deal_price_block = self.soup.select("#priceblock_dealprice")

                    for deal_price in deal_price_block:
                        price = deal_price.get_text()

                    if price is None:
                        logging.info("AMAZON_SCRAPPER: Didn't find the price")
        else:
            logging.info("AMAZON_SCRAPPER: Sale Price Found :" + price)

        if price is None:
            price = "Not Found"

        # print price
        # print "--------------"
        self.set_price(price)
        return self

    def parse_short_description(self):
        logging.info("AMAZON_SCRAPPER: Parsing short description")
        # print "AMAZON_SCRAPPER: Parsing short description"

        des = self.soup.select("#feature-bullets span.a-list-item")

        first = True
        strs = []

        # Skip the hidden element that is at the top
        for item in des:
            if first:
                # print "First --"
                first = False
                continue
            strs.append(item.get_text())

        short_description = "\r\n".join(strs)

        if short_description is None:
            short_description = "Not Found"

        self.set_short_description(short_description)

        return self

    def parse_full_description(self):
        logging.info("AMAZON_SCRAPPER: Parsing full description")

        des = self.soup.select(".productDescriptionWrapper")

        for description in des:
            product_description = description.get_text()

            if product_description is None:
                product_description = "Not Found"

            self.set_description(product_description)

        return self

    def scrape(self, filename=None, from_file=False):
        user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
        data = None
        headers = {'User-Agent': user_agent}

        if from_file is False:
            product_url = self.get_url()
            logging.info("AMAZON_SCRAPPER: Visit product : " + product_url)
            print "AMAZON_SCRAPPER: Visit product : " + product_url
            request = urllib2.Request(product_url, data, headers)

        try:
            status_code = 200
            data = None

            if from_file is False:
                response = urllib2.urlopen(request)
                status_code = response.code
                data = response.read()

            if status_code is 200:
                if from_file is True:
                    with open(filename, "rb") as product_file:
                        data = product_file.read()

                # if data is None:
                #     print "data is None"
                # else:
                #     fw = open("data-file.html","wb+")
                #     fw.write(data)
                #     fw.close()

                self.set_data(data)
                self.set_soup(data)

                self.parse_title()
                self.parse_price()
                self.parse_short_description()
                self.parse_full_description()
            else:
                # print response.code
                print "Not good"

            # return response
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code

    def get_product_details(self):
        fp = file("product_details.txt", "r")
        data = fp.read()
        self.set_data(data)
        self.set_soup(data)
        self.parse_short_description()

        short_description = self.get_short_description()
        # self.save_to_unicode("output.csv", [short_description])
        # print short_desc

        # strs = []
        # for i in short_desc:
        #     strs.append(str(i))
        #
        # w = file("output.csv","ab+")
        # w.write(''.join(strs))
        # w.close()

        print "completed"

    # def save_to_unicode(self, csv_filename, row):
    #     with codecs.open(csv_filename, 'a+') as file_obj:
    #         wr = UnicodeWriter(file_obj)
    #         wr.writerow(row)

    def get_info_dict(self):
        return {
            'price': self.price,
            'sale_price': self.sale_price,
            'partial_description': self.short_description,
            'description': self.description
        }

    title = None
    price = None
    asin = None
    url = None
    data = None
    sale_price = None
    description = None
    short_description = None
    parsers = []
    soup = None
    logger = None
