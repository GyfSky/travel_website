import numpy as np
from flasker.user_pkg.UserClass import User
from werkzeug.security import generate_password_hash, check_password_hash

def view_all(POOL):
    db = POOL.connection()
    cursor = db.cursor()

    sql = "SELECT * FROM node"  # sql命令
    cursor.execute(sql)  # 执行sql语句
    result = cursor.fetchall()  # 获取查询结果

    cursor.close()
    db.close()

    return result

def get_all_table(name,POOL):
    db = POOL.connection()
    cursor = db.cursor()

    sql = "SELECT * FROM " + name
    cursor.execute(sql)
    results = cursor.fetchall()

    cursor.close()
    db.close()

    return results, [desc[0] for desc in cursor.description]


# ---------------------------------------------------- 用户信息 ------------------------------------------------------------
# 空值处理
def is_null(username, password):
    if username == '' or password == '':
        return True
    else:
        return False


# 用户存在
def exist_user(username,POOL):
    db = POOL.connection()
    cursor = db.cursor()

    sql = "SELECT * FROM users WHERE user_name ='%s'" % (username)
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    db.close()

    if len(result) == 0:
        return False
    else:
        return True

def search_user(usn,pwd,POOL):
    db=POOL.connection()
    cursor=db.cursor()

    sql = "SELECT * FROM users WHERE user_name ='%s'" % usn
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    db.close()

    if validate_password(result[0][2],pwd):
        user=User(result[0][0],result[0][1],result[0][2],result[0][3],result[0][4],result[0][5],result[0][6],result[0][7],result[0][8],result[0][9])
        return True,user
    else:
        return False,[]

# 添加新用户
def add_user(username, password,POOL):
    db=POOL.connection()
    cursor=db.cursor()

    password_hash = set_password(password)

    sql = "INSERT INTO users(user_name, password) VALUES ('%s','%s')" % (username, password_hash)  # sql命令
    cursor.execute(sql)  # 执行sql语句
    db.commit()

    cursor.close()
    db.close()

    print("已成功添加用户名为{0}的新用户".format(username))


# 获取用户信息
def get_user_msg(username):
    pass

def set_password(password):  # 用来设置密码的方法，接受密码作为参数
    password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段
    return password_hash

def validate_password(password_hash,password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(password_hash, password)  # 返回布尔值


# ---------------------------------------------------- 景点信息 ------------------------------------------------------------


# 获取景点信息
def get_spot_msg(spot_id,POOL):
    db=POOL.connection()
    cursor=db.cursor()

    sql = "select * from node where id=%s" % spot_id  # 获取景点信息
    cursor.execute(sql)
    result = cursor.fetchone()

    cursor.close()
    db.close()

    index = get_index_by_id(spot_id,POOL)
    id = result[0]
    name = result[1]
    is_open = result[2]
    price = result[4]
    introduction = result[5]
    score = float(result[6])
    spot_type = result[7]
    people = result[8]
    return [name, index, id, introduction, spot_type, price, score, people, is_open]


# 获得两个景点间的距离
def get_distance(start_spot_id, end_spot_id,POOL):
    db=POOL.connection()
    cursor=db.cursor()

    sql = "select distance from edge where from_id = '%s' and to_id ='%s'" % (start_spot_id, end_spot_id)
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    db.close()

    if result:
        return result[0][0]
    else:
        return None


# 获得景点人数并设置等级(当前人数/可容纳人数，向上取整，1~10级），返回一行等级列表
def get_people_level():
    pass


# 根据景点id得到景点索引
def get_index_by_id(spot_id,POOL):
    db=POOL.connection()
    cursor=db.cursor()

    sql = """
    SELECT position FROM (
        SELECT id, @rownum := @rownum + 1 AS position
        FROM node, (SELECT @rownum := 0) r
        ORDER BY id
    ) AS numbered_rows
    WHERE id = %s
    """
    cursor.execute(sql, (spot_id,))
    row = cursor.fetchone()

    cursor.close()
    db.close()

    return int(row[0] - 1)


# 根据索引获得景点id
def get_id_by_index(spot_index,POOL):
    db=POOL.connection()
    cursor=db.cursor()

    # 确保index是整数
    index = int(spot_index)
    # 使用参数化的方式进行查询
    sql = "SELECT * FROM node ORDER BY id LIMIT 1 OFFSET %s"
    cursor.execute(sql, (index,))
    result = cursor.fetchall()
    result = result[0][0]

    cursor.close()
    db.close()

    return result


# 获取某个兴趣类型所有景点的id
def get_spot_id_by_type(spot_type,POOL):
    db=POOL.connection()
    cursor=db.cursor()

    sql = "SELECT id FROM node WHERE class LIKE %s"
    pattern = "%" + spot_type + "%"
    cursor.execute(sql, (pattern,))
    result = cursor.fetchall()

    cursor.close()
    db.close()

    spot_id_list = []
    for i in result:
        spot_id_list.append(i[0])
    return spot_id_list


def get_spot_index_by_type(spot_type):
    spot_id_list = get_spot_id_by_type(spot_type)
    spot_index_list = [get_index_by_id(i) for i in spot_id_list]
    return spot_index_list

def get_spot_id_by_name(spot_name,POOL):
    db=POOL.connection()
    cursor=db.cursor()

    sql = "SELECT id FROM node WHERE name = %s"
    cursor.execute(sql, (spot_name,))
    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result[0]


# 获取某个id的景点名字
def get_spot_name_by_id(spot_id,POOL):
    db=POOL.connection()
    cursor=db.cursor()

    sql = "SELECT name FROM node WHERE id = %s" % spot_id
    cursor.execute(sql)
    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result[0]


# 获取景点评分
def get_spot_score(spot_id,POOL):
    db=POOL.connection()
    cursor=db.cursor()

    sql = 'SELECT recommendation FROM node WHERE id = %s' % spot_id
    cursor.execute(sql)
    result = cursor.fetchone()

    cursor.close()
    db.close()

    return result[0]


# 获取所有景点的名字(返回根据索引顺序的景点名字列表）
def get_all_spots_name():
    pass


# 获得邻接矩阵（关闭的景点不能设为MAX = float('inf')）
def get_adjacent_matrix(POOL):
    db=POOL.connection()
    cursor=db.cursor()

    cursor.execute("SELECT id FROM node ORDER BY id DESC LIMIT 1;")
    last_row = cursor.fetchone()

    cursor.close()
    db.close()

    end_index = get_index_by_id(last_row[0],POOL)
    start_index = 0
    index_range = end_index - start_index + 1
    adjacent_matrix = np.full(shape=(index_range, index_range), fill_value=np.inf)
    # 要根据索引获得对应的id，然后再根据景点id获得对应的距离
    for i in range(index_range):
        start_id = get_id_by_index(i,POOL)
        for j in range(index_range):
            end_id = get_id_by_index(j,POOL)
            if get_distance(start_id, end_id,POOL):
                adjacent_matrix[i][j] = get_distance(start_id, end_id,POOL)
    return adjacent_matrix
