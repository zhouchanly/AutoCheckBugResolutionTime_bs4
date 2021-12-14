import re

import requests,bs4

from requests.auth import HTTPBasicAuth

class Elementanalysis():  #直接传入soup
    def __init__(self,jiraid):
        url = ("http://jira.intretech.com:8080/browse/" + jiraid)
        res = requests.get(url, auth=HTTPBasicAuth('10324', '123aaa'))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features="html.parser")
        self.soup=soup

    #问题详情-状态
    def bug_status(self):
        try:
            bug_status = self.soup.find(id="status-val")  # 问题详情中的状态
            bug_status_text = bug_status.text.strip()
            # print(bug_status_text)
            return bug_status_text
        except AttributeError:
            print("找不到问题状态，出现以下异常%s" % AttributeError)
            return False

    #问题详情-解决结果
    def bug_status_type(self):
        try:
            bug_status_type = self.soup.find(id="resolution-val")  # 问题详情中的类型
            bug_status_type_text = bug_status_type.text.strip()
            # print(bug_status_type_text)
            return bug_status_type_text
        except AttributeError:
            print("找不到问题详情中断饿解决结果，出现以下异常%s" % AttributeError)
            return False

    #问题详情-模块
    def components(self):
        try:
            components = self.soup.find(id="components-field")  # 问题详情中的“模块”---输出的结果有点话都有值
            components_text = components.text.strip()
            print(components_text)
            return components_text
        except AttributeError:
            print("找不到模块，出现以下异常%s" % AttributeError)
            return False

    #经办人&报告人
    def assignee_reporter(self):
        try:
            assignee_reporter = self.soup.find_all("span", attrs={"class", "user-hover"})
            assignee_gonghao = assignee_reporter[0].get('rel')  # 经办人工号
            reporter_gonghao = assignee_reporter[1].get('rel')  # 报告人工号
            print(assignee_gonghao, reporter_gonghao)
            return assignee_gonghao, reporter_gonghao
        except AttributeError:
            print("找不到报告人/经办人，出现以下异常%s" % AttributeError)
            return False

    #创建时间
    def creat_date(self):
        try:
            creat_date = self.soup.find(id="create-date")
            creat_time = creat_date.find("time", attrs={"class", "livestamp"})
            creattime = creat_time.get("datetime")
            return creattime
        except AttributeError:
            print("找不到创建时间，出现以下异常%s" % AttributeError)
            return False

    #解决时间
    def resolved_date(self):
        try:
            resolved_date = self.soup.find(id="resolved-date")
            resolved_time = resolved_date.find("time", attrs={"class", "livestamp"})
            resolvedtime = resolved_time.get("datetime")
            return resolvedtime
        except AttributeError:
            print("找不到解决时间，出现以下异常%s" % AttributeError)
            return False

    #问题不存在
    def issueContent(self):
        try:
            issueContent = self.soup.find("div", attrs={"class", "aui-page-header-main"})
            issue_Content = issueContent.text
            return issue_Content
        except AttributeError:
            print("找不到'问题不存在'%s" % AttributeError)
            return False

    #问题详情-类型
    def type_check(self):
        try:
            type_check = self.soup.find(id="type-val")
            type_check_value = type_check.text.strip()
            return type_check_value
        except AttributeError:
            print("找不到问题类型，出现以下异常%s" % AttributeError)
            return False

    #提取父链接id
    def parent_issue(self):  #如果有的话可能要在这里做处理判断父连接
        try:
            parent_issue=self.soup.find(id="parent_issue_summary")
            # print(parent_issue)
            parent_issue_id = parent_issue.get("data-issue-key")
            # print(parent_issue_id)
            #打印问题标题
            # parent_bug_title = self.soup.title.string
            # print(parent_bug_title)

            #这些不应该放在这里，应该放在type_check里去判断，type_check是用来判断类型的，父问题类型和子问题类型都应该判断
            # match_str = "Buglist|buglist|问题集"
            # match = re.findall(match_str, str(parent_bug_title.text))
            # print("match长度" %len(match))
            # parent_issue_isbug =False
            # if len(match) != 0:
            #     print("子任务的父问题是buglist")
            #     parent_issue_isbug = True
            # return parent_issue_id,parent_issue_isbug
            return parent_issue_id

        except AttributeError:
            print("找不到父链接，出现以下异常%s" % AttributeError)
            return False

    #判断父链接是否为buglist
    def parent_type_check(self):
        try:
            type_check = self.soup.find(id="type-val")
            type_check_value = type_check.text.strip()
            print(type_check_value)
            if type_check_value == "问题点":
                return True
            else:
                parent_bug_title = self.soup.title.string
                print(parent_bug_title)
                match_str = "Buglist|buglist|问题集"
                match = re.findall(match_str, str(parent_bug_title))
                print(len(match))
                if len(match):
                    return True
                else:
                    return False
        except AttributeError:
            print("找不到问题类型，出现以下异常%s" % AttributeError)
            return False
    #  问题类型  直接在里面判断类型好了

    # 问题详情-发生概率
    # 问题详情-前提条件
    # 问题详情-操作步骤
    # 问题详情-实际结果
    # 问题详情-预期结果

    # 问题详情-影响范围
    # 问题详情-是否提交代码
    # 问题详情-原因分析
    # 问题详情-解决措施

    #描述里的bug详情

    #附件有无判断

    #备注内容判断






# url='http://jira.intretech.com:8080/browse/GGXB-4800'
# res=requests.get(url,auth=HTTPBasicAuth('10324','123aaa'))
#
# res.raise_for_status()
#
# soup=bs4.BeautifulSoup(res.text,features="html.parser")

# GGXB-4253
e=Elementanalysis('GGXB-5314')
print(e.bug_status_type())
print(e.type_check())
# e1 = e.type_check()
# print(e1)
#
# e2 = e.parent_issue()
# print(e2)
#
# e3 = e.parent_type_check()
# print(e3)

