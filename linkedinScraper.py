from bs4 import BeautifulSoup
import requests
import string
import re
import json

def scrape_data(topic_url):
    topic = {}
    topic['name'] = topic_url.getText()
    topic['count'] = None
    topic['companies'] = None
    topic['skills'] = None
    topic['topSkills'] = None
    if topic_url.has_attr('href'):
        r = requests.get(topic_url['href'])
        topic_soup = BeautifulSoup(r.text)
        if r.status_code != 404:
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
    return topic

def create_json(topic):
    with open(r'C:\Users\shtabriz\Desktop\linkedin_topics.json', 'r+') as f:
        if f.read():
            f.write(',\n')
        else:
            f.write('[')
        json.dump(topic,f)
        print(topic)

        return

def get_content(url):
    headers = {

        }
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    section_last = soup.find("div", {"class": "section last"})
    if section_last.find_all("li", {"class": "content"}):
        content = section_last.find_all("li", {"class": "content"})
    else:
        content = None

    return content

def main():
    letters = list(string.ascii_lowercase)
    letters.append('more')
    base_url = "https://www.linkedin.com/directory/topics-"
    for letter in letters:
        letter_url = base_url + letter + "/"
        content = get_content(letter_url)
        for con in content:
            if letter == 'y' or letter == 'z':
                sub_content = content
            else:
                letter_page_url = con.find("a")
                print(letter_page_url)
                if letter_page_url.has_attr('href'):
                    sub_content = get_content(letter_page_url['href'])
                else:
                    sub_content = None
            for sub_con in sub_content:
                topic_url = sub_con.find("a")
                topic = scrape_data(topic_url)
                create_json(topic)
            if letter == 'y' or letter == 'z':
                break