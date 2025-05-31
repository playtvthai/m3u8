import requests,re,json
from bs4 import BeautifulSoup
from urllib.parse import urlparse,unquote,parse_qs
from urllib.parse import urljoin
from datetime import datetime
from clint.textui import colored

#web_movie = input(colored.green("\n กรุณาใส่ URL :"))
#web_movie = "https://www.24-hd.com/%e0%b8%ab%e0%b8%99%e0%b8%b1%e0%b8%87%e0%b9%83%e0%b8%ab%e0%b8%a1%e0%b9%88-2023/"
#web_movie = "https://www.24-hd.com/%e0%b8%ab%e0%b8%99%e0%b8%b1%e0%b8%87%e0%b8%81%e0%b8%b2%e0%b8%a3%e0%b9%8c%e0%b8%95%e0%b8%b9%e0%b8%99/"

web_movie = "https://www.24-hdd.com/netflix/"

#####  ใส่ที่อยู่ที่ต้องการเก็บตรง f_path  #################################################################
f_path = r"D:\playlist\\"
#f_path = r"D:\python\24-hd_on\\"
#######################################################################################
date = datetime.now().strftime("%d")
mo = datetime.now().strftime("%m")
month = ['','มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม']
timeday = f'วันที่ {date} {month[int(mo)]} {int(datetime.now().strftime("%Y"))+543}'
#################################################
fname = unquote(urlparse(web_movie).path.strip('/').split('/')[-1])
wname = unquote(urlparse(web_movie).netloc.strip('.').split('.')[-2])
f_w3u = wname + "_" +fname+ ".w3u"
f_m3u = wname + "_" +fname+ ".m3u"
#################################################
W_W3U = 1       # 1 = เขียน ไฟล์ w3u 
W_M3U = 1       # 1 = เขียน ไฟล์ m3u 
needHD = 1      #
#################################################
M_f = 1         #ห้ามแก้
#################################################
aseries = """{
    "name": "",
    "author": "",
    "info": "ความสำเร็จไม่ใช่จุดสิ้นสุด ความล้มเหลวไม่ใช่เรื่องร้ายแรง ความกล้าหาญที่จะทำต่อไปต่างหากที่สำคัญ",
    "image": "",
    "key": []}"""
#################################################



headers = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
from selenium import webdriver
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument("User-Agent=" + headers)
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

################################################


jseries = json.loads(aseries)
jseries['groups'] = jseries.pop('key')
parsed_uri = urlparse(web_movie)
referer = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
sess = requests.Session()
sess.headers.update({'User-Agent': headers, 'referer': referer})


driver.get(web_movie)
soup = BeautifulSoup(driver.page_source, 'lxml')

#driver.get(web_movie)
#soup = BeautifulSoup(driver.page_source, 'lxml')
page = soup.find("nav", {"class": "navigation pagination"})
if page is not None:
    page_numbers = page.find_all("a", {"class": "page-numbers"})
    if page_numbers:
        pmax = int(page_numbers[-2].text)
    else:
        pmax = 1
else:
    pmax = 1

pcurrent = 1
#pmax = 1
jseries['name'] = ppname = soup.find("div", {"class": "movietext"}).text.strip()
jseries['image'] = "https://www.24-hdd.com/wp-content/uploads/2022/08/logo24.png"
jseries['author'] = jseries['author'] + timeday
if jseries['name'] == "แนะนำหนังใหม่":
    jseries['name'] = "ดูหนังออนไลน์ หนังใหม่ HD ฟรี"
if ppname == "แนะนำหนังใหม่":
    ppname = "ดูหนังออนไลน์ หนังใหม่ HD ฟรี"


def find_hd(elink):
    purl = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
    view_page = sess.get(elink)
    regex_pattern = re.compile('RESOLUTION=(.+)*\n(.+[-a-zA-Z0-9()@:%_\+.~#?&//=])')
    result = regex_pattern.findall(str(view_page.text))
    if result: 
        try:
            result1 = result[-1]
            purl2 = result1[-1]
        except:
            purl2 = result[-1][-1]  
        purl2 = re.sub(r'^/', '', purl2)
        elink = purl + purl2
    return elink
def edit_link(elink):
    if elink != "https://www.24-hdd.com/api/fileprocess.html":
        try:
            cid = parse_qs(urlparse(elink).query)['id'][0]
        except:
            print()
        purl = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elink))
        if re.search('main.24playerhd.com',elink):
            try:
                backup = parse_qs(elink)['backup'][0]
            except:
                backup = 0
            try:
                ptype = parse_qs(elink)['ptype'][0]
            except:
                ptype = 0
            if backup == 1:
                elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
            else:
                if ptype == 2:
                    elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
                else:
                    elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
        if re.search('xxx\.77player\.xyz',elink):
            try:
                ptype = parse_qs(elink)['ptype'][0]
            except:
                ptype = 0
            if ptype == 2:
                elink = purl + 'newplaylist/' + cid + '/' + cid + '.m3u8'
            else:
                elink = purl + 'autoplaylist/' + cid + '/' + cid + '.m3u8'
    else:
        elink = ""
    return elink

