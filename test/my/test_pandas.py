import pandas as pd

titles=['name','password']
df=pd.concat([pd.Series(['aaa','bbb','ccc']),pd.Series(['123456','sdfdgf','dfdfdf'])],axis=1)
df.columns=titles
kk=df[(df['name']=='aaa')&(df['password']=='12456')]
if kk.empty:
    print('no')
