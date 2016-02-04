import csv
import os.path

with open("files/LED-Strip-Lights.csv","rb") as csv_file, open("files/LED-Strip-Lights-missing.csv", "wb+") as csv_outfile:
    linereader = csv.reader(csv_file, delimiter=",")

    for row in linereader:
        url = row.pop()

        parts = url.split("/")
        asin = parts.pop()

        if not os.path.isfile("files/"+asin):
            print "Missing : "+ asin
            csv_outfile.write(url+"\n")
            # print asin
            # print parts
            # parts = re.search("")
            # print url
