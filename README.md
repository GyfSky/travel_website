<h1 align="center">旅游景点智能导览系统</h1>
<p align="center" style="margin-bottom:16px;">
    <img src="https://img.shields.io/badge/Flask-blue" />
    <img src="https://img.shields.io/badge/MySQL-red" />
    <img src="https://img.shields.io/badge/Node.js-green" />
    <img src="https://img.shields.io/badge/Python-yellow" />
</p>

## 项目介绍
旅游景点智能导览系统，旨在通过现代技术手段，为游客提供全
面、便捷、智能的导览服务。平台集成了地图服务、景点介绍、路线
推荐等功能，帮助游客更好地规划行程，提高旅游体验。

## 主要功能模块
1.用户管理模块：包括用户注册、登录等功能。
2.地图服务模块：集成高德地图API，实现地图显示、景点标记、路
线规划等功能。
3.景点推荐模块：根据用户偏好，推荐旅游景点，并提供各个景点的
详细介绍及图片展示
4.路径规划模块：根据推荐数据结合用户兴趣、消费偏好等需求规划
最优观光路线

## 项目分工
巩一凡：推荐算法，后端框架，部分数据收集及前端通信
李志帆：路径规划算法，连接数据库及读取数据
于清栋：前端页面编写，前端通信
林宇鸣：数据库搭建

## 项目结构描述
├─7_22_less_users.sql  //数据库相关文件
├─7_22_more_users_normal_distribution.sql
│
├─final
│  ├─web.py            //启动文件
│  │
│  ├─flasker
│  │  ├─database       //数据库读写相关文件
│  │  ├─manage_pkg     //人流量生成相关文件
│  │  ├─routing_pkg    //路径规划算法相关文件
│  │  ├─spot_pkg       //推荐算法及景点相关文件
│  │  └─user_pkg       //用户相关文件
│  │
│  ├─static
│  │  ├─css            //CSS文件
│  │  ├─data
│  │  ├─fonts
│  │  ├─img            //图片文件
│  │  ├─js             //JS文件
│  │  └─video          //视频文件
│  └─templates         //HTML文件
│
└─test                 //测试文件
    ├─my
    └─teammate

## 项目部署
1.将sql文件导入本地数据库中
2.更改final/web.py文件中关于数据库的配置
3.将final/templates/index_forth.html中的line40,line43改为自己高德地图JS api 中的安全密钥和key
4.启动web.py文件
5.用户默认密码为123456_1


# 个人更改内容更新
v1.0.0 //小组最终版本
v1.0.1 //增加哈希密码生成及验证
