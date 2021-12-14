import re
import xlrd
import xlwt
from xlutils.copy import copy
from filepath import Filepath


class ReadExcel(object):
    def __init__(self,jiraname,jira_sheetname):
        self.jiraname = jiraname
        self.jira_sheetname=jira_sheetname


    def project_if_exist(self):
        path = Filepath()
        summarypath = path.summary_report()
        xls = xlrd.open_workbook(summarypath, formatting_info=True)
        newxls = copy(xls)
        existproject = xls.sheet_names()
        if self.jiraname in existproject:
            print("表格中该项目已创建")
            return True

        else:
            print("表格中没有这个项目,需要新建")
            new_project_sheet = newxls.add_sheet(self.jiraname)
            # newxls.save('C:\\Users\\test\\Desktop\\Bug_info_check.xls')
            newexistproject = xls.sheet_names()
            # print(newexistproject)  # 获取所有sheet名称

            # 需要添加一些表头信息
            # 创建样式
            style = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()
            font.name = 'Arial'
            font.bold = True  # 加粗
            # TODO 单元格颜色填充的，后面再补充
            # pattern = xlwt.Pattern()
            # pattern.pattern = xlwt.Pattern.SOLID_PATTERN
            # pattern.pattern_fore_colour = 5
            style.font = font  # 设定样式
            # style.pattern = pattern

            new_project_sheet.write(0, 0, '项目名称', style)  # 加样式
            new_project_sheet.write(0, 1, self.jira_sheetname, style)
            new_project_sheet.write(1, 0, 'JIRA ID', style)
            new_project_sheet.write(1, 1, '创建时间', style)
            new_project_sheet.write(1, 2, '解决时间', style)
            new_project_sheet.write(1, 3, '问题状态', style)
            new_project_sheet.write(1, 4, '责任人', style)
            new_project_sheet.write(1, 5, '已检查到', style)
            new_project_sheet.write(2, 5, self.jiraname + '-1')  #从项目的第一个jiraid开始检查
            new_project_sheet.write(1, 6, '解决时间', style)

            # newxls.save('C:\\Users\\test\\Desktop\\Bug_info_check.xls')
            newxls.save(summarypath)
            return False


    def latest_id(self):
        path = Filepath()
        summarypath = path.summary_report()
        xls = xlrd.open_workbook(summarypath, formatting_info=True)
        existproject = xls.sheet_names()
        project_sheet_index = existproject.index(self.jiraname)  # 获取projectjiraid在sheet表中的index序列号值
        project_name = xls.sheet_by_name(xls.sheet_names()[project_sheet_index])  # 提取这个序号值对应的sheet的名称
        print('当前表格名称：' + str(project_name.name), '行数：' + str(project_name.nrows), '列数：' +str(project_name.ncols))

        latestid = project_name.cell(project_name.nrows - 1, 5)  # 最后一行最后一个
        latestidType = latestid.ctype
        #单元格的数据类型有5种：
        #0：empty
        #1：string
        #2：number
        #3：date
        #4：boolean
        #5：error
        print("最后一行最后一个单元格类型：" + str(latestidType))
        if latestidType == 6 or latestidType == 0:
            print('"最后一行最后一个单元格为空')
            latestid = project_name.cell(project_name.nrows - 1, 0)  # 最后一行第一个 行号要-1
            latestidType = latestid.ctype
            print("最后一行第一个单元格类型：" + str(latestidType))
        search_last_checkid = re.search(r'(?<=-)\d+', str(latestid))  #匹配表格中GGXB-4423中-后面的部分
        if search_last_checkid:
            lastcheck_idnumber=search_last_checkid.group()#如GGXB-4423,提取4423这部分
            return int(lastcheck_idnumber)
        else:
            print("获取上一次检查的最后一个id匹配失败")

    def latest_nrows(self):
        path = Filepath()
        summarypath = path.summary_report()
        xls = xlrd.open_workbook(summarypath, formatting_info=True)
        existproject = xls.sheet_names()
        project_sheet_index = existproject.index(self.jiraname)  # 获取projectjiraid在sheet表中的index序列号值
        project_name = xls.sheet_by_name(xls.sheet_names()[project_sheet_index])  # 提取这个序号值对应的sheet的名称
        return int(project_name.nrows)