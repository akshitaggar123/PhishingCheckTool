from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import threading
import tldextract
import requests
from .models import Url,Person,Report,Fraud,Verify
from .generator import Domain_generator
import datetime
from datetime import date
from html_similarity import style_similarity, structural_similarity, similarity
from bs4 import BeautifulSoup
from .features import Features
import re
import random
import string
import time
import pickle
import joblib
import os
from .suggestions import Suggestions

def find(arr,item):
    for i in arr:
        if(i["url"]==item):
            return 1
    return 0

def thread_function(index,possible_urls,responses,original_text,workers,headers):

    work_load=int(len(possible_urls)/workers)
    end=(index+1)*work_load
    if(index==workers-1):
        end=len(possible_urls)

    
    for i in range(index*work_load,end):
        '''for j in range(2):
            res=-1
            try:
                if(j==0):
                    res=requests.get(possible_urls[i],timeout=3)
                else:
                    #print('I came here')
                    res=requests.get(possible_urls[i],timeout=8)
                if(res):
                    #print(f'Success site {possible_urls[i]}')
                    responses[i]=sim(str(res.text),original_text)*100
                    #print(f'{i}. {possible_urls[i]} --> {responses[i]} %')
                    break
                
                else:
                    break

            except requests.exceptions.Timeout:
                if(j==1):
                    break
            
            except:
                break'''
        try:
            res=requests.get(possible_urls[i],headers=headers,timeout=3)
            #print(f'{res.status} - {possible_urls[i]}')
            if(res):
                #responses[i]=sim(str(res.text),original_text)*100
                responses[i]=similarity(str(res.text),original_text)*100
        except Exception:
            pass
            #print (f'{possible_urls[i]} :  f{e.__class__.__name__}')

# Create your views here.

def common(request):
    id=''.join(random.choices(string.ascii_uppercase +string.digits, k = 10))
    if request.COOKIES.get('id'):
        response = render(request, 'index.html',{'cookie':request.COOKIES['id']})
        print("There is cookie")
        print("Cookie is",request.COOKIES['id'])
    else:
        response = render(request, 'index.html',{'cookie':'No cookie'})
        response.set_cookie('id',id,time.time() + (10 * 365 * 24 * 60 * 60))
        print("There is no cookie")
        print("Cookie set to",id)
    return response

def flush(request,val):
    if(val=='g'):
        #"https://www.google.com",
        Url.objects.filter(main='https://www.google.com').delete()
        return HttpResponse("Deleted google")
    if(val!='p'):
        Url.objects.all().delete()
    Person.objects.all().delete()
    print("Objects deleted")
    return HttpResponse("Deleted")

def report(request):
    factor=0.3
    data={'report':0,'exceed':0}
    x = datetime.datetime.now()
    today=str(x.day)+'-'+str(x.month)+'-'+str(x.year)
    url=request.GET.get('p', '').lower()
    if(url[:4]!='http'):
        r=tldextract.extract(url)
        #https://www.youtube.com/
        url="https://"+r.subdomain+'.'+r.domain+'.'+r.suffix

    id='0'
    if request.COOKIES.get('id'):
        id=request.COOKIES['id']
    
    early=list(Verify.objects.filter(url=url,identity=id))
    if(len(early)>0):
        print("Already reported")
        data['exceed']=1
        return JsonResponse(data,safe=False)
        
    entity=list(Report.objects.filter(url=url))
    Verify.objects.create(url=url,identity=id)

    if(len(entity)>0):
        last_update=entity[0].updated
        last_count=entity[0].count
        new_count=last_count+1
        Report.objects.filter(url=url).delete()
        if(last_update==today):
            Report.objects.create(url=url,updated=today,count=new_count)
            if(new_count>=25):
                Fraud.objects.create(url=url)
        else:
            last_update=last_update.split('-')
            f_date = date(int(last_update[2]),int(last_update[1]),int(last_update[0]))
            delta = x.date()-f_date
            if(delta.days<10):
                new_count=int(factor*last_count)+1
                Report.objects.create(url=url,updated=today,count=new_count)
                if(new_count>=24):
                    Fraud.objects.create(url=url)
            else:
                Report.objects.create(url=url,updated=today,count=1)
    else:
        Report.objects.create(url=url,updated=today,count=1)

    print("Reported successfully")
    data['report']=1
    return JsonResponse(data,safe=False)

