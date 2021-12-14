import xlrd as xlrd
from xlutils.copy import copy

from filepath import Filepath


class WriteExcel(object):
    def __init__(self):
        pass

    def write_lates_id(self,last_rows,jiraname,jiraid):
        path = Filepath()
        summarypath = path.summary_report()
        xls = xlrd.open_workbook(summarypath, formatting_info=True)
        newxls = copy(xls)
        existproject = xls.sheet_names()
        project_sheet_index = existproject.index(jiraname)  # 获取projectjiraid在sheet表中的index序列号值
        project_sheet = newxls.get_sheet(project_sheet_index)
        project_sheet.write(int(last_rows)-1, 5, jiraid)
        newxls.save(summarypath)

    def write_non_conformity(self,last_rows,jiraname,jiraid,createtime, resolutiontime, bugstatus,reporter_name):  # 检查到不符合项，调用这个函数写到表格里
        path = Filepath()
        summarypath = path.summary_report()
        xls = xlrd.open_workbook(summarypath, formatting_info=True)
        newxls = copy(xls)
        project_sheet_old= xls.sheet_by_name(jiraname)
        existproject = xls.sheet_names() #获取所有工作表名
        project_sheet_index = existproject.index(jiraname)  # 获取表的序列号
        project_sheet = newxls.get_sheet(project_sheet_index)#使用获取到的序列号提取复制的新的newxls中对应的表格

        #这里做一个判断，如果除了第6列的id号有写，其他前几列没写，就直接这在这行上面
        cell1 = project_sheet_old.cell(last_rows - 1, 0).ctype
        cell2 = project_sheet_old.cell(last_rows - 1, 1).ctype
        cell3 = project_sheet_old.cell(last_rows - 1, 2).ctype
        cell4 = project_sheet_old.cell(last_rows - 1, 3).ctype


        if cell1==0 and cell2==0 and cell3==0 and cell4==0:
            project_sheet.write(last_rows - 1, 0, jiraid)
            project_sheet.write(last_rows - 1, 1, createtime)
            project_sheet.write(last_rows - 1, 2, resolutiontime)
            project_sheet.write(last_rows - 1, 3, bugstatus)
            project_sheet.write(last_rows - 1, 4, reporter_name)
            # project_sheet.write(last_rows - 1, 6, time_difference)
        else:
            project_sheet.write(last_rows, 0, jiraid)
            project_sheet.write(last_rows, 1, createtime)
            project_sheet.write(last_rows, 2, resolutiontime)
            project_sheet.write(last_rows, 3, bugstatus)
            project_sheet.write(last_rows, 4, reporter_name)
            # project_sheet.write(last_rows, 6, time_difference)
        newxls.save(summarypath)

