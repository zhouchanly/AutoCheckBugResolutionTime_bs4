import os
import time
import xlrd
import xlwt
from xlutils.copy import copy


class Singlereport(object):
    def __init__(self):
        pass
    # def create_write_report(self,path,sheetname,shuzu):
    def create_write_report(self, path,sheetname,jiraid,nonconformityitem, responsible):
        # print('path='+str(path))
        if os.path.isfile(path): #中断，文件存在，需要累计进去
            xls = xlrd.open_workbook(path, formatting_info=True)
            sheet = xls.sheet_by_name(sheetname)
            nrows = sheet.nrows
            newxls = copy(xls)
            existsheet = xls.sheet_names()  # 获取所有工作表名
            project_sheet_index = existsheet.index(sheetname)  # 获取表的序列号
            project_sheet = newxls.get_sheet(project_sheet_index)
            project_sheet.write(nrows, 0, jiraid)
            project_sheet.write(nrows, 1, nonconformityitem)
            project_sheet.write(nrows, 2, responsible)
            project_sheet.write(nrows, 3, time.strftime("%Y/%m/%d"))
            newxls.save(path)
        else:#路径是文件夹，判断路径是文件用os.path.isfile(i)
            work_book = xlwt.Workbook(encoding='utf-8')
            newsheet = work_book.add_sheet(sheetname)
            #TODO 写入结果,第一次创建，表格都是空的，肯定要写表头
            style = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()
            font.name = 'Arial'
            font.bold = True  # 加粗
            style.font = font  # 设定样式
            newsheet.write(0, 0, 'JIRA ID', style)
            newsheet.write(0, 1, '不符合项', style)
            newsheet.write(0, 2, '责任人', style)
            newsheet.write(0, 3, '检查时间', style)
            #TODO 写入不符合项
            newsheet.write(1, 0, jiraid)
            newsheet.write(1, 1, nonconformityitem)
            newsheet.write(1, 2, responsible)
            newsheet.write(1, 3, time.strftime("%Y/%m/%d"))
            work_book.save(path)

        # else:
        #     print('路径有问题')


    def write_report(self):
        pass


# sheetname = time.strftime("%Y-%m-%d", time.localtime()) + ' jira Bug内容规范检查.xls'
# # sheetname='\\Users\\test\\PycharmProjects\\AutoCheckBugInformation\\2020-10-15 jira Bug内容规范检查.xls'
# curPath = os.path.dirname(os.path.realpath(__file__))
# print(curPath)
# singlereport_path = os.path.join(curPath, sheetname)
#
# sz=[111,'aa','xiaomign ']
# p = (singlereport_path,sheetname)
# s=Singlereport()
# s.create_write_report(p,sz)

# j='C:\/Users\/test\PycharmProjects\AutoCheckBugInformation'
# i='C:\/Users\/test\PycharmProjects\AutoCheckBugInformation\/2020-10-16 jira Bug内容规范检查.xls'
# print(os.path.exists(i))
# print(os.path.isdir(sheetname))
# print(os.path.isfile(sheetname))
