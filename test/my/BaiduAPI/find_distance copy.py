import requests
import pandas as pd
def get_info(start,end,ak):
    url = 'https://api.map.baidu.com/directionlite/v1/walking?origin=' + start + '&destination=' + end + '&ak=' + ak + '&coord_type=wgs84'
    response = requests.get(url)
    answer = response.json()
    if answer["status"] == 0:
        get_distance = answer['result']['routes'][0]['distance']
        get_time = answer['result']['routes'][0]['duration']
    else:
        get_distance =0
        get_time=0
    print(answer)
    return get_distance,get_time

# # 保存数据
ak="your BaiDu ak"

# distance,time=get_info('30.251908040926853,120.166689977221','30.25190827490253,120.16639578216648',ak)
# print(distance)

r_time,r_distance,r_start,r_end=[],[],[],[]

df=pd.read_csv('location.csv')
name=df['location']
longitude=df['longitude']
latitude=df['latitude']
titles=['from','to','distance','time']
for i in range(4):
    for j in range(4):
        if i<j:
            start=str(latitude[i]) + ',' + str(longitude[i])
            end= str(latitude[j]) + ',' + str(longitude[j]) 
            distance,time=get_info(start,end,ak)
            r_time.append(time)
            r_distance.append(distance)
            r_start.append(name[i])
            r_end.append(name[j])
df=pd.concat([pd.Series(r_start),pd.Series(r_end),pd.Series(r_distance),pd.Series(r_time)],axis=1)
df.columns=titles
df.to_csv('distance.csv')

