import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode



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

    return doc

'''
    Helper functions to retrieve metadata
'''

# this function for the extracting information of the tags
def get_tags(doc):
  paper_tag = doc.select('[data-lid]')
  cite_tag = doc.select('[title=Cite] + a')
  link_tag = doc.find_all('h3',{"class" : "gs_rt"})
  author_tag = doc.find_all("div", {"class": "gs_a"})

  return paper_tag,cite_tag,link_tag,author_tag


# this function for the extracting information of the tags
def get_tags(doc):
  paper_tag = doc.select('[data-lid]')
  cite_tag = doc.select('[title=Cite] + a')
  link_tag = doc.find_all('h3',{"class" : "gs_rt"})
  author_tag = doc.find_all("div", {"class": "gs_a"})

  return paper_tag,cite_tag,link_tag,author_tag


# it will return the number of citation of the paper
def get_citecount(cite_tag):
  cite_count = []
  for i in cite_tag:
    cite = i.text
    if i is None or cite is None:  # if paper has no citatation then consider 0
      cite_count.append(0)
    else:
      tmp = re.search(r'\d+', cite) # its handle the None type object error and re use to remove the string " cited by " and return only integer value
      if tmp is None :
        cite_count.append(0)
      else :
        cite_count.append(int(tmp.group()))

  return cite_count


# it will return the number of citation of the paper
def get_citecount(cite_tag):
  cite_count = []
  for i in cite_tag:
    cite = i.text
    if i is None or cite is None:  # if paper has no citatation then consider 0
      cite_count.append(0)
    else:
      tmp = re.search(r'\d+', cite) # its handle the None type object error and re use to remove the string " cited by " and return only integer value
      if tmp is None :
        cite_count.append(0)
      else :
        cite_count.append(int(tmp.group()))

  return cite_count

  # function for the getting autho , year and publication information
def get_author_year_publi_info(authors_tag):
  years = []
  publication = []
  authors = []
  for i in range(len(authors_tag)):
      authortag_text = (authors_tag[i].text).split()
      year = int(re.search(r'\d+', authors_tag[i].text).group())
      years.append(year)
      publication.append(authortag_text[-1])
      author = authortag_text[0] + ' ' + re.sub(',','', authortag_text[1])
      authors.append(author)
  
  return years , publication, authors


# creating final repository
paper_repos_dict = {
                    'Paper Title' : [],
                    'Year' : [],
                    'Author' : [],
                    'Citation' : [],
                    'Publication' : [],
                    'Url of paper' : [] }

# adding information in repository
def add_in_paper_repo(papername,year,author,cite,publi,link):
  paper_repos_dict['Paper Title'].extend(papername)
  paper_repos_dict['Year'].extend(year)
  paper_repos_dict['Author'].extend(author)
  paper_repos_dict['Citation'].extend(cite)
  paper_repos_dict['Publication'].extend(publi)
  paper_repos_dict['Url of paper'].extend(link)

  return pd.DataFrame(paper_repos_dict)


for i in range (0,10):
    
 
  doc = scrape_by_keyword('aiops')

  # function for the collecting tags
  paper_tag,cite_tag,link_tag,author_tag = get_tags(doc)
  
  # paper title from each page
  papername = get_papertitle(paper_tag)

  # year , author , publication of the paper
  year , publication , author = get_author_year_publi_info(author_tag)

  # cite count of the paper 
  cite = get_citecount(cite_tag)

  # url of the paper
  link = get_link(link_tag)

  # add in paper repo dict
  final = add_in_paper_repo(papername,year,author,cite,publication,link)
  
  # use sleep to avoid status code 429
  sleep(30)