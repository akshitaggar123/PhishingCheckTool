import requests

def thread_function(index,workers,work_load,possible_urls,original_text,responses):
    end=(index+1)*work_load
    if(index==workers-1):
        end=len(possible_urls)

    
    for i in range(index*work_load,end):
        for j in range(2):
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
                pass
            
            except:
                break