pbak = web_movie
for num in range(int(pcurrent), int(pmax)+1):
    if num == 1:
        plink = pbak = web_movie
    else:
        plink = "page/%s" % (num)
        plink = pbak = web_movie + plink
        driver = webdriver.Chrome(options=options) #เปิด Chrome ใหม่
        driver.get(plink)
        soup = BeautifulSoup(driver.page_source, 'lxml')



    eprint = "หน้า [%s/%s] %s" % (num,pmax,plink)
    print(eprint)

    articles = soup.find_all("div", class_="box")
    smax = len(articles)

    for i, article in enumerate(articles, start=1):
        url = article.find("a")['href']
        pname = article.find("div", {"class": "p2"}).text.strip()
        try:
            ppic = article.find("div", {"class": "box-img"}).find("img")["data-lazy-src"]
        except:
            ppic = article.find("div", {"class": "box-img"}).find("img")["src"]
        ppic = ppic.replace('-187x269','')
        try:
            pinfo = article.find("span", {"class": "EP"}).text.strip()
            pinfo = pinfo.replace("\n"," ")
        except:
            pinfo = article.find("div", {"class": "p1"}).text.strip()
            pinfo = pinfo.replace("\n"," ")
        eprint = "%s\n[หน้า : %s/%s เรื่องที่ : %s/%s] %s" % (ppname,num,pmax,i,smax,pname)
        merror = " >>> ค้นหา link %s ไม่เจอ <<< " % (pname)
        print(eprint)
        jseries['groups'].append({"name":pname,"info":pinfo,"image":ppic,"stations":[]})
        #driver.quit()
        driver = webdriver.Chrome(options=options) #เปิด Chrome ใหม่
        driver.get(url)
        soup_video = BeautifulSoup(driver.page_source, 'lxml')
        lang_select = soup_video.find(id='Lang_select')

        try:
            default_option = lang_select.find_all('option')
        except:
            print(colored.red(merror))
            continue
            #exit()
        for l, link in enumerate(default_option, start=1):
            default_option = link['value']
            tsub = default_option
            if tsub == "Thai":
                tsub = tsub.replace("Thai","พากย์ไทย")
            if tsub == "Sound Track":
                tsub = tsub.replace("Sound Track","ซับไทย")
            #default_value = default_option['value']
            lsub = soup_video.find_all(class_='halim-episode')
            for J, links in enumerate(lsub, start=1):
                if J ==3:
                    continue
                if J ==4:
                    continue
                data_post_id = links.find('span')['data-post-id']
                data_episode = links.find('span')['data-episode']
                data_server = links.find('span')['data-server']
                data_position = links.find('span')['data-embed']
                pnonce = links.find('span')['data-type']
                data = {
                    'action': 'halim_ajax_player',
                    'nonce': pnonce,
                    'episode': data_episode,
                    'postid': data_post_id,
                    'lang': default_option,
                    'server': data_server
                }
                home_page = sess.post("https://api.24-hdd.com/get.php", data=data)
                soup = BeautifulSoup(home_page.content, "lxml")
                try:
                    elink = soup.find("iframe")['src']
                except:
                    continue
                if elink == "": continue
                if elink == "https://www.24-hdd.com/api/fileprocess.html": continue
                if "https://waaw.to" in elink: continue
                if "https://face" in elink: continue
                if ".123players" in elink: continue
                if "https://www.fembed.com/" in elink: continue
                elink = edit_link(elink)
                if needHD:
                    try:
                        elink = find_hd(elink)
                    except:
                        print()
                print("         ลิ้งค์ : ",(tsub),(colored.blue(elink)))
                g1 = len(jseries['groups']) - 1
                jseries['groups'][g1]['stations'].append({"name":pname,"info":tsub,"image":ppic,"url":elink,"referer":referer})
                if W_M3U:
                    if M_f:
                        with open(f_path+f_m3u, 'w',encoding='utf-8') as f:
                            f.write("#EXTM3U\n")
                            f.close()
                            M_f = 0
                    with open(f_path+f_m3u, 'a',encoding='utf-8') as f:
                        f.write(f'#EXTINF:-1 tvg-logo="{ppic}" group-title="เจียว เจียว จะดู {fname}" ,{pname} {tsub}\n')
                        f.write(f'#EXTVLCOPT:http-referer={referer}\n')
                        f.write(f'{elink}\n')
                        f.close()   
                if W_W3U:   
                    with open(f_path+f_w3u, 'w',encoding='utf-8') as f:
                        json.dump(jseries, f, indent=1, ensure_ascii=False)

print("------ดึงเสร็จสิ้น------")
if not W_W3U:
    pass
else:
    out  = f_path+f_w3u
    re.sub(r' ', '', out)
    out  = "บันทึกไฟล์ W3u ที่ " + out
    print(out)
if W_M3U:
    out  = f_path+f_m3u
    re.sub(r' ', '', out)
    out  = "บันทึกไฟล์ M3u ที่ " + out
    print(out)