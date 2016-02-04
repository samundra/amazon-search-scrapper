import csv
import exceptions
import os.path
import sys
import threading

import product
from page import Page


def save_to_file(p):
    # print output_file
    sc_url, prod_title, sale_price = p.get_url(), p.get_title(), p.get_price()
    short_description, full_description = p.get_short_description(), p.get_full_description()

    if short_description is None:
        short_description = ""

    if full_description is None:
        full_description = ""

    page.save_to_unicode(output_file, [sc_url, prod_title, sale_price, short_description, full_description.strip()])


def scrap_all():
    count = 0
    for row in linereader:
        url = row.pop()
        parts = url.split("/")
        asin = parts.pop()

        product_file = "files/" + asin
        print product_file
        if os.path.isfile(product_file):
            try:
                p = product.Product()
                p.set_url(url)
                p.scrape(filename=product_file, from_file=True)
                t = threading.Thread(target=save_to_file, args=(p,))
                threads.append(t)
                print "Thread Processing: " + product_file
                t.start()
                print " \033[91m- completed\033[0m"
            except exceptions.AttributeError as e:
                print "Error Found"
                print url
                sys.exit(0)
                # with open("error-urls.txt", "ab+") as error_file:
                #     error_file.write(url + "\n")
                # print url
        count += 1
        # if count % 50 is 0:
        #     break;
        # sys.exit(0)


def scrap_single_product(asin, skip_save=False):
    product_file = "files/" + asin
    print product_file
    if os.path.isfile(product_file):
        p = product.Product()
        p.set_url(product_file)
        p.scrape(filename=product_file, from_file=True)

        print p.get_title()
        print p.get_price()
        print p.get_short_description()
        print p.get_full_description()

        if skip_save is False:
            save_to_file(p)


arg_list_count = len(sys.argv)
arg_list = sys.argv
single_product = False
threads = []
page = Page()
input_file = None
output_file = None
skip_single_product_save = False

if "--outfile" not in arg_list:
    print "Please specify output files to save the results. e.g. output.txt"
    print "\n\tpython --single B00W8ULUTU --outfile output.txt"
    sys.exit(1)

if "--skip-save" in arg_list:
    skip_single_product_save = True

output_file = arg_list[int(arg_list.index("--outfile")) + 1]

if "--single" in arg_list:
    single_product = True
    single_product_asin = arg_list[int(arg_list.index("--single")) + 1]
    scrap_single_product(asin=single_product_asin, skip_save=skip_single_product_save)
else:
    if "--infile" not in arg_list:
        print "Please specify source input files"
        sys.exit(1)
    else:
        print "Processing all the files"
        input_file = arg_list[int(arg_list.index("--infile")) + 1]

        if not os.path.isfile(input_file):
            print "Source file {} do not exists.".format(input_file)
            sys.exit(1)
        page.save_to_unicode(output_file,
                             ["url", "title", "price", "short_description", "full_description"])
        with open(input_file, "rb") as csv_file:
            # with open("files/LED-Strip-Lights.csv", "rb") as csv_file:
            linereader = csv.reader(csv_file, delimiter=",")
            scrap_all()
