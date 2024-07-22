import requests
import json
import pandas as pd
location=['杭州西湖风景名胜区-梅家坞', '真际院', '梅坞春早', '瞭望亭', '九溪十八涧', '理安寺', '梵音亭', '杭州西湖风景名胜区-九曲亭', '杭州西湖风景名胜区-龙井八景', '杭州西湖风景名胜区-杨梅岭', '杭州动物园', '虎跑公园', '六和塔文化公园', '纯阳殿', '古香禅院', '杭州永福寺', '灵隐飞来峰', '济公殿', '史量才墓', '徐锡麟烈士墓', '杭州西湖风景名胜区-秦亭', '美女山', '灵峰探梅', '杭州西湖风景名胜区-状元峰', '漱碧', '凉亭', '杭州植物园', '桃源李社', '撷翠亭', '树木园', '双峰插云', '树木园', '竹类植物区', '曲院风荷', '郭庄景点', '神舟基地', '美景房车茅家埠营地', '704工程', '杭州西湖风景名胜区-于谦墓', '艺人盖叫天墓', '景行古桥', '芍药圃', '东坡亭', '一炽松树', '九曜阁', '太子湾公园', '大风车', '魏源墓', '挹江亭', '雷峰塔景区', '苏堤', '锁澜桥', '压堤桥', '东浦桥', '钱塘苏小小之墓', '紫云洞', '黄龙吐翠', '宝石山', '北街寻梦', '云水光中', '白堤', '平湖秋月', '海娃塑像', '沙孟海旧居', '音乐喷泉观赏区', '西湖外事游船', '淑影桥', '涌金公园', '钱王祠', '柳浪闻莺公园', '学士公园', '华君武', '环翠楼', '紫阳街道游客服务中心', '玄朗洞', '万松书院', '杭州宣和美术馆', '凤凰山上凤凰亭', '圣果寺遗址', '宋韵文化园', '将台山', '玉皇山景区', '石龙洞造像', '西湖风景名胜区-海月亭', '郊坛下和老虎洞窑址']
lon=[]
lat=[]
titles=['location','latitude','longitude']
def get_location_coordinates(address_name, ak):
    # 构造请求URL
    url = f"https://api.map.baidu.com/geocoding/v3/?address={address_name}&output=json&ak={ak}&city=太原市"
    
    # 发送HTTP GET请求
    response = requests.get(url)
    
    # 解析响应数据
    data = json.loads(response.text)
    
    # 获取并返回经纬度
    if data['status'] == 0:  # 检查状态码是否为0，表示成功
        result = data['result']
        location = result['location']
        return location['lat'], location['lng']
    else:
        return None, None  # 如果失败，返回None

# 使用函数
# if __name__ == "__main__":
#     ak = "your BaiDu ak"
#     for i in location:
#         latitude, longitude = get_location_coordinates('西湖'+i, ak)
#         lat.append(latitude)
#         lon.append(longitude)
#     df=pd.concat([pd.Series(location),pd.Series(lat),pd.Series(lon)],axis=1)
#     df.columns=titles
#     df.to_csv('location.csv')
                 
if __name__ == "__main__":
    ak = "your BaiDu ak"
    latitude, longitude = get_location_coordinates("杭州市凤凰山与九华山山谷内 郊坛下和老虎洞窑址", ak)
    print(latitude, longitude)