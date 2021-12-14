import xlrd
from xlutils.copy import copy
from filepath import Filepath

class Review(object):
    def __init__(self):
        pass
    def get_review_url(self,jiraname):
        position={}
        path = Filepath()
        summarypath = path.summary_report()
        xls = xlrd.open_workbook(summarypath, formatting_info=True)
        review_project = xls.sheet_by_name(jiraname)
        review_project_nrows = review_project.nrows
        review_project_ncols = review_project.ncols
        print('整张表格的行数='+str(review_project_nrows)+'，整张表格的列数='+str(review_project_ncols))
        print(review_project.cell_value(2, 0))
        if review_project.cell_value(2, 0) != '' and review_project.cell_value(2, 1) != '' and review_project.cell_value(2, 2) != '':
            #TODO
            num = int((review_project_ncols - 7) / 5)
            print("num=" + str(num))
            if num == 0:  # 第一次检查，那就全部按照这些行检查一遍---那就返回全部的jiraid---urllist
                print('第一次复查')
                result_position_ncols = 8
                for row in range(2, review_project_nrows):
                    non_comfority_id = review_project.cell_value(row, 0)
                    position.update({non_comfority_id:(row,result_position_ncols)})  #如'APP-125': (3, 23)，'APP-125'写在第3行，23列写本次的检查结果
                print(position)
            else:  # 第N次检查
                print('第'+str(num+1)+'次复查')
                check_cols = review_project_ncols - 4  #假设本次是第3次检查  check_cols为第2次的复查结果,列号
                check_cols_content = review_project.col_values(check_cols)  # 复查的倒数第一次的内容
                print(check_cols_content)
                print('check_cols_content的长度='+str(len(check_cols_content)))

                for i in range(2, len(check_cols_content)): #i表示行号
                    mark_position_ncols = review_project.cell_value(i, 6)
                    print('第'+str(i+1)+'行的mark_position_ncols='+str(mark_position_ncols))
                    if mark_position_ncols == '': #第二次复查
                        if check_cols_content[i] == '':
                            if check_cols == 8:
                                result_position_ncols = 8
                                non_comfority_id = review_project.cell_value(i, 0)
                                position.update({non_comfority_id: (i, result_position_ncols)})
                            else:
                                print('标注位为空，第'+str(i)+"行不是第二次，有点问题")
                                for t in range(check_cols - 5, 7,-5):
                                    print("标注位为空，查看前几次的检查结果，前一次的列号 =" + str(t))
                                    front_check_cols_content = review_project.cell_value(i, t)  # 获取前一次的复查结果
                                    print('标志位空，前前次的结果='+str(front_check_cols_content))
                                    if front_check_cols_content == '不符合':
                                        print('标志位空，找到前几次中最近一次不符合的位置了')
                                        result_position_ncols = t + 5
                                        non_comfority_id = review_project.cell_value(i, 0)
                                        position.update({non_comfority_id: (i, result_position_ncols)})
                                        print('找到前几次的检查结果了，这里的break好像有问题')
                                        break
                                    elif t == 8 and front_check_cols_content == '':   #会出现进行好几遍复查了，但是有些问题一次都还没有进行过复查的情况，就是标志位也是空的，后面的检查都是空的
                                        result_position_ncols = 8
                                        non_comfority_id = review_project.cell_value(i, 0)
                                        position.update({non_comfority_id: (i, result_position_ncols)})
                                        print('第'+str(num+1)+'次复查,但改问题才进行第一次复查')
                    elif mark_position_ncols == '需要':
                        if check_cols_content[i] == '':
                            # TODO 以下这段还要造数据验证一下
                            for t in range(check_cols - 5, 7, -5): #for t in range(check_cols - 5, 8, -5)这个里面要写7，不能写8，这个范围是版包含的关系[起点，终点）这样的形式
                                print("查看前一次的检查结果，前一次的列号 ="+str(t))
                                front_check_cols_content = review_project.cell_value(i, t)  # 获取前一次的复查结果
                                if front_check_cols_content == '不符合':
                                    result_position_ncols = t+5
                                    non_comfority_id = review_project.cell_value(i, 0)
                                    position.update({non_comfority_id: (i, result_position_ncols)})
                                    print('需要，不符合，找到位置了')
                                    break
                        elif check_cols_content[i] == '不符合':
                            print('需要，不符合')
                            result_position_ncols = 7+2+num*5-1
                            non_comfority_id = review_project.cell_value(i, 0)
                            position.update({non_comfority_id: (i, result_position_ncols)})
                        else:
                            print('符合，不用检查了')

                    else:
                        print("不需要复查")
            return position
            #TODO
        else:
            print('首行为空，不复查！')
            return False


    def review_bug_nonconformity(self,jiraname,write_rows,write_cols,result,nonconformityitem, responsible, checktime):
        path = Filepath()
        summarypath = path.summary_report()
        xls = xlrd.open_workbook(summarypath, formatting_info=True)
        newxls = copy(xls)
        existproject = xls.sheet_names()  # 获取所有工作表名
        project_sheet_index = existproject.index(jiraname)  # 获取表的序列号
        project_sheet = newxls.get_sheet(project_sheet_index)  # 使用获取到的序列号提取复制的新的newxls中对应的表格


        project_sheet_old = xls.sheet_by_name(jiraname)
        try:
            if project_sheet_old.cell_value(1, write_cols) == '':
                project_sheet.write(1, write_cols, '第' + str(int((write_cols - 8) / 5) + 1) + '次复查结果')
        except IndexError:  # 第一次复查的情况 get_ncols=6,write_cols=8  但整张表的列数只有6行，这种情况下读第8行就会出错
            project_sheet.write(1, write_cols, '第' + str(int((write_cols - 8) / 5) + 1) + '次复查结果')

        try:
            if project_sheet_old.cell_value(1, write_cols + 1) == '':
                project_sheet.write(1, write_cols + 1, '不符合项')
        except IndexError:
            project_sheet.write(1, write_cols + 1, '不符合项')

        try:
            if project_sheet_old.cell_value(1, write_cols + 2) == '':
                project_sheet.write(1, write_cols + 2, '责任人')
        except IndexError:
            project_sheet.write(1, write_cols + 2, '责任人')

        try:
            if project_sheet_old.cell_value(1, write_cols + 3) == '':
                project_sheet.write(1, write_cols + 3, '复查时间')
        except IndexError:
            project_sheet.write(1, write_cols + 3, '复查时间')

        try:
            if project_sheet_old.cell_value(1, 6) == '':
                project_sheet.write(1, 6, '是否需要复查')
        except IndexError:
            project_sheet.write(1, 6, '是否需要复查')


        if result =='不符合':
            project_sheet.write(write_rows, write_cols, result)
            project_sheet.write(write_rows, write_cols+1, nonconformityitem)
            project_sheet.write(write_rows, write_cols+2, responsible)
            project_sheet.write(write_rows, write_cols+3, checktime)
            project_sheet.write(write_rows, 6, '需要')  #第7列的标注位
        elif result == '符合':
            project_sheet.write(write_rows, write_cols, result)
            project_sheet.write(write_rows, write_cols + 1, '/')
            project_sheet.write(write_rows, write_cols + 2, '/')
            project_sheet.write(write_rows, write_cols + 3, checktime)
            project_sheet.write(write_rows, 6, '不需要')   #第7列的标注位
        newxls.save(summarypath)

