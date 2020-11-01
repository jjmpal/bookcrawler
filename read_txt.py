#!/opt/local/bin//python3

import pyttsx3
from bs4 import BeautifulSoup

with open('dbt.html', 'r') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    for table in soup.find_all("table"):
        table.extract()

content = []
for p in soup.findAll(["p", "h1", "h2", "h3"]):
    content.append(p.getText() + "\n")

all_content = "\n".join(content)

print(all_content)

exit()

engine = pyttsx3.init()
engine.setProperty('rate', 165)
engine.setProperty('volume', 1.0)
engine.setProperty('voice', "com.apple.speech.synthesis.voice.tessa")
engine.save_to_file(all_content, "wav/dbt.wav")
engine.runAndWait()
engine.stop()
