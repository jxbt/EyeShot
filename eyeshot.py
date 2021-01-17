#!/usr/bin/python3

import sys
import getopt
import os
import requests
import time
import threading
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import re
import urllib3
from requests.adapters import HTTPAdapter
import random

urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)


logo = r"""

  _______  ___  ___  _______   ________  __    __     ______  ___________  
 /"     "||"  \/"  |/"     "| /"       )/" |  | "\   /    " \("     _   ") 
(: ______) \   \  /(: ______)(:   \___/(:  (__)  :) // ____  \)__/  \\__/  
 \/    |    \\  \/  \/    |   \___  \   \/      \/ /  /    ) :)  \\_ /     
 // ___)_   /   /   // ___)_   __/  \\  //  __  \\(: (____/ //   |.  |     
(:      "| /   /   (:      "| /" \   :)(:  (  )  :)\        /    \:  |     
 \_______)|___/     \_______)(_______/  \__|  |__/  \"_____/      \__|     
                                                                           


                        Coded By Jxbt

"""


usage = """
Usage:
    eyeshot [options]


Flags:

    -f, --file                 the file containing URLS to screenshot and collect info about (required)

    -o, --outdir               the output folder path (required)

    -t, --threads              the amount of threads (optional) (default is 1)

    -h, --help                 show the help menu (optional)

    -v, --verbose              verbose mode (optional)

    --cc                       specify which responses/pages you want to screenshot and collect info about according to the response status code (optional)

    --dc                       specify which responses/pages you don't want to screenshot and collect info about according to the response status code (optional)

    --lt                       page loading timeout in seconds before taking the screenshot (optional) (default is 90)
    
    --rt                       request timeout in seconds (optional) (default is 60)

    --cl                       collect info about the URLs that you want to screenshot and store it in 00_meta.json (optional) (default is False)



Examples:

    1- eyeshot -f ~/Desktop/urls.txt -o  ~/Desktop/shots -t 10
    
    2- eyeshot -f ~/urls.txt -o ~/shots  -t 15 --cc 2xx,404

    3- eyeshot -f ~/urls.txt -o ~/shots -t 10 --dc 4xx,5xx,302

    4- eyeshot -f ~/urls.txt -o ~/shots -t 10 --lt 50 --rt 30

    5- eyeshot -f ~/urls.txt -o ~/shots -t 10 --lt 50 --cl -v
"""


url_list_file = ""
threads_num = 1
output_dir = ""
url_list =  []

cap1_urls_list = []
cap2_urls_list = []

json_meta = []   
verbose = False
collect_info = False

page_load_timeout = 90  
timeout = 60
max_ret = 3


user_agents = ["Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36","Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"]

statuscodes_y = [] 
statuscodes_n = [] 

argv = sys.argv[1:]
opts = []
args = []




try:
    opts,args = getopt.getopt(argv,"f:o:t:vh",["file=","outdir=","threads=","cc=","dc=","lt=","rt=","cl","verbose","help"])

except Exception as ex:
    print(logo)
    print(usage)
    sys.exit(1)




for opt,arg in opts:

    if "-h" in opt or "--help" in opt:
        print(usage)
        sys.exit(0)
    
    elif "-v" in opt or "--verbose" in opt:
        verbose = True
    
    elif "-t" in opt or "--threads" in opt:
        threads_num = int(arg)
    
    elif "-f" in opt or "--file" in opt:
        url_list_file = arg
    
    elif "-o" in opt or "--outdir" in opt:
        output_dir = arg
    
    elif "--cc" in opt:

        pattern = re.compile(r"\dxx")

        temp_lst = str(arg).split(",")

        if len(temp_lst) > 0:

            for st in temp_lst:
                matches = pattern.findall(st)

                if  len(matches) > 0:
                    st_inital = str(matches[0][0])+"00"
                    st_inital = int(st_inital)

                    st_range = range(st_inital,st_inital+100)

                    for st_r in st_range:
                        statuscodes_y.append(st_r)
                else:
                    st_int = int(st)
                    statuscodes_y.append(st_int)
        else:
            pass
    
    elif "--dc" in opt:

        temp_lst = str(arg).split(",")

        if len(temp_lst) > 0:
            pattern = re.compile(r"\dxx")

            for st in temp_lst:
                matches = pattern.findall(st)

                if len(matches) > 0:

                    st_inital = str(matches[0][0])+"00"
                    st_inital = int(st_inital)

                    st_range = range(st_inital,st_inital+100)

                    for st_r in st_range:
                        statuscodes_n.append(st_r)
                else:

                    st_int = int(st)
                    statuscodes_n.append(st_int)
        else:
            pass
    
    elif "--lt" in opt:
        page_load_timeout = int(arg)

    elif "--rt" in opt:
        timeout = int(arg)
    
    elif "--cl" in opt:
        collect_info = True

        
    else:
        pass



print(logo)


if threads_num == 0  or url_list_file == "" or output_dir == "":
    
    print(usage)
    sys.exit(1)



if(os.path.isdir(output_dir)):
    pass
else:
    os.mkdir(output_dir)




if ".json" in url_list_file:

    with open(url_list_file,"r") as f:
        json_data = json.load(f)
        for key,val in json_data:
            url_list.append(val)
