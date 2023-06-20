import requests
from bs4 import BeautifulSoup
import re
import json

infogram_url = f'https://e.infogram.com/_/LZxiw3cLUAm7uBMQlBsD?src=embed%22%20title=%22India%2012Q23%20fig%202%20historical%20GDP%22%20width=%221062%22%20height=%22606%22%20scrolling=%22no%22%20frameborder=%220%22%20style=%22border:none;%22%20allowfullscreen=%22allowfullscreen%22'
r = requests.get(infogram_url)
soup = BeautifulSoup(r.text, "html.parser")

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

print(tables)