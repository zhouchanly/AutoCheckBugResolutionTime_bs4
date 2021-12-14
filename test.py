import re
from datetime import datetime

a = "2020-12-02T11:47:59+0800"
b = "2020-12-02T11:57:59+0800"

# p = re.compile(r'.*T.*')
# print(p.findall(a))
# # pp = re.findall(".*T.*",a)
# # print (pp)
# out = re.sub(p,'\000',a)
# print(out)
#
# # print ('\000')#表示空格

# print(a.replace("T"," "))
a=a.replace("T"," ")
# print (a.replace("+0800"," "))

# print(b.replace("T"," "))
b=b.replace("T"," ")
# print (b.replace("+0800"," "))
# bb = "2020-12-02 11:57:59 "
# bb = datetime.strptime(bb, "%Y-%m-%d %X")
# print(bb)


p='2020-12-02 15:24:41'
p1 = datetime.strptime(p,"%Y-%m-%d %X" )
# print(p1)
# c=b-a
# print(c)


#方法二
(year,month,shuju) = p.split('-')
(day,shijian) = shuju.split(' ')
(shi,fen,miao) = shijian.split(':')
print(year,month,day,shi,fen,miao)
print(datetime(int(year),int(month),int(day),int(shi),int(fen),int(miao)))


