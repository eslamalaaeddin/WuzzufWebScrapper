import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_titles = []
company_names = []
locations = []
job_skills = []
links = []
salary = []
responsibilities = []
date = []
page_num = 0

while True:
    result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")
    # to get the markup
    src = result.content
    # to beautify the content
    soup = BeautifulSoup(src, "lxml")

    page_limit = int(soup.find("strong").text)

    if page_num > page_limit // 15:
        print("pages ended")
        break

    job_titles_with_markup = soup.find_all("h2", {"class": "css-m604qf"})
    company_names_with_markup = soup.find_all("a", {"class": "css-17s97q8"})
    locations_with_markup = soup.find_all("span", {"class": "css-5wys0k"})
    job_skills_with_markup = soup.find_all("div", {"class": "css-y4udm8"})
    posted_new_with_markup = soup.find_all("div", {"class": "css-4c4ojb"})
    posted_old_with_markup = soup.find_all("div", {"class": "css-do6t5g"})

    posted = [*posted_new_with_markup, *posted_old_with_markup]
    # get the text
    for i in range(len(job_titles_with_markup)):
        job_titles.append(job_titles_with_markup[i].text)
        links.append(job_titles_with_markup[i].find("a").attrs['href'])
        company_names.append(company_names_with_markup[i].text)
        locations.append(locations_with_markup[i].text)
        job_skills.append(job_skills_with_markup[i].text)
        date.append(posted[i].text)

    page_num += 1
    print("Page switched")

for link in links:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    salaries = soup.find("div", {"class": "matching-requirement-icon-container", "data-toggle": "tooltip",
                                 "data-placement": "top"})
    salary.append(salaries.text.strip())
    requirements = soup.find("span", {"itemprop": "responsibilities"}).ul
    respon_text = ""
    for li in requirements.find_all("li"):
        respon_text += li.text + "| "
    responsibilities.append(respon_text)

# build CSV file
file_list = [job_titles, company_names, date, locations, job_skills, links, salary, responsibilities]
exported = zip_longest(*file_list)
with open("/Users/IslamAlaaEddin/Desktop/jobs.csv", "w") as myFile:
    writer = csv.writer(myFile)
    writer.writerow(["job title", "company name", "date", "location", "skills", "links", "salary", "responsibilities"])
    writer.writerows(exported)
