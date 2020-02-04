import csv
import urllib.request

with open('/home/christopher/Downloads/freemidi.org-(Crawl-Run)---2020-01-24T225844Z.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['Genre Link'], row['Genre Link_link'])
        # Download the file from `url` and save it locally under `file_name`:
        with urllib.request.urlopen(row['Genre Link_link']) as response, open(row['Genre Link']+'.mid', 'wb') as out_file:
            data = response.read() # a `bytes` object
            out_file.write(data)