def phis(request):
    x = datetime.datetime.now()
    today=str(x.day)+'-'+str(x.month)+'-'+str(x.year)

    data={}
    data['suggested_urls']=[]
    data['err']=0
    data['exceed']=0


    if request.COOKIES.get('id'):
        id=request.COOKIES['id']
        entity=list(Person.objects.filter(identity=id,updated=today,category='phising'))
        if(len(entity)>0):
            count=entity[0].count
            if(count>=5):
                data['exceed']=1
                print("Limit Exceeded",entity[0].identity,entity[0].updated,entity[0].count)
                return JsonResponse(data,safe=False)
            else:
                entity[0].count=count+1
                entity[0].save()
        else:
            Person.objects.filter(identity=id,category='phising').delete()
            Person.objects.create(identity=id,updated=today,category='phising',count=1)

    url=request.GET.get('p', '').lower()
    if(url[:4]!='http'):
        r=tldextract.extract(url)
        #https://www.youtube.com/
        url="https://"+r.subdomain+'.'+r.domain+'.'+r.suffix
    
    
    print("Entered here successfully",url)
    '''detector=Suggestions(url)
    if(detector.err==1):
        print("Some error occured")
        data['err']=1
        return JsonResponse(data,safe=False)
    detector.detect()
    if(detector.err==1):
        print("Some error occured")
        data['err']=1
        return JsonResponse(data,safe=False)

    detector.detect()
    data['suggested_urls']=detector.suggested_urls
    if(len(data['suggested_urls'])==0):
        print("Not a phising website")
    else:
        print("Phising website")
    return JsonResponse(data,safe=False)'''

    #print(os.getcwd())
    #classifier=pickle.load(open('rf_final.pkl', 'rb'))

    entity=list(Fraud.objects.filter(url=url))

    finder=Suggestions(url)
    if(finder.err==1):
        print("Some error occured")
        data['err']=1
        return JsonResponse(data,safe=False)
    finder.detect()
    if(finder.err==1):
        print("Some error occured")
        data['err']=1
        return JsonResponse(data,safe=False)

    if(len(entity)>0):
        print("Phising site DB")
        if(len(finder.suggested_urls)==0):
            data['suggested_urls'].append('https://www.google.com/')
        else:
            data['suggested_urls']=finder.suggested_urls
        return JsonResponse(data,safe=False)

    if(finder.found==1):
        print("Not a phising site SE")
        return JsonResponse(data,safe=False)
    
    extractor=Features(url)
    extractor.extract()
    if(extractor.err==1):
        print("Some error occured")
        data['err']=1
        return JsonResponse(data,safe=False)

    classifier = joblib.load('ML/rf_final.pkl')
    prediction=classifier.predict(extractor.features)[0]

    print("Prediction is",prediction)

    if(prediction!=-1):
        print("Phising website")
        #data['suggested_urls']=extractor.suggested_urls
        if(len(finder.suggested_urls)==0):
            data['suggested_urls'].append('https://www.google.com/')
        else:
            data['suggested_urls']=finder.suggested_urls
    else:
        print("Not phising website")  
    return JsonResponse(data,safe=False)

def check(request):
    urls=list(Url.objects.all())
    d={"urls":[]}
    for i in urls:
        d["urls"].append(i.main)
    
    return JsonResponse(d,safe=False)

def scan(request):
    main=request.GET.get('q1', '').lower()
    copy=request.GET.get('q2', '').lower()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }
    print("Hey I entered here",main,copy)
    data={}
    data['score']=0
    data['err']=0

    r=tldextract.extract(main)

    if(main[:5]!='https'):
        main='https://'+r.subdomain+'.'+r.domain+'.'+r.suffix

    r=tldextract.extract(copy)

    if(copy[:4]!='http'):
        copy='https://'+r.subdomain+'.'+r.domain+'.'+r.suffix

    original_text=''
    new_text=''

    for j in range(2):
        res=-1
        try:
            if(j==0):
                res=requests.get(main,headers=headers,timeout=3)
            else:
                res=requests.get(main,headers=headers,timeout=8)
            if(res):
                original_text=res.text
                break
            else:
                data['err']=1
                break

        except requests.exceptions.Timeout:
            if(j==1):
                data['err']=1
                break
            
        except:
            data['err']=1
            break

    if(data['err']==0):

        for j in range(2):
            res=-1
            try:
                if(j==0):
                    res=requests.get(copy,headers=headers,timeout=3)
                else:
                    res=requests.get(copy,headers=headers,timeout=8)
                if(res):
                    new_text=res.text
                    break
                else:
                    data['err']=1
                    break

            except requests.exceptions.Timeout:
                if(j==1):
                    data['err']=1
                    break
                
            except:
                data['err']=1
                break
        
    #data['score']=round(sim(new_text,original_text)*100,2)
    data['score']=round(similarity(new_text,original_text)*100,2)
    print(data['score'])
    if(data['err']==1):
        print("Something went wrong!!")
    return JsonResponse(data,safe=False)


