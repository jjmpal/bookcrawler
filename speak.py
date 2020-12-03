#!/opt/local/bin//python3

import pyttsx3
import sys
from bs4 import BeautifulSoup
import re

engine = pyttsx3.init()

if len(sys.argv) != 3:
    print("Usage: %s <input> <output>"%sys.argv[0])
    exit(1)

finput = sys.argv[1]
foutput = sys.argv[2]
    
with open(finput, 'r') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    for table in soup.find_all("table"):
        table.extract()
    for anchor in soup.findAll('a'):
        anchor.extract()

replacers = {
    "LVH": "left ventricle hypertrophy",
    "LV": "left ventricle",
    "RV": "right ventricle"}
        
content = []
for p in soup.findAll(["p", "h1", "h2", "h3"]):
    line = re.sub("([.,?!;])", r"  \1 ", p.getText())
    repline = ' '.join([replacers.get(e, e) for e in line.split()])
    content.append(repline + "\n")


all_content = "\n".join(content)

engine = pyttsx3.init()
#engine.setProperty('rate', 165)
engine.setProperty('volume', 1.0)
#engine.setProperty('voice', "com.apple.speech.synthesis.voice.tessa")
engine.setProperty('voice', "com.apple.speech.synthesis.voice.daniel")
engine.save_to_file(all_content, foutput)
engine.runAndWait()
engine.stop()
