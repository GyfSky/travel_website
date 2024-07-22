import requests

ak="your BaiDu ak"
start1='30.228932114135855,120.12792000971587'
end1='30.230587634882042,120.12022431624243'
start2='37.87698902884778,112.55639149167204'
end2='30.07942308505079,119.91418240684366'
url1='http://api.map.baidu.com/routematrix/v2/walking?'+'origins='+start1+'&destinations='+end1+'&output=json&ak='+ak
url2='https://api.map.baidu.com/directionlite/v1/driving?'+'origin='+start1+'&destination='+end1+'&output=json&ak='+ak
response = requests.get(url1)
answer = response.json()
print(answer)