import tldextract
import requests
import re
from bs4 import BeautifulSoup
from .similarity import Similarity

class Suggestions:
    def __init__(self,url,num=100):
        self.suggested_urls=[]
        self.found=0
        self.err=0
        self.num=str(num)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }

        r=tldextract.extract(url)
        if(url[:4]!='http'):
            url='https://'+r.subdomain+'.'+r.domain+'.'+r.suffix
        self.original_domain=r.domain
        self.original_subdomain=r.subdomain
        try:
            res=requests.get(url,headers=headers,timeout=3)
            query_string=self.original_domain+'%20'+self.original_subdomain
            soup=BeautifulSoup(res.content,"lxml")
            for title in soup.find_all('title'):
                query_string=query_string+'%20'+title.get_text()

            self.query_string=query_string
            print(query_string)
        except:
            self.err=1

    def detect(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }
        try:
            page = requests.get(f"https://www.google.dz/search?q={self.query_string}&num={self.num}",headers=headers,timeout=3)
        except:
            self.err=1

        soup = BeautifulSoup(page.content,"lxml")
        #links = soup.findAll("a")
        i=0
        useful_links=[]
        for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
            google_url=str(re.split(":(?=http)",link["href"].replace("/url?q=",""))[0])
            r=tldextract.extract(google_url)
            '''if(self.num=="100"):
                print(google_url)
                print(r.subdomain,r.domain)'''
            if(i>=int(self.num)):
                break
            if(r.domain==self.original_domain and r.subdomain==self.original_subdomain):
                self.found=1
                return
            
            sim=Similarity(self.original_domain,r.domain)
            sim.final_score()
            useful_links.append((google_url,sim.score))
            i=i+1
        
        useful_links=sorted(useful_links, key=lambda x: x[1], reverse=True)
        some_links=[]
        for i in useful_links:
            if(i[0] not in some_links):
                some_links.append(i[0])
                if(len(some_links)>=10):
                    break
        self.suggested_urls=some_links