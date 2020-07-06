import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.fr/emplois?q=python&l=Paris%20(75)&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all('a')  # links is printed out as List
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find("h2", {"class": "title"}).find('a')["title"]
    company = html.find("span", {"class": "company"})
    if company:
      company_anchor = company.find("a")
      if company_anchor is not None:
          company = str(company_anchor.string)
      else:
          company = str(company.string)
      company = company.strip()
    else:
      company = None  
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    # job_advn = html["data-empn"]
    job_vjk = html["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://www.indeed.fr/voir-emploi?jk={job_vjk}"
    }


def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping INDEED: Page: {page+1}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        job = extract_job(result)
        jobs.append(job) 
  return jobs


def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs

