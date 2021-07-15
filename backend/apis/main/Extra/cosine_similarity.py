import re, math
import requests
from bs4 import BeautifulSoup
from collections import Counter

def parse_from_html(html):
     #html = str(requests.get(url,timeout=3).text)
     soup = BeautifulSoup(html, "lxml" )
     #soup = BeautifulSoup(html)
     for script in soup(["script", "style","a","p"]):
          script.extract()
     text = soup.get_text()
     return text

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator



def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)



def sim(h1, h2):
     text1 = parse_from_html(h1)
     text2 = parse_from_html(h2)


     vector1 = text_to_vector(text1)
     vector2 = text_to_vector(text2)

     cosine11 = get_cosine(vector1, vector2)
     return cosine11



