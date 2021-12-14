import re
import time
from datetime import datetime
from selenium.common.exceptions import StaleElementReferenceException
from filepath import Filepath


class BugInFormation(object):
    def __init__(self):
        pass

    def issue_if_exist(self,issueContent):
        if issueContent == '问题不存在':
            return False
        else:
            return True


        # try:
        #     # issueContent = self.driver.find_elements_by_xpath("//*[@id=\"issue-content\"]/header/div/header/div/div[1]/h1")
        #     if len(issueContent) > 0:
        #         if issueContent[0].text == '问题不存在':
        #             print(issueContent[0].text)
        #             return False  # 这是目前的最后一条jira
        #     else:
        #         print('问题存在')
        #         return True
        # except StaleElementReferenceException:
        #     # issueContent = self.driver.find_elements_by_xpath("//*[@id=\"issue-content\"]/header/div/header/div/div[1]/h1")
        #     if len(issueContent) > 0:
        #         if issueContent[0].text == '问题不存在':
        #             print(issueContent[0].text)
        #             return False  # 这是目前的最后一条jira
        #     else:
        #         print('问题存在')
        #         return True

    def jiraissue_status(self,status,resolutionVal):
        # status = self.driver.find_element_by_xpath('//*[@id="status-val"]/span')
        # resolutionVal = self.driver.find_element_by_xpath('//*[@id="resolution-val"]')

        if status == '[关闭]':  #要检查经办人是否有写修复版本
            print('问题状态 = '+str(status))
            if resolutionVal == '[解决]' or resolutionVal == '已完成':
                return status #这边要只检查经办人的修复版本，还是也要再检查一下报告人的影响版本和模块，可能还是要的，避免漏网之鱼。这里做一个判断，根据哪个内容没写，写出责任人
            else:
                return '无需检查'#问题为关闭，但是“解决结果”为其他情况的

        elif status== '[解决]':
            print('问题状态 = ' + str(status))
            if resolutionVal == '[解决]' or resolutionVal == '已完成':
                return status
            else:
                return '无需检查'#问题为关闭，但是“解决结果”为其他情况的
        else:     #要检查报告人是否有写影响版本,模块
            print("问题状态："+str(status))
            print("解决结果：" + str(resolutionVal))
            return False

    def type_check(self,type_val,parent_issue_type):
        # type_val = self.driver.find_element_by_xpath("//*[@id=\"type-val\"]")
        # print(type_val.text)
        if type_val == '问题点':
            print("问题类型为“问题点”")
            return True
        if type_val == '子任务开展':
            print("问题类型为“子任务开展”")
            # # 检查父问题类型
            # parent_issue = self.driver.find_elements_by_xpath("//*[@id=\"parent_issue_summary\"]")
            # # print(len(parent_issue))
            # parent_issue_link = parent_issue[0].get_attribute('href')
            # self.driver.get(parent_issue_link)
            # parent_type_val = self.driver.find_element_by_xpath("//*[@id=\"type-val\"]")
            if parent_issue_type:
                print("子任务的父问题是问题点")
                # self.driver.back()  # 返回上一页
                return True
            # else:
            #     # 获取父问题点的标题
            #     bug_title = self.driver.find_element_by_xpath("//*[@id=\"summary-val\"]")
            #     # print('bug_title='+str(bug_title.text))
            #
            #     #2020-11-11 优化，新增判断任务类型为“任务安排”的标题匹配，检查是否为buglist
            #     match_str = "Buglist|buglist|问题集"
            #     match = re.findall(match_str, str(bug_title.text))
            #     if len(match) != 0:
            #         print("子任务的父问题是buglist")
            #         self.driver.back()  # 返回上一页
            #         return True
            #     else:
            #         print("子任务的父问题不是问题点")
            #         return False

                #2020-11-11删除，用re.findall替代
                # match_buglist = re.match(r'.*Buglist.*', str(bug_title.text), re.I)  # re.I使匹配对大小写不敏感
                # # print('match_buglist='+str(match_buglist))
                # if match_buglist:  # 匹配成功，说明该问题是一个buglist的形式
                #     # buglis  t = match_buglist.group()
                #     print("子任务的父问题是buglist")
                #     self.driver.back()  # 返回上一页
                #     return True
                # print("子任务的父问题不是问题点")
                # return False
        else:
            print("问题类型为"+str(type_val))
            return False

    '''
    #不符合项检查判断 ---正确的
    def non_conformity_zq(self, check_item):
        affect_version = self.check_affect_version()
        fix_version = self.check_fix_version()
        affect_module = self.check_affect_module()
        customfield = self.check_customfield()   #检查“解决措施”内容是否符合规范
        description = self.check_description()
        comment1 = self.nonconformity_close_reason()   #发现有不符合项但关闭，检查是否填写关闭原因
        # comment2 = self.noreasontoclose()  # 检查解决措施填写不符合规范时顺便看下备注里面是否备注原因
        assigneecheck = self.assignee_check()
        assignee = self.driver.find_elements_by_xpath("//*[@id=\"assignee-val\"]") #经办人
        reporter = self.driver.find_elements_by_xpath("//*[@id=\"reporter-val\"]")  #报告人
        s1 = str(affect_version) + str(description) + str(affect_module)  #报告人检查项
        s2 = str(fix_version) + str(customfield)   #经办人检查项
        print("报告人不符合项 = " + str(s1))
        print("经办人不符合项 = " + str(s2))
        # print("s3 = " + str(s3))
        nonconformity = []
        responsible = []
        creator = self.check_creator()

        #经办人检查，为软件部开发人员才往下检查
        if assigneecheck:
            #为啥GGXB-4517没进入这个判断,因为不是软件开发部的开发提的，所以不会判断
            if creator:  # 判断bug为测试人员本人创建
                print('bug由报告人(测试人员)创建')
                ####################
                if check_item == "[关闭]":
                    if s1 != '':
                        nonconformity.append(s1)
                        responsible.append(reporter[0].text)
                    #TODO 判断s3备注内容是否合格
                    if customfield == '没写解决措施，但有写理由':
                        s3 = ''
                    # elif customfield == '没写解决措施，也没写理由':
                    #     pass
                    else:
                        s3 = str(comment1)  # 问题关闭后（测试人员/开发人员）备注，如果检查到不符合项，需要检查下备注的地方，解决措施的地方，是否有填写说明关闭的原因

                    if s3 != '':
                        nonconformity.append(s3)
                        if reporter[0].text in responsible:  #如果不符合项里的责任人中已经有测试人员的名字了，就不用再继续写入一个
                            pass
                        else:
                            responsible.append(reporter[0].text)
                    if s2 != '':
                        if s1 != '':
                            s2 = '\n' + str(fix_version) + str(customfield)
                        nonconformity.append(s2)
                        responsible.append(assignee[0].text)
                    return nonconformity,responsible
                elif check_item == "[解决]":
                    if s2 != '':
                        nonconformity.append(s2)
                        responsible.append(assignee[0].text)
                    return nonconformity, responsible

                elif check_item == "无需检查":#######之前忽略了问题为关闭但解决措施为取消的情况，这边没有针对这个做判断，现在补上
                    return nonconformity, responsible
                else:#提出，正在处理，重新打开
                    if s1 != '':
                        nonconformity.append(s1)
                        responsible.append(reporter[0].text)
                    return nonconformity, responsible
                ###########################
            else:
                print("该bug不是由测试人员本人创建")
                nonconformity.append("此bug不是由测试人员创建，但请测试人员尽量补全bug信息")
                responsible.append(reporter[0].text)
                return nonconformity, responsible
        else:
            print('报告人不是开发人员')
            return nonconformity, responsible

        # 不符合项检查判断

    def non_conformity(self, check_item):
        affect_version = self.check_affect_version()
        fix_version = self.check_fix_version()
        affect_module = self.check_affect_module()
        customfield = self.check_customfield()  # 检查“解决措施”内容是否符合规范
        description = self.check_description()
        comment1 = self.nonconformity_close_reason()  # 发现有不符合项但关闭，检查是否填写关闭原因
        # comment2 = self.noreasontoclose()  # 检查解决措施填写不符合规范时顺便看下备注里面是否备注原因
        assigneecheck = self.assignee_check()
        assignee = self.driver.find_elements_by_xpath("//*[@id=\"assignee-val\"]")  # 经办人
        reporter = self.driver.find_elements_by_xpath("//*[@id=\"reporter-val\"]")  # 报告人
        s1 = str(affect_version) + str(description) + str(affect_module)  # 报告人检查项
        s2 = str(fix_version) + str(customfield)  # 经办人检查项
        print("报告人不符合项 = " + str(s1))
        print("经办人不符合项 = " + str(s2))
        # print("s3 = " + str(s3))
        nonconformity = []
        responsible = []
        creator = self.check_creator()

        # 经办人检查，为软件部开发人员才往下检查
        if assigneecheck:
            ####################
            if check_item == "[关闭]":
                if s1 != '':
                    if creator:  # 判断bug为测试人员本人创建
                        print('bug由报告人(测试人员)创建')
                        nonconformity.append(s1)
                        responsible.append(reporter[0].text)
                    else:
                        s1 = s1 + "(此bug不是由测试人员创建，但请测试人员尽量补全bug信息)"
                        nonconformity.append(s1)
                        responsible.append(reporter[0].text)

                # TODO 判断s3备注内容是否合格
                if customfield == '没写解决措施，但有写理由':
                    s3 = ''
                # elif customfield == '没写解决措施，也没写理由':
                #     pass
                else:
                    s3 = str(comment1)  # 问题关闭后（测试人员/开发人员）备注，如果检查到不符合项，需要检查下备注的地方，解决措施的地方，是否有填写说明关闭的原因

                if s3 != '':
                    nonconformity.append(s3)
                    if reporter[0].text in responsible:  # 如果不符合项里的责任人中已经有测试人员的名字了，就不用再继续写入一个
                        pass
                    else:
                        responsible.append(reporter[0].text)
                if s2 != '':
                    if s1 != '':
                        s2 = '\n' + str(fix_version) + str(customfield)
                    nonconformity.append(s2)
                    responsible.append(assignee[0].text)
                return nonconformity, responsible
            elif check_item == "[解决]":
                if s2 != '':
                    nonconformity.append(s2)
                    responsible.append(assignee[0].text)
                return nonconformity, responsible

            elif check_item == "无需检查":  #######之前忽略了问题为关闭但解决措施为取消的情况，这边没有针对这个做判断，现在补上
                return nonconformity, responsible
            else:  # 提出，正在处理，重新打开
                print("问题类型为提出，正在处理，重新打开")
                print(creator)
                if s1 != '':
                    if creator:  # 判断bug为测试人员本人创建
                        print('bug由报告人(测试人员)创建')
                        nonconformity.append(s1)
                        responsible.append(reporter[0].text)
                    else:
                        s1 = s1 + "(此bug不是由测试人员创建，但请测试人员尽量补全bug信息)"
                        print(s1)
                        nonconformity.append(s1)
                        responsible.append(reporter[0].text)
                return nonconformity, responsible
                ###########################
        else:
            print('报告人不是开发人员')
            return nonconformity, responsible





    # 检查“bug描述”
    def check_description(self):
        s = ''
        string = ''
        ms = ''
        description = self.driver.find_elements_by_xpath("//*[@id=\"description-val\"]/div/p")  # "问题描述"内容定位
        if len(description) != 0:
            for i in description: #问题描述里，如果有空行，会分段，所以要把所有段加起来
                ms += str(i.text)
            matchstring = ms
        else:
            matchstring = ''
            print('没有问题描述')
        # match_description = re.match(r'[\s\S]*前[\s\S]*操作[\s\S]*结果[\s\S]*结果[\s\S]*', str(matchstring), re.I)
        # match1 = re.match(r'[\s\S]*率[\s\S]*', str(matchstring), re.I)  #出现概率暂时不检查，目前各个项目写法不同，后面还会推rpn，所以暂时不写
        # match2 = re.match(r'[\s\S]*前[\s\S]*', str(matchstring), re.I)
        match2s = "前置|前提|预置"
        match2 = re.findall(match2s,str(matchstring))
        # match3 = re.match(r'[\s\S]*操作[\s\S]*', str(matchstring), re.I)
        match3s = "操作"
        match3 =re.findall(match3s,str(matchstring))
        # match4 = re.match(r'[\s\S]*预期结果[\s\S]*', str(matchstring), re.I)
        match4s = "预期结果|期望结果|预期输出"
        match4 = re.findall(match4s,str(matchstring))
        # print('match4='+str(match4))
        match5s = "实际结果|实际输出"
        match5 = re.findall(match5s, str(matchstring))
        # match5 = re.match(r'[\s\S]*实际结果[\s\S]*', str(matchstring), re.I)
        # match6 = re.match(r'[\s\S]*附件[\s\S]*', str(matchstring), re.I)   #有些UI问题，只能用截图表示的

        if len(description) == 0:
            s = "问题描述没写;"
            # return s
        # if match_description == None:
        #     s = "问题描述没有填写规范;"
            # return s
        else:
            # if match1 == None:
            #     string += "出现概率没有写;"
            # if match2 == None:
            #     string += "前提条件没有写;"
            # if match3 == None:
            #     string += "操作步骤没有写;"
            # if len(match4) == 0:
            #     string += "预期结果没有写;"
            # if match5 == None:
            #     string += "实际结果没有写;"
            if len(match2) == 0 and len(match3) == 0 and len(match4) == 0 and len(match5) == 0:
                match_fujian = "附件"
                match_attachment = re.findall(match_fujian,matchstring)
                if len(match_attachment) == 0:
                    s = "Bug描述详情没写;"
            else:
                # print("跳到这里来")
                if len(match2) == 0:
                    string += "前提条件没有写;"
                if len(match3) == 0:
                    string += "操作步骤没有写;"
                if len(match4) == 0:
                    string += "预期结果没有写;"
                if len(match5) == 0:
                    string += "实际结果没有写;"

        if s != '':
            return s
        elif string != '':
            string = 'Bug描述详情：'+ string
            return string
        # elif match6 != None:  #只写见附件，没有问题描述的情况
        #     s_match6 = ''
        #     return s_match6
        else:
            return ''

    # 检查“检查解决措施”内容
    def check_customfield(self):
        s = ''
        ss=''
        customfield = self.driver.find_elements_by_xpath("//*[@id=\"customfield_10040-val\"]")  # “解决措施”定位
        if len(customfield) != 0:
            matchstring = customfield[0].text
            # print(matchstring)
        else:
            matchstring = ''
            print('解决措施没有写')
        # match_customfield = re.match(r'.*问题原因[\s\S]*解决措施[\s\S]*影响范围[\s\S]*提交.*', str(matchstring), re.I)
        matcmatch_customfield_1s = "问题原因|原因"
        match_customfield_1 = re.findall(matcmatch_customfield_1s, str(matchstring))
        # match_customfield_1 = re.match(r'[\s\S]*问题原因[\s\S]*', str(matchstring), re.I)
        # match_customfield_2 = re.match(r'[\s\S]*解决措施[\s\S]*', str(matchstring), re.I)
        matcmatch_customfield_2s = "解决措施"
        match_customfield_2 = re.findall(matcmatch_customfield_2s, str(matchstring))
        matcmatch_customfield_3s = "影响范围"
        match_customfield_3 = re.findall(matcmatch_customfield_3s, str(matchstring))
        # match_customfield_3 = re.match(r'[\s\S]*影响范围[\s\S]*', str(matchstring), re.I)
        # match_customfield_4 = re.match(r'[\s\S]*提交[\s\S]*', str(matchstring), re.I)
        matcmatch_customfield_4s = "提交"
        match_customfield_4 = re.findall(matcmatch_customfield_4s, str(matchstring))

        if len(customfield) == 0:
            # 添加判断，没写解决措施，则检查备注里面是否有写关闭的原因---这个就不是bug本身引起的问题了，误提或者工具问题等
            #没写解决措施，但是“备注里面”有可关闭字眼。说明有解释关闭的原因了？不一定，一种是真的解释了原因，一种是真的没有写解决措施。所以还是要正则判断一下
            comment = self.noreasontoclose()
            return str(comment)
            # if comment == '没写解决措施，但有写理由':
            #     print('没写解决措施，但有写理由')
            #     return "没写解决措施，但有写理由"
            # else:
            #     return "解决措施没写"
        else:
            if len(match_customfield_1)==0 and len(match_customfield_2) == 0 and len(match_customfield_3)==0 and len(match_customfield_4)==0:
                s = "未按照要求填写;"
                #TODO 这边要添加如果问题重复的判断，开发直接写“已创建类似问题，属于重复问题”的情况，类似这种情况需要给出另一个相似问题的jiraid才可以
            else:
                if len(match_customfield_1)==0:
                    s += '问题原因没写；'
                if len(match_customfield_2)==0:
                    s += '解决措施没写；'
                if len(match_customfield_3)==0:
                    s += '影响范围没写；'
                if len(match_customfield_4)==0:
                    s += '是否提交代码没写；'
            if s != '':
                s = '"解决措施"内容：'+s
                return s
            else:
                return s


    def check_affect_version(self):
        s = ''
        affect_version = self.driver.find_elements_by_xpath("//*[@id=\"versions-field\"]")
        if len(affect_version) == 0:
            s = "影响版本没写;"
            return s
        else:
            return ''

    def check_fix_version(self):
        s = ''
        fix_version = self.driver.find_elements_by_xpath("//*[@id=\"fixVersions-field\"]")
        if len(fix_version) == 0:
            s ="修复版本没写;"
            return s
        else:
            return ''

    def check_affect_module(self):
        s = ''
        project_name = self.driver.find_elements_by_xpath("//*[@id=\"project-name-val\"]")  # jirabug中的项目名称
        affect_module = self.driver.find_elements_by_xpath("//*[@id=\"components-field\"]")
        if project_name[0].text == '咕咕学霸': #咕咕学霸的bug中模块不检查
            return ''
        else:
            if len(affect_module) == 0:
                s = "模块没写;"
                return s
            else:
                return ''
'''

    #检查是否为测试人员提交
    def reporter_check(self,reporter_id):
        testerlist = Filepath()
        reporter_dict = testerlist.reporter_file()
        # user_hover = self.driver.find_elements_by_xpath("//*[@class='user-hover']")
        # weizhi = len(user_hover)-1
        # reporter_id = user_hover[weizhi].get_attribute('rel')
        # print(reporter_id)
        # print(reporter_dict.keys())

        if reporter_id in reporter_dict.keys():
            print("测试人员名字：", reporter_dict[reporter_id])
            return reporter_dict[reporter_id]
        else:
            print("非测试人员提交")
            return False

    #检查是否为软件开发人员提交
    def assignee_check(self,reporter_id):
        assigneelist = Filepath()
        reporter_dict = assigneelist.assignee_file()
        # user_hover = self.driver.find_elements_by_xpath("//*[@class='user-hover']")
        # reporter_id = user_hover[0].get_attribute('rel')
        if reporter_id in reporter_dict.keys():
            print("开发人员名字：", reporter_dict[reporter_id])
            return reporter_dict[reporter_id]
        else:
            print("非开发人员提交")
            return False

    '''


    #发现有不符合项但关闭，检查是否填写关闭原因
    def nonconformity_close_reason(self):
        b = self.driver.find_elements_by_xpath("//*[@id=\"comment-tabpanel\"]")
        b[0].click()
        time.sleep(0.4)
        comment = self.driver.find_elements_by_xpath("//*[@id=\"issue_actions_container\"]")  # 获取到的内容应该倒着来匹配正则表达式内容
        comment_list = str(comment[0].text).split('\n')
        # print(comment_list)
        s = ''
        for i in comment_list[::-1]:  # 倒叙遍历
            comment_s1 = "可关闭|验证通过|关闭该问题点|故关闭|已解决|已修复|未复现"  # 备注里面
            match_comment_s1 = re.findall(comment_s1, i)
            if len(match_comment_s1) == 0:
                # print("不匹配")
                s = '未备注问题可以关闭的原因；'
            else:
                # print("匹配")
                break
        return s

    # 检查解决措施填写不符合规范时顺便看下备注里面是否备注原因
    def noreasontoclose(self):
        b = self.driver.find_elements_by_xpath("//*[@id=\"comment-tabpanel\"]")
        b[0].click()
        time.sleep(0.4)
        comment = self.driver.find_elements_by_xpath("//*[@id=\"issue_actions_container\"]")  # 获取到的内容应该倒着来匹配正则表达式内容
        comment_list = str(comment[0].text).split('\n')
        # print(comment_list)
        s = ''
        for i in comment_list[::-1]:  # 倒叙遍历
            comment_s1 = "[\s\S]*问题，故关闭|重复提交|误提|已修复" # 备注里面
            match_comment_s1 = re.findall(comment_s1, i)
            if len(match_comment_s1) == 0:
                # print("备注不匹配")
                s = '没写解决措施，也没写理由'
            else:
                # print("备注匹配")
                s = '没写解决措施，但有写理由'
                break
        return s

    def check_creator(self):  #判断问题的创建人是否与报告人一致
        b = self.driver.find_elements_by_xpath("//*[@id=\"all-tabpanel\"]")
        if len(b):
            b[0].click()
            time.sleep(0.5)
        creator = self.driver.find_elements_by_xpath("//*[@class='user-hover user-avatar']")
        # print(creator[0].get_attribute('rel'))
        user_hover = self.driver.find_elements_by_xpath("//*[@class='user-hover']")
        weizhi = len(user_hover)-1
        if creator[0].get_attribute('rel')==user_hover[weizhi].get_attribute('rel'):
            return True
        else:
            return False

    def resolution_time(self):
        create_date = self.driver.find_elements_by_xpath("//*[@id=\"create-date\"]/time")
        resolute_date = self.driver.find_elements_by_xpath("//*[@id=\"resolved-date\"]/time")
        bug_status = status = self.driver.find_element_by_xpath('//*[@id="status-val"]/span')
        user_hover = self.driver.find_elements_by_xpath("//*[@class='user-hover']")
        reporter_name = user_hover[0].text
        create_time = ''
        resolute_time = ''
        time_difference = ''
        if len(create_date) and len(resolute_date):
            create_time = str(create_date[0].get_attribute('datetime')).replace("T", " ")
            create_time = create_time.replace("+0800","")
            print(create_time)
            # create_time = datetime.strptime(createtime,"%Y-%m-%d %H:%M:%S" )
            resolute_time = str(resolute_date[0].get_attribute('datetime')).replace("T", " ")
            resolute_time = resolute_time.replace("+0800", "")
            print(resolute_time)
            # resolute_time = datetime.strptime(resolutetime, "%Y-%m-%d %H:%M:%S")
            # time_difference = resolute_time - create_time
            # print(time_difference)
        elif len(create_date) == 0:
                create_time = ''
                print("没有创建时间")
        elif len(resolute_date) == 0:
                resolute_time = ''
                print("没有创建时间")

        return create_time, resolute_time, bug_status.text,reporter_name

'''


