import requests
from bs4 import BeautifulSoup


def scrape_by_keyword(keyword):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    query_params = { 'q' : keyword, 'as_ylo' : 2012, 'as_yhi' : 2022}
    url = "https://scholar.google.com/scholar?as_vis=1&hl=en&as_sdt=1,5&" + urllib.parse.urlencode(query_params)

    response=requests.get(url,headers=headers)

    #error of fetching keywords that do not exist
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ')

    doc = BeautifulSoup(response.text,'html.parser')
