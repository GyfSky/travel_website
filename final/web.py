import threading
from dbutils.pooled_db import PooledDB
import pymysql
import time

from flask import Flask, render_template,url_for,request,redirect,flash,make_response,jsonify
from flask_login import login_user,LoginManager,UserMixin,login_required, logout_user,current_user
from flask_cors import CORS

from flasker.user_pkg.UserClass import *
from flasker.database.database_link import *
from flasker.spot_pkg.recommendation import recom_fresh
from flasker.routing_pkg.routing import get_path,recommend_route,select_route
from flasker.manage_pkg.random_people import generate_and_update_data


app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
app.config['SECRET_KEY'] = 'dev'
CORS(app)
lock = threading.Lock()
final_reco={}
POOL=PooledDB(creator=pymysql,#数据库类型
                maxconnections=10,  
                mincached=2,  
                maxcached=3,
                blocking=True,
                ping=0,
                setsession=[],
                host='127.0.0.1',
                user='root',
                password='',
                database='guide'
            )


@login_manager.user_loader
def load_user(user_id):
    db=POOL.connection()
    cursor=db.cursor()
    sql = "SELECT * FROM users WHERE user_name ='%s'" % (user_id)  
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    user=User(result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8],result[0][9])
    return user


class User(User,UserMixin):
    @property
    def id(self):
        return self.username


@app.route('/')
def index():
    return render_template('index_first.html')


@app.route('/second')
@login_required
def second():
    return render_template('index_second.html')


@app.route('/third')
@login_required
def third():
    return render_template('index_third.html')

@app.route('/forth/')
@login_required
def forth():
    print(final_reco)
    if final_reco=={}:
        results=recom_fresh(POOL)
    else:
        results=[int(i[8:11]) for i in final_reco]#只包含名称的列表
    # print(results)
    results=[i for i in results if i!=205 and i!=175 and i!=208 ]
    results=[get_spot_msg(i,POOL) for i in results]
    return render_template('index_forth.html',spots=results[0:9])