def similar(request):
    x = datetime.datetime.now()
    data={}
    data['urls']=[]
    data['err']=0
    data['exceed']=0

    today=str(x.day)+'-'+str(x.month)+'-'+str(x.year)
    #print("Today is",today)
    if request.COOKIES.get('id'):
        id=request.COOKIES['id']
        entity=list(Person.objects.filter(identity=id,updated=today,category='branding'))
        if(len(entity)>0):
            count=entity[0].count
            if(count>=5):
                data['exceed']=1
                print("Limit Exceeded",entity[0].identity,entity[0].updated,entity[0].count)
                return JsonResponse(data,safe=False)
            else:
                entity[0].count=count+1
                entity[0].save()
        else:
            Person.objects.filter(identity=id,category='branding').delete()
            Person.objects.create(identity=id,updated=today,category='branding',count=1)
    
    
    responses=[]
    workers=300
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    }

    url=request.GET.get('q', '').lower()
    p=int(request.GET.get('p', ''))
    
    r=tldextract.extract(url)

    if(url[:5]!='https'):
        if(r.subdomain==''):
            url='https://www'+'.'+r.domain+'.'+r.suffix
        else:
            url='https://'+r.subdomain+'.'+r.domain+'.'+r.suffix

    print("Hey I entered here",url,p)
    urls=list(Url.objects.filter(main=url))
    #print(urls)
    flag=0
    if(len(urls)>0):
        
        last_update=urls[0].updated.split('-')
        f_date = date(int(last_update[2]),int(last_update[1]),int(last_update[0]))
        delta = x.date()-f_date
        if(delta.days<10):
            flag=1
            print("It is there in db")
            for url in urls:
                if(url.score>=p):
                    data['urls'].append({'url':url.similar,'similarity':url.score})
            #return JsonResponse(data,safe=False)


    if(flag==0):
        Url.objects.filter(main=url).delete()
        original_text=''
        res=-1
        print(headers)
        for j in range(2):
            try:
                if(j==0):
                    res=requests.get(url,headers=headers,timeout=3)
                else:
                    res=requests.get(url,headers=headers,timeout=8)
                if(res):
                    original_text=str(res.text)
                else:
                    data['err']=1
                    break
            
            except requests.exceptions.Timeout:
                if(j==1):
                    data['err']=1
                    break
            except:
                data['err']=1
                break

        if(original_text!=''):
        
            #print(original_text)

            g=Domain_generator(url)
            possible_urls=sorted(g.generate_urls())

            print("Search space",len(possible_urls))

            for i in possible_urls:
                responses.append(-1)
                

            #print("Hey there")

            threads = list()
            for index in range(workers):
                x = threading.Thread(target=thread_function, args=(index,possible_urls,responses,original_text,workers,headers,))
                threads.append(x)
                x.start()

            for thread in threads:
                thread.join()
            
            j=1
            for i in range(len(possible_urls)):
                if(responses[i]!=-1):
                    Url.objects.create(main=url,similar=possible_urls[i],score=responses[i],updated=today)
                    #if(find(data['urls'],possible_urls[i])==0):
                    if(responses[i]>=p):
                        data['urls'].append({'url':possible_urls[i],'similarity':round(responses[i],2)})

            if(len(data['urls'])==0):
                Url.objects.create(main=url,similar=url,score=100,updated=today)
                if(p==100):
                    data['urls'].append({'url':url,'similarity':100})

        else:
            data['err']=1
            print("Wrong supplied url")
    data['urls']=sorted(data['urls'], key=lambda k: k['similarity'],reverse=True) 
    print('Finished')

    return JsonResponse(data,safe=False)

            
