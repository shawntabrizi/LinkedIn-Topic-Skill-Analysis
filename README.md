# LinkedIn-Topic-Skill-Analysis
This is a tool that will automatically collect public data about linkedin skills and topics, and do analysis on them.

I do analysis on using this data here:
http://shawntabrizi.com/linkedin/scraping-linkedin-topics-skills-data/

### How many topics are there total?
```
len(data)
```
```
33188
```




### What are the most popular overall topics/skills?
```	
ordered_by_count = sorted(data, key=lambda k: k['count'] if isinstance(k['count'],int) else 0, reverse=True)
for skill in ordered_by_count[:20]:
    print(skill['name'])
```
```
Management - 69725749
Microsoft - 55910552
Office - 46632581
Microsoft Office - 45351678
Planning - 34397412
Microsoft Excel - 32966966
Leadership - 31017503
Customer Service - 30810924
Leadership Management - 25854094
Word - 25793371
Project - 25766790
Project+ - 25766790
Microsoft Word - 25567902
Business - 25374740
Customer Management - 24946045
Management Development - 24207445
Development Management - 24207409
Project Management - 23922491
Marketing - 23047665
Customer Service Management - 22856920
```




### What are the top <Company> Skills?
```
company = 'Microsoft'
company_skills = []
for skill in ordered_by_count:
    if skill['companies'] is not None:
        if company in skill['companies']:
            company_skills.append(skill)
 
order_by_company = sorted(company_skills, key=lambda k: k['companies'][company], reverse=True)
for skill in order_by_company[:20]:
     print(skill['name'], "-", skill['companies'][company])
```
Microsoft
```
Cloud - 74817
Cloud Computing - 74817
Cloud-Computing - 74817
Cloud Services - 74817
Management - 73123
Management Skills - 73123
Multi-Unit Management - 73123
Enterprise - 54516
Enterprise Software - 54516
Software Development - 53201
Project Management - 52083
Project Management Skills - 52083
PMP - 52083
PMI - 52083
Strategy - 43983
SaaS - 41450
Software as a Service - 41450
Program Management - 40749
Business Intelligence - 39291
C# - 39158
```
Google
```
Java - 23225
Strategy - 22235
Marketing - 21672
Data-driven Marketing - 21672
Python - 20788
Software Development - 20406
C++ - 20199
Social Media - 20082
Social Networks - 20082
Digital Marketing - 19942
Online Advertising - 19922
Marketing Strategy - 16882
Linux - 16272
JavaScript - 14567
JavaScript Frameworks - 14567
C - 14460
C Programming - 14460
Online Marketing - 13925
Online-Marketing - 13925
Social Media Marketing - 12931
```
Amazon
```
Leadership - 44329
Leadership Skills - 44329
Microsoft Office - 42713
Office for Mac - 42713
Customer Service - 36176
Microsoft Excel - 33403
Java - 25609
Word - 23314
Microsoft Word - 23314
PowerPoint - 22318
Microsoft PowerPoint - 22318
Social Media - 22110
Social Networks - 22110
C++ - 19619
Training - 19250
Marketing - 18826
Data-driven Marketing - 18826
Software Development - 18521
Public Speaking - 17366
C - 16813
```
Facebook
```
Digital Marketing - 4973
Online Advertising - 4334
Digital Strategy - 3399
Online Marketing - 3012
Online-Marketing - 3012
Facebook - 2883
Algorithms - 2881
Mobile Marketing - 2163
Machine Learning - 2103
Distributed Systems - 2033
User Experience - 1971
UX - 1971
Web Analytics - 1682
SEM - 1626
Computer Science - 1440
Google Analytics - 1261
Adwords - 1093
Google AdWords - 1093
Scalability - 1057
Mobile Advertising - 919
```




### What are the top interconnected skills?
```
skill_count = {}
for topic in data:
    if topic['skills'] is not None:
        for top_skill in topic['skills']:
            if top_skill not in skill_count:
                skill_count[top_skill] = 1
            else:
                skill_count[top_skill] += 1
    if topic['topSkills'] is not None:
        for top_skill in topic['topSkills']:
            if top_skill not in skill_count:
                skill_count[top_skill] = 1
            else:
                skill_count[top_skill] += 1
 
for skill in sorted(skill_count, key=skill_count.get, reverse = True)[:20]:
    print(skill, "-", skill_count[skill])
```
```
Microsoft Office - 11081
Management - 8845
Customer Service - 7010
Project Management - 6902
Microsoft Excel - 4884
Leadership - 4682
Social Media - 3883
Research - 3798
Public Speaking - 3243
Marketing - 2644
Microsoft Word - 2426
Sales - 2335
SQL - 2322
Engineering - 2300
Business Development - 2071
Strategic Planning - 1879
Java - 1792
Adobe Photoshop - 1555
JavaScript - 1488
Microsoft PowerPoint - 1483
```
