import requests
from bs4 import BeautifulSoup

LIMIT = 50


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})

    if pagination is not None:
        links = pagination.find_all('a')
        pages = []
        for link in links[:-1]:
            pages.append(int(link.string))

        max_page = pages[-1]
    else:
        max_page = 1

    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("div", {
        "class": "sjcl"
    }).find("span", {"class": "company"})
    if company:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = company_anchor.string
        else:
            company = company.string
        if company is not None:
            company = company.strip()
    else:
        company = None
    location = html.find("div", {
        "class": "sjcl"
    }).find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        "title":
        title,
        "company":
        company,
        "location":
        location,
        "link":
        f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: Page {page}")
        result = requests.get(f"{url}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={word}&l=%EA%B2%BD%EA%B8%B0%EB%8F%84&limit={LIMIT}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
