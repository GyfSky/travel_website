from flask_login import login_required, logout_user
from flask_login import login_user
from flask_login import LoginManager
from flask import Flask,request,flash,redirect,url_for,render_template
from flask_login import UserMixin


class User(UserMixin):
    is_authenticated=False
app = Flask(__name__)
login_manager = LoginManager(app)
User={'1':'dfsf',"password":'12345'}


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.get(user_id) # 用 ID 作为 User 模型的主键查询对应的用户
    return user 


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User
        # 验证用户名和密码是否一致
        if username == user['1'] and user['passsword']==password:
            login_user(user)  # 登入用户
            return redirect(url_for('index'))  # 重定向到主页

        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')

@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index')) 
app.run()