from selenium import webdriver
import os
import requests
from selenium.webdriver.chrome.options import Options
import xlwt


# 获取访问指定url的状态码
def get_status_code(url):
    r = requests.get(url)
    return r.status_code


# 生成Issue报告
def make_issue_report():
    Desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    p1 = os.path.join(Desktop, "p.txt")
    options = Options()
    options.add_argument("--headless")

    auto = webdriver.Chrome(options=options)
    # auto.get('your gitlab sign_in page url')
    auto.get('http://192.168.0.180:10080/users/sign_in')
    user_name = auto.find_element_by_id('user_login')
    # your username
    user_name.send_keys('duliduo')
    user_password = auto.find_element_by_id('user_password')
    # your password
    user_password.send_keys('zyx123456789')
    sign_in = auto.find_element_by_name('commit')
    sign_in.click()

    # lir is your Issues urls
    lir = ['http://192.168.0.180:10080/Nebula/EHPEngine/issues?state=opened',
           'http://192.168.0.180:10080/Nebula/EHPEngine/issues?page=2&state=opened',
           'http://192.168.0.180:10080/Nebula/EHPEngine/issues?page=3&state=opened'
           ]

    issue_path = os.path.join(Desktop, "Issue.xls")
    new_workbook = xlwt.Workbook()
    new_sheet = new_workbook.add_sheet("SheetName_test")

    # Add from name
    new_sheet.write(0, 0, "Issue")
    new_sheet.write(0, 1, "Title")
    new_sheet.write(0, 2, "assignee")
    new_sheet.write(0, 3, "Status")
    new_sheet.write(0, 4, "Reopen")
    new_sheet.write(0, 5, "Create_date")
    new_sheet.write(0, 6, "Priority")
    new_sheet.write(0, 7, "Due_Date")

    count = 0
    for num in lir:
        if get_status_code(num) == 200:
            auto.get(num)

        # Issue Title
        title = auto.find_elements_by_class_name('issue-title-text')
        title_issue = []
        for item in title:
            title_issue.append(item.text)
        for i in range(len(title_issue)):
            j = i + 1 + count * 20
            new_sheet.write(j, 1, title_issue[i])

        # Issue ID
        id = auto.find_elements_by_class_name('issuable-reference')
        id_issue = []
        for item in id:
            id_issue.append(item.text)
        for i in range(len(id_issue)):
            j = i + 1 + count * 20
            new_sheet.write(j, 0, id_issue[i])

        # aggignee who
        assignee = auto.find_elements_by_xpath("//a[@class='author_link has-tooltip']")
        assignee_issue = []
        for item in assignee:
            assignee_issue.append(item.get_attribute("title"))
        for i in range(len(assignee_issue)):
            j = i + 1 + count * 20
            new_sheet.write(j, 2, assignee_issue[i])

        # Create Date
        date = auto.find_elements_by_xpath("//time[@class='js-timeago js-timeago-render']")
        create_date = []
        for item in date:
            create_date.append(item.get_attribute("datetime")[0:10])
            # print(item.get_attribute("datetime")[0:10])
        for i in range(len(create_date)):
            j = i + 1 + count * 20
            new_sheet.write(j, 5, create_date[i])
        count += 1
    new_workbook.save(issue_path)
    auto.close()
    list1 = os.listdir(Desktop)
    for i in list1:
        if 'Issue.csv' not in str(i):
            return False
        else:
            return True
