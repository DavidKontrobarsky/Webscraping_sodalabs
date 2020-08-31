#encoding=utf-8
import os
import platform
if platform.system() == "Windows":
    try:
        import requests
    except ImportError:
        os.system('python -m pip install requests')
        os.system('python -m pip install parsel')
else:
    try:
        import requests
    except ImportError:
        os.system('python3 -m pip install requests')
        os.system('python3 -m pip install parsel')



import requests
from parsel import Selector
import csv

base_headers = {
    "Host": "elephrame.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0",
    "Accept": "text/html, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://elephrame.com",
    "Connection": "keep-alive",
    "Referer": "https://elephrame.com/textbook/BLM/chart",
    "Cookie": "PHPSESSID=d38573013ee520a0b637248882150a10; _ga=GA1.2.1063371836.1597380961; _gid=GA1.2.1619986680.1597380961; _gali=blm-results; att=y",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "Trailers",
}

if __name__=="__main__":

    if 'elephram.csv' not in os.listdir(os.getcwd()):
        with open("elephram.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow(['location','date','subject','participants','time','description','sources'])

    for page in range(1,225):
        r = requests.post(
            "https://elephrame.com/gather",
            headers={**base_headers,},
            data={"page": str(page), "contentType": "blm", "search": ""},
        )

        datas = Selector(text=r.text).xpath('.//*[@class="item chart"]').extract()
        for data in datas:
            sel = Selector(text=data)
            location = sel.xpath('.//*[@class="item-protest-location"]/text()').extract_first()
            date = sel.xpath('.//*[@class="protest-start"]/text()').extract_first()
            subject = sel.xpath('.//*[@class="item-protest-subject"]/text()').extract_first()
            participants = sel.xpath('.//*[@class="item-protest-participants"]/text()').extract_first()
            time = sel.xpath('.//*[@class="item-protest-time"]/text()').extract_first()
            description = sel.xpath('.//*[@class="item-protest-description"]/text()').extract_first()
            try:
                sources = ' '.join(sel.xpath('.//*[@class="item-protest-url"]//text()').extract())
            except:
                sources = ''

            with open("elephram.csv","a") as f:
                writer = csv.writer(f)
                writer.writerow([location,date,subject,participants,time,description,sources])
                print([location,date,subject,participants,time,description,sources])



