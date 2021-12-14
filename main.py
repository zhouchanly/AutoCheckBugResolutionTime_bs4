import re
import time
import traceback

from buginfomation import BugInFormation
from driversetting import Driversettings
from elementanalysis import Elementanalysis
from filepath import Filepath
from readfromexcel import ReadExcel
from review import Review
from singlereport import Singlereport
from writeintoexcel import WriteExcel




if __name__=="__main__":
    # driversetting = Driversettings()
    # driver = driversetting.set_driver()
    # driversetting.login(driver)


    path = Filepath()
    jiradict = path.projectlist_file()
    s = Singlereport()
    # jiexi = Elementanalysis()   #元素解析到进来了，下面直接给它穿url就可以了。下面的driver可以去掉



    try:
        for key in jiradict:
            jiraname = key
            jira_sheetname = jiradict[key]
            print(jira_sheetname)
            read_excel=ReadExcel(jiraname,jira_sheetname)
            project_exist=read_excel.project_if_exist()

            writeexcel = WriteExcel() #实例化
            buginformation = BugInFormation()  #实例化
            review = Review()  #实例化

            
            #检查新问题
            for id in range(read_excel.latest_id(),9000):
                url_id = str(jiraname + '-' + str(id))
                # url=driversetting.get_url(url_id)

                print("当前检查的问题："+ jiraname + '-' + str(id))
                elementanalysis = Elementanalysis(url_id)
                issueContent = elementanalysis.issueContent()
                status=elementanalysis.bug_status()
                resolutionVal=elementanalysis.bug_status_type()
                assignee_reporter=elementanalysis.assignee_reporter()
                creatdate = elementanalysis.creat_date()
                resolveddate = elementanalysis.resolved_date()

                #获取问题类型
                type_val = elementanalysis.type_check()
                #直接获取，看有没有父标题
                parent_issue = elementanalysis.parent_issue()

                if parent_issue:
                    parent_issue_analysis = Elementanalysis(parent_issue)
                    parent_issue_type =parent_issue_analysis.parent_type_check()
                else:
                    #父链接不是bug，就不往下查了
                    parent_issue_type = False



                if buginformation.issue_if_exist(issueContent):    #检查问题是否存在
                    if buginformation.type_check(type_val,parent_issue_type):   #检查问题类型
                        if buginformation.reporter_check(assignee_reporter[1]):
                            # check_item = buginformation.jiraissue_status()
                            # print("check_item="+str(check_item))
                            # bug_time_infor = buginformation.resolution_time()
                            # bug_non_conformity=buginformation.non_conformity(check_item)
                            writeexcel.write_non_conformity(read_excel.latest_nrows(), jiraname,
                                                            jiraname + '-' + str(id), creatdate,
                                                            resolveddate, status,assignee_reporter[1])
                            read_excel.latest_nrows() + 1

                        else:
                            writeexcel.write_lates_id(read_excel.latest_nrows(), jiraname, jiraname + '-' + str(id))
                    else:
                        writeexcel.write_lates_id(read_excel.latest_nrows(), jiraname, jiraname + '-' + str(id))
                else:
                    writeexcel.write_lates_id(read_excel.latest_nrows(), jiraname, jiraname + '-' + str(id))
                    break
        backpath = path.backup_file()
        summarypath = path.summary_report()
        path.backup_summary(summarypath, backpath)  # 备份汇总报告
        # driver.quit()

    except BaseException:  #Python所有的错误都是从BaseException类派生的,所以用这个方式来保证程序发生任何错误时，备份汇总报告
        backpath = path.backup_file()
        summarypath = path.summary_report()
        path.backup_summary(summarypath, backpath)  #备份汇总报告
        traceback.print_exc() #打印异常
        # driver.quit()







