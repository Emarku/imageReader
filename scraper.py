import requests
from bs4 import BeautifulSoup
import re
import json

def foleon_scraper(url):

    '''Function scrapes gleeds foleon pages and returns chart data'''

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    output_data = {}

    # Cycling through all iframes to rip out the data
    for iframe in soup.findAll('iframe'):
        infogram_url = iframe['src']

        r = requests.get(infogram_url)
        soup = BeautifulSoup(r.text, "html.parser")

        # Here we are finding the title of each of the plots and removing the key string
        title = soup.find('title').prettify()
        title = title.split("\n")[1]
        title = title.split("- Infogram")[0]
        
        script = [
            t 
            for t in soup.findAll("script") 
            if "window.infographicData" in t.text
        ][0].text

        extract = re.search(r".*window\.infographicData=(.*);$", script)

        data = json.loads(extract.group(1))

        entities = data["elements"]["content"]["content"]["entities"]

        tables = [
            (entities[key]["props"]["chartData"]["sheetnames"], entities[key]["props"]["chartData"]["data"])
            for key in entities.keys()
            if ("props" in entities[key]) and ("chartData" in entities[key]["props"])
        ]

        sub_data = []
        for i in tables[0][1][0]:
            sub_data.append(i)

        # Collecting URL and dictionary together for each data source
        sub_dictionary = {"URL":infogram_url, "Data":sub_data}

        output_data[title]=sub_dictionary
        
    
    return output_data