from bs4 import BeautifulSoup
from urllib.request import Request, build_opener, HTTPCookieProcessor
from urllib.parse import urlencode
from http.cookiejar import MozillaCookieJar
import re, time, sys, urllib

def get_num_results(keyword, start_year, end_year):

    # Reading the html of webpage
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
    query_params = { 'q' : keyword, 'as_ylo' : start_year, 'as_yhi' : end_year}
    url = "https://scholar.google.com/scholar?as_vis=1&hl=en&as_sdt=1,5&" + urllib.parse.urlencode(query_params)
    opener = build_opener()
    request = Request(url=url, headers={'User-Agent': user_agent})
    handler = opener.open(request)
    html = handler.read() 

    # Parsing html with soup
    soup = BeautifulSoup(html, 'html.parser')

    # find line 'About x results (y sec)
    div_results = soup.find("div", {"id": "gs_ab_md"}) 

    if div_results != None:

        res = re.findall(r'(\d+).?(\d+)?.?(\d+)?\s', div_results.text) 
        
        if res == []:
            num_results = '0'
            success = True
        else:
            num_results = ''.join(res[0])
            success = True

    else:
        success = False
        num_results = 0

    return num_results, success

def get_range(keyword, start_year, end_year):

    fp = open("count_keyword_"+keyword+".csv", 'w')
    fp.write("year,results\n")
    print("year,results")

    for year in range(start_year, end_year + 1):

        num_results, success = get_num_results(keyword, year, year)
        if not(success):
            print("Error while fetching from GScholar.")
            break
        year_results = "{0},{1}".format(year, num_results)
        print(year_results)
        fp.write(year_results + '\n')
        time.sleep(0.8)

    fp.close()

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python keyword_count.py '<keyword>' <start year> <end year>")
        
    else:
        keyword = sys.argv[1]
        start_year = int(sys.argv[2])
        end_year = int(sys.argv[3])
        html = get_range(keyword, start_year, end_year)