else:
    with open(url_list_file,"r") as f:

        line = f.readline()
        
        while(len(line) > 0):
            url_list.append(str(line))
            line = f.readline()




def meta_gen(url,ex1_signal):

    if ex1_signal:
        return
    

    s = requests.Session()
    s.mount(url,HTTPAdapter(max_retries=max_ret))

    if len(statuscodes_y) > 0:

        try:

            url_status_code = s.get(url,headers={"User-Agent":user_agents[random.randint(0,4)]},verify=False,timeout=timeout).status_code

            if url_status_code in statuscodes_y:
                pass
            else:
                s.close()
                return
        except Exception as ex:
            s.close()
            return
        
    elif len(statuscodes_n) > 0:

        try:
            url_status_code = s.get(url,headers={"User-Agent":user_agents[random.randint(0,4)]},verify=False,timeout=timeout).status_code

            if url_status_code in statuscodes_n:
                s.close()
                return
            else:
                pass
        
        except Exception as ex:
            s.close()
            return
        
        else:
            pass
    
    try:
        resp = s.get(url,headers={"User-Agent":user_agents[random.randint(0,4)]},verify=False,timeout=timeout)
        st_code = resp.status_code
        resp_text = resp.text

        html_content = BeautifulSoup(resp_text,"html.parser")
        try:
            els = html_content.find_all("title")
            title = str((els[0]).text)
        except Exception as ex:
            title = "null"

        domain = str(url).replace("http:","").replace("https:","").replace("/","").replace("\n","")
        obj = {"status_code":st_code,"title":title,"url":url,"image":"( {} ).png".format(domain)}
        json_meta.append(obj)

        s.close()

       
    
    except Exception as ex:
        s.close()
    



def screen_shoter(url,ex2_signal):

    if ex2_signal:
        return


    s = requests.Session()
    s.mount(url,HTTPAdapter(max_retries=max_ret))
    

    if len(statuscodes_y) > 0:

        try:
            url_status_code = requests.get(url,headers={"User-Agent":user_agents[random.randint(0,4)]},verify=False,timeout=timeout).status_code

            if url_status_code in statuscodes_y:
                pass
            else:
                if verbose:
                    print(f'[+] taking screenshot for {url} (ignored "{str(url_status_code)} status-code").\n')

                s.close()
                return
        except Exception as ex:
            if verbose:
                print(f'[+] taking screenshot for {url} (failed "timeout").\n')
            s.close()
            return
    
    elif len(statuscodes_n) > 0:

        try:
            url_status_code = requests.get(url,headers={"User-Agent":user_agents[random.randint(0,4)]},verify=False,timeout=timeout).status_code

            if url_status_code in statuscodes_n:
                if verbose:
                    print(f'[+] taking screenshot for {url} (ignored "{str(url_status_code)} status-code").\n')

                s.close
                return
            else:
                pass
        except Exception as ex:
            if verbose:
                print(f'[+] taking screenshot for {url} (failed "timeout").\n')
            s.close()
            return
    
    else:
        s.close()
    
    
    os.environ["MOZ_HEADLESS"] = '1'

    profile = webdriver.FirefoxProfile()
    profile.accept_untrusted_certs = True

    driver = webdriver.Firefox(firefox_binary="binPath",firefox_profile=profile)
    
    driver.set_page_load_timeout(page_load_timeout)

    
    
    try:
        
        driver.get(url)

        domain = str(url).replace("http:","").replace("https:","").replace("/","")
        driver.save_screenshot("{}/( {} ).png".format(output_dir,domain))
        driver.quit()

        

        if verbose:
            print(f"[+] taking screenshot for {url} (succeed).\n")
    
    except Exception as ex:
        driver.quit()

        if verbose:
            print(f'[+] taking screenshot for {url} (failed "timeout").\n')
    





print("\neyeshot started ...\n\n")


iu_1 = 0
iu_2 = 0

while iu_1 < len(url_list) and iu_2 < len(url_list):

    threads_1 = []
    threads_2 = []
    
    url = ""
    
    try:
        url = url_list[iu_1]
    except Exception as ex:
        break
    
    if collect_info == True:

        for _ in range(threads_num):


            ex1_signal = False

            try:
                url = url_list[iu_1]
            except Exception as ex:
                pass

            if url in cap1_urls_list:
                ex1_signal = True
            else:
                ex1_signal = False

            t = threading.Thread(target=meta_gen,args=[url.replace("\n",""),ex1_signal])
            t.start()
            threads_1.append(t)
            cap1_urls_list.append(url)
            
            iu_1 += 1
            
        for thread in threads_1:
            thread.join()



    url = url_list[iu_2]
    for _ in range(threads_num):

        ex2_signal = False

        try:
            url = url_list[iu_2]
        except Exception as ex:
            pass

        if url in cap2_urls_list:
            ex2_signal = True
        else:
            ex2_signal = False
        
        t = threading.Thread(target=screen_shoter,args=[url.replace("\n",""),ex2_signal])
        t.start()
        threads_2.append(t)
        cap2_urls_list.append(url)
        
        iu_2 +=1

    for thread in threads_2:
        thread.join()
    
    
    time.sleep(1)




if collect_info == True:

    with open("{}/00_meta.json".format(str(output_dir)),"w") as f:
        json.dump(json_meta,f,indent=2)




print("\nDone!")