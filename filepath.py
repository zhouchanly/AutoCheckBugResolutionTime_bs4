import os
import shutil
import time
import yaml


class Filepath(object):
    def summary_report(self):
        curPath = os.path.dirname(os.path.realpath(__file__))
        report = 'report'
        summary = 'summaryreport'
        summaryreport_path = os.path.join(curPath,report,summary, "Bug_info_check.xls")#输出的类似是“'C:\\Users\\test\\Desktop\\Bug_info_check.xls'”
        return summaryreport_path

    def single_report(self):
        sheetname = time.strftime("%Y-%m-%d", time.localtime()) + ' jira Bug内容规范检查.xls'
        curPath = os.path.dirname(os.path.realpath(__file__))
        report = 'report'
        single = 'singlereport'
        singlereport_path = os.path.join(curPath,report,single,sheetname)
        return singlereport_path, sheetname


    def projectlist_file(self):
        curPath = os.path.dirname(os.path.realpath(__file__))
        yamlPath = os.path.join(curPath, "projectlist.yaml")
        file = open(yamlPath, 'r', encoding='utf-8')
        projectlist = file.read()
        jiradict = yaml.load(projectlist, Loader=yaml.FullLoader)
        return jiradict

    def reporter_file(self):
        curPath = os.path.dirname(os.path.realpath(__file__))  # 获取当前脚本所在文件夹路径
        yamlPath = os.path.join(curPath, "reporter.yaml")  # 获取yaml文件路径
        file = open(yamlPath, 'r', encoding='utf-8')  # open方法打开直接读出来
        reporter_list = file.read()
        reporter_dict = yaml.load(reporter_list, Loader=yaml.FullLoader)  # 用load方法转字典
        return reporter_dict

    def assignee_file(self):
        curPath = os.path.dirname(os.path.realpath(__file__))  # 获取当前脚本所在文件夹路径
        yamlPath = os.path.join(curPath, "assignee.yaml")  # 获取yaml文件路径
        file = open(yamlPath, 'r', encoding='utf-8')  # open方法打开直接读出来
        assignee_list = file.read()
        assignee_dict = yaml.load(assignee_list, Loader=yaml.FullLoader)  # 用load方法转字典
        return assignee_dict

    def backup_file(self):  #TODO 这个方法直接写成备份好的数据就好了
        curPath = os.path.dirname(os.path.realpath(__file__))
        report = 'report'
        backup = 'backupreport'
        file_name = 'Bug_info_check(backupin' + time.strftime("%Y_%m_%d", time.localtime()) + ').xls'
        backupreport_path = os.path.join(curPath, report, backup,file_name)  # 输出的类似是“'C:\\Users\\test\\Desktop\\Bug_info_check.xls'”
        return backupreport_path

    def backup_summary(self,oldfile,newfile):
        shutil.copyfile(oldfile,newfile)

# #\report\singlereport
# f=Filepath()
# a=f.single_report()
# b=f.summary_report()
# # old='C:\/Users\/test\Desktop\APK\/adblogcat\log.txt'
# # new='C:\/Users\/test\Desktop\APK\/adblogcat\log222222.txt'
# # c=f.backup_summary(old,new)
# g=f.backup_file()