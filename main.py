import urllib
import bcolors
import sys
from scraper import Scraper

# keywords = urllib.urlencode({"field-keywords": "LED Shop"})
# search_keyword = "LED Shop and Garage Bulb"
# search_keyword = "LED Strip Lights"


# url = "http://www.amazon.com/s/ref=sr_pg_20?rh=i%3Aaps%2Ck%3ALED&page=20&keywords=LED&ie=UTF8&qid=1454475649&spIA=B00GOJ9R6O,B00QUE072Q,B0182DXKWQ,B00AC6YQ3Y,B00YT3CTKS,B0030B0HKO"
# print "scrapping url : "+url
def show_version():
    print "alpha1.0"
    sys.exit(0)

def show_help():
    print "Usage: python main.py [--search SEARCH_KEYWORD][--help][--version]\n"\
          "                      [--outfile OUTPUT_FILENAME]\n"\
          "Command Line Utility to Scrape the Amazon Vendor products\n"\
          "--------------------------------------------------------------\n"\
          "Optional Arguments:\n"\
          "--search SEARCH_KEYWORD\t\tSpecify the search keyword\n"\
          "--outfile OUTPUT_FILENAME\tSaves the output in the specified output file\n"\
          "--version\t\t\tShow the version number and exit\n"\
          "--help\t\t\t\tShow this help message and exit\n"
    sys.exit(1)

argument_list = sys.argv

if "--help" in argument_list:
    show_help()

if "--version" in argument_list:
    show_version()

if "--search" not in argument_list:
    # print bcolors.bcolors.bred("Enter vendor product to search.")
    show_help()
    sys.exit(1)

if "--outfile" not in argument_list:
    print bcolors.bcolors.bred("Outfile was not found, outfile will match to the keywords.")
    print bcolors.bcolors.bred("Example: \n Keyword : LED strip lights")
    print bcolors.bcolors.bred("         \n Outfile : led-strip-lights.csv")

argument_count = len(sys.argv)

if argument_count >= 3:
    search_index = argument_list.index("--search")
    search_keyword = argument_list[search_index + 1]
    query_string = urllib.urlencode({"field-keywords": search_keyword})
    url = "http://www.amazon.com/s/?" + query_string
    print "Scrapping : " + bcolors.bcolors.bgreen(url)

    s = Scraper(url)
    s.set_output_file(search_keyword)
    s.main()

else:
    # print bcolors.bcolors.bred("Enter vendor product to search.")
    show_help()
