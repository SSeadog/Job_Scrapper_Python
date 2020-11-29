import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    last_page_span = soup.find("span", {"class": "pgTotal"})
    if last_page_span is not None:
        last_page = last_page_span.string
    else:
        last_page = 1
    print(last_page)
    return int(last_page)


def extract_job(html):
    if html.find("a", {"class": "title"}) is not None:
        title = html.find("a", {"class": "title"})["title"]
        company = html.find("a", {"class": "name"})["title"]
        location = html.find("p", {"class": "option"}).find(
            "span", {"class": "long"}).string
        job_id = html["data-gno"]
        link = f"http://www.jobkorea.co.kr/Recruit/GI_Read/{job_id}"
        return {"title": title, "company": company, "location": location, "link": link}
    else:
        return {}


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping jk: Page {page}")
        result = requests.get(f"{url}&Page_No={page + 1}")
        soup = BeautifulSoup(result.text, "html.parser")
        if soup.find("div", {"class": "list-default"}) is None:
            return []
        results = soup.find("div", {"class": "list-default"}).find_all("li")
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"http://www.jobkorea.co.kr/Search/?stext={word}&careerType=1&edu=0&tabType=recruit"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
