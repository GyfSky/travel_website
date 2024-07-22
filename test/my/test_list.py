from Sql import *
db=Mysql()
cursor=db.cursor
table,jjj=get_all_table('node')
with open('text03.txt','a',encoding='utf-8') as file_read:
    for i in range(len(table)):
        # sq=table[i][1]
        sq='<li><input type="checkbox" '+'id="a'+str(i+1)+'" /><label for="a'+str(i+1)+'">'+table[i][1]+"</label></li>"
        file_read.write(sq+'\n')
        # print(sq)