@app.route('/login', methods=['GET', 'POST','OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # 处理OPTIONS请求，可以在这里设置允许的头部、方法等
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    if request.method == 'POST':

        username=request.form.get("username")
        password=request.form.get("password")

        if not username or not password:
            flash ('用户名或密码不能为空')
            return redirect(url_for('index'))
        
        if_exit,ustem = search_user(username,password,POOL)
        # 验证用户名和密码是否一致
        if if_exit:
            user=User(ustem.se_id,username,ustem.password,ustem.interest,ustem.min_consume,ustem.max_consume,ustem.min_distance,ustem.max_distance,ustem.min_score,ustem.max_score)
            login_user(user)  # 登入用户
            flash('登录成功')
            global user_final_name
            lock.acquire()
            user_final_name=username
            lock.release()
            return redirect(url_for('second'))  # 定向到用户主页

        flash ('用户名或密码错误')  
        return redirect(url_for('index'))
        
  
@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('欢迎下次使用')
    print(final_reco)
    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not password or not username:
            flash('用户名或密码不能为空')
            return redirect(url_for('index'))
        else:
            if not exist_user(username,POOL):
                add_user(username, password,POOL)
                flash('注册成功')
                return redirect(url_for('index'))
            else:
                flash('用户名已存在')
                return redirect(url_for('index'))


# @param 景点编号or名称
# @brief 更改景点属性
# @return 管理员总界面or编辑的界面
@app.route('/admin/edit/<int:spot_id>',
           methods=['GET', 'POST'])  # 另外一种?可能？https://127.xxx:5000/admin/edit?spot_id=xxx（函数不需要传参）
def edit(spot_id):
    if request.method == 'POST':
        title = request.form['title']  # 获得数据
        db = POOL.connection()
        cursor = db.cursor
        # 更新数据
        sql = "UPDATE EMPLOYEE SET AGE = '%s' WHERE SEX = '%c'" % ('dfs', 'M')
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.db.commit()
        except:
            # 发生错误时回滚
            db.rollback

        # 关闭数据库连接
        db.db.close()
        return redirect(url_for('admin'))

    return render_template('edit.html', movie='xxx')


# @param 景点名称及属性
# @brief 添加景点
# @return 管理员总界面or添加的界面
@app.route('/admin/add/', methods=['GET', 'POST'])
def add():
    db = POOL.connection()
    cursor = db.cursor
    if request.method == 'POST':
        title = request.form['title']  # 获得数据
        year = request.form['year']
        # 更新数据
        sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
       LAST_NAME, AGE, SEX, INCOME) \
       VALUES ('%s', '%s',  %s,  '%s',  %s)" % \
              ('Mac', 'Mohan', 20, 'M', 2000)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 执行sql语句
            db.db.commit()
        except:
            # 发生错误时回滚
            db.rollback
        db.db.close()
        return redirect(url_for('admin'))
    return render_template('edit.html', movie='xxx')


# @param 景点编号or名称
# @brief 删除景点
# @return 管理员总界面
@app.route('/admin/delete/<int:spot_id>', methods=['POST'])
def delete(spot_id):
    # 删除数据
    db = POOL.connection()
    cursor = db.cursor
    sql = "DELETE FROM EMPLOYEE WHERE id == %s" % (spot_id)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 执行sql语句
        db.db.commit()
    except:
        # 发生错误时回滚
        db.rollback

    db.db.close()
    return redirect(url_for('admin'))

def recom_silent():
    from flasker.spot_pkg.recommendation import only_item_based,fina_recommendation
    while True:
        global final_reco
        try:
            results, headers = get_all_table('users',POOL)
            final_reco = fina_recommendation(results, len(headers), headers, user_final_name)
            print("sucess")
            break
        except:
            final_reco = {}
        time.sleep(2)


thread = threading.Thread(target=generate_and_update_data,args=(POOL,))
thread2 = threading.Thread(target=recom_silent)

thread.start()
thread2.start()


@app.route('/routing', methods=['POST'])
def routing():
    
    results = request.json
    print(results)
    interest = results['interests']
    if results['price'] is not None:
        consume = list(map(int, results['price'].split(',')))
    else:
        consume = None
    if results['rating'] is not None:
        score = list(map(float, results['rating'].split(',')))
    else:
        score = None
    if results['spots'] is not None and len(results['spots']) > 0:
        add_spot_indexs = [int(i.lstrip('a'))-1 for i in results['spots']]
        add_spot_ids = [get_id_by_index(i,POOL) for i in add_spot_indexs]
        print('add_spot_indexs:', add_spot_ids)
    else:
        add_spot_ids = []
    start_spot_name = results['start_end'][0]
    end_spot_name = results['start_end'][1]
    print('start_spot_name:', start_spot_name, 'end_spot_name:', end_spot_name)
    try:
        start_spot_id, end_spot_id = get_spot_id_by_name(start_spot_name,POOL), get_spot_id_by_name(end_spot_name,POOL)
    except:
        print('error:未输入起点或终点!!!')
        return jsonify(["请选择起点和终点"]), 400
    print('start_spot_id:', start_spot_id, 'end_spot_id:', end_spot_id, 'consume:', consume,
          'interest:', interest, 'score:', score)
    print("start_spot_id:", type(start_spot_id),
          "end_spot_id:", type(end_spot_id), "consume:", type(consume),
          "interest:", type(interest), "score:", type(score))

    # 判断选择根据用户兴趣推荐，还是根据选择推荐
    if len(interest) == 0 and score is None and consume is None:
        if final_reco =={}:
            return jsonify(["新用户需要自定义路线"])
        else:
            path = recommend_route(start_spot_id, end_spot_id,final_reco,POOL)
            final_path = get_path(path,POOL)
            print('final_path:', final_path)
            return_spots = []
            for i in final_path:
                return_spots.append({'keyword': i, 'city': '杭州'})
            return jsonify(return_spots)
    else:
        path = select_route(POOL,current_user.username, start_spot_id, end_spot_id, add_spot_ids, consume, interest,
                            score)
        final_path = get_path(path,POOL)
        print(final_path)
        return_spots = []
        for i in final_path:
            return_spots.append({'keyword': i, 'city': '杭州'})
        return jsonify(return_spots)


app.run(host='127.0.0.1', port=5000)
