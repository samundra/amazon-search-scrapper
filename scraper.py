import logging
import re
import sys
import urllib2
from page import Page
from product import Product
import threading
import time


class Scraper:
    ROOT_DOMAIN = 'http://www.amazon.com'
    HTTP_STATUS_OK = 200
    THREAD_NUM = 5

    def __init__(self, url):
        self.url = None
        self.set_url(url)
        self.page = Page()
        self.product = Product()
        self.page_links = []
        self.output_filename = "out_"
        self.threads = []

    def set_url(self, url):
        self.url = url
        return self

    def set_output_file(self, keyword):
        self.output_filename = keyword.replace(" ", "_").lower()

    def get_page_links(self):
        return self.page_links

    def get_url(self):
        return self.url

    def build_page_links(self, max_page_num, pagination_format):

        if pagination_format is not None:
            query_string = pagination_format.split("&")
            # pages = query_string[1].split("=")
            match = re.search("page=(\d+)", pagination_format)

            page_num = int(match.group(1))

            page_dict = {
                "page": str(page_num),
                "url": self.ROOT_DOMAIN + pagination_format
            }

            self.page_links.append(page_dict)

            while page_num < int(max_page_num):
                page_num += 1

                query_string[1] = 'page=' + str(page_num)
                pack_query_string = '&'.join(query_string)

                page_dict = {
                    "page": str(page_num),
                    "url": self.ROOT_DOMAIN + pack_query_string
                }

                self.page_links.append(page_dict)

    def visit_page(self, product_list_url, page_num):
        print "Page-{}, {}".format(page_num, product_list_url)

        response = urllib2.urlopen(product_list_url)

        if response.code is self.HTTP_STATUS_OK:
            page = Page()
            page.set_data(response.read())
            page.set_url(product_list_url)
            page.set_out_file(self.output_filename + "-page-" + str(page_num) + "-")
            page.scrap()

            print "{} - Completed".format(product_list_url)
            # list_page.set_response(response)

            # products = self.page.scrap()

    def scrap_all_products(self):

        # total_links = len(self.page_links)
        # print "Total Links : " + str(total_links)
        #
        # chunks = total_links / self.THREAD_NUM
        # remaining = total_links % self.THREAD_NUM
        #
        # print "Loop Required : " + str(chunks)
        # print "Starting Thread Count :" + str(self.THREAD_NUM)
        # print "Remaining Count : " + str(remaining)
        #
        # for i in range(0, chunks):
        #     for idx in range(self.THREAD_NUM):
        #         # print idx
        #         link = self.page_links[idx]
        #         page_num = link["page"]
        #         page_url = link["url"]
        #         #
        #         print "Starting Thread for url: " + page_url
        #         # t = threading.Thread(target=self.visit_page, args=(page_url, page_num,))
        #         # self.threads.append(t)
        #         # t.start()

        #
        # start_index = self.THREAD_NUM * chunks
        # #
        # remaining_chunk = total_links % self.THREAD_NUM
        # #
        # for j in range(remaining_chunk):
        #     print "Starting Thread for remaining urls"
        #     link = self.page_links[start_index]
        #     page_num = link["page"]
        #     page_url = link["url"]
        #
        #     print page_url
        #
        #     # t = threading.Thread(target=self.visit_page, args=(page_url, page_num,))
        #     # self.threads.append(t)
        #     #
        #     # print "Starting Thread for url: " + page_url
        #     # t.start()
        #
        #     start_index += 1

        count = 0;
        for link in self.page_links:
            # print link["url"]
            page_num = link["page"]
            page_url = link["url"]

            if (count % 4) is 0:
                time.sleep(5)

            t = threading.Thread(target=self.visit_page, args=(page_url, page_num,))
            self.threads.append(t)
            print "Starting Thread for url: " + page_url
            count += 1
            t.start()
            # self.visit_page(product_list_url=page_url, page_num=page_num)

    def main(self):
        try:
            opener = urllib2.build_opener()
            # opener.add_headers = [
            #     ('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'),
            #     ('Referer', 'http://www.amazon.com/?field-keywords=LED+Lights'),
            #     ('Host', 'www.amazon.com'),
            #     ('Content-Type', 'application/x-www-form-urlencoded'),
            #     ('X-Requested-With', 'XMLHttpRequest'),
            #     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            # ]
            response = opener.open(self.get_url())
            # #
            # # print response.code
            #
            #
            # # response.code = 200
            #
            # # request = urllib2.Request(self.get_url())
            # # response = urllib2.urlopen(request, None, headers)

            if response.code is self.HTTP_STATUS_OK:
                # if True:
                html = response.read()

                # # TODO Remove this hard-coded page listings
                # fh = open("listing-1.html", "rb+")
                # html = fh.read()

                self.page.set_data(html)
                self.page.set_url(self.get_url())
                self.page.scrap()

                pagination_link_format = self.page.get_pagination_link()
                max_pagination_number = self.page.get_max_pagination_num()
                logging.info("Max pagination number found : " + max_pagination_number)

                # link = s.build_page_links(20, "/s?ie=UTF8&page=2&rh=i%3Aaps%2Ck%3ABrown%20LED")
                self.build_page_links(max_pagination_number, pagination_link_format)

                # print self.page_links
                self.scrap_all_products()
            else:
                print "Something did not work properly."

        except urllib2.HTTPError as e:
            print e.code
            print e.reason
