from bs4 import BeautifulSoup
import requests
import string
import re
import json

letters = list(string.ascii_lowercase)
base_url = "https://www.linkedin.com/directory/topics-"

for letter in letters[2:]:
     letter_url = base_url + letter + "/"
     r = requests.get(letter_url)
     soup = BeautifulSoup(r.text)

     section_last = soup.find("div", {"class": "section last"})
     content = section_last.find_all("li", {"class": "content"})
     for con in content:
         letter_page_url = con.find("a")
         print(letter_page_url)
         if letter_page_url.has_attr('href'):
            r2 = requests.get(letter_page_url['href'])
            sub_soup = BeautifulSoup(r2.text)
            sub_section_last = sub_soup.find("div", {"class": "section last"})
            sub_content = sub_section_last.find_all("li", {"class": "content"})
            for sub_con in sub_content:
                topic_url = sub_con.find("a")
                topic = {}
                topic['name'] = topic_url.getText()
                if topic_url.has_attr('href'):
                    r3 = requests.get(topic_url['href'])
                    topic_soup = BeautifulSoup(r3.text)
                    if r3.status_code != 404:
                        member_count_text = (topic_soup.find("span",{"class": "member-count"})).getText()
                        topic['count'] = int(''.join(filter(str.isdigit, member_count_text)))
                        if topic_soup.find_all("li", {"class": "stat"}):
                            stats_list = topic_soup.find_all("li", {"class": "stat"})
                            for stat in stats_list:
                                if (stat.find("h3", {"class": "stats-text-header"})).getText() == "Top companies":
                                    top_companies = stat.find_all("li", {"class": "stat-text"})
                                    companies = {}
                                    for company in top_companies:
                                        company_regex = re.findall('(.*)\s\-\s([\d\,]*)', company.getText())[0]
                                        companyName = company_regex[0]
                                        companyNumber = int(company_regex[1].replace(',',''))
                                        companies[companyName] = companyNumber
                                    topic['companies'] = companies
                                if (stat.find("h3", {"class": "stats-text-header"})).getText() == "Top skills":
                                    top_skills = stat.find_all("li", {"class": "stat-text"})
                                    skills = {}
                                    for skill in top_skills:
                                        skill_regex = re.findall('(.*)\s\-\s([\d\,]*)', skill.getText())[0]
                                        skillName = skill_regex[0]
                                        skillNumber = int(skill_regex[1].replace(',',''))
                                        skills[skillName] = skillNumber
                                    topic['skills'] = skills
                            if topic_soup.find("div", {"class": "top-skills"}):
                                top_skills_div = topic_soup.find("div", {"class": "top-skills"})
                                if top_skills_div.find_all("li", {"class": "skill"}):
                                    top_skills = top_skills_div.find_all("li", {"class": "skill"})
                                    topSkills = []
                                    for top_skill in top_skills:
                                        topSkills.append(top_skill.getText())
                                    topic['topSkills'] = topSkills
                with open(r'C:\Users\shtabriz\Desktop\linkedin_topics.json', 'r+') as f:
                    if f.read():
                        f.write(',\n')
                    else:
                        f.write('[')
                    json.dump(topic,f)
                    print(topic)
                    

