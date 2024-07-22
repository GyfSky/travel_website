def loadData_item(files,n,name):
    data={}
    for line in files:
        data.setdefault(line[0],{})
        for i in range(1,n):
            if line[i]!=None:
                data[line[0]][name[i]]=line[i]
    return data

def loadData_user(files,n,name):
    data={}
    data_pl={}
    data_na={}
    for i in range(1,n-1):
        data_pl.setdefault(name[i+1],0)
        data_pl[name[i+1]]=i
        data_na.setdefault(i,0)
        data_na[i]=name[i+1]
    for line in files:
        data.setdefault(line[0],{})
        for i in range(2,n):
            if line[i]!=None:
                data[line[0]][data_pl[name[i]]]=line[i]
    return data,data_na

files=[('aaa','sdsdf',4.0,None),('ada','sdsdf',5.0,5.0),('adfa','sdsdf',4.3,5.0),('aas','sdsdf',4.8,5.0)]
n=4
name=['name','sdd','a','b']
ddd,data=loadData_user(files,n,name)
print(data)