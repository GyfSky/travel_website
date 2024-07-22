import numpy as np
import time

def generate_normal_random():
    while True:
        u1 = np.random.rand()
        u2 = np.random.rand()
        z0 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
        # 将 z0 映射到 (0, 1) 区间
        if 0.01 < z0 < 1:
            return z0
        
def generate_and_update_data(POOL):
    sleep_time = 6
    data, spots = [], []
    max = 1
    min = 0

    db =POOL.connection()
    cursor = db.cursor()

    query = "SELECT name FROM node"
    try:
        cursor.execute(query)
        name = cursor.fetchall()
    except:
        # 发生错误时回滚
        db.rollback()

    cursor.close()
    db.close()
    
    for i in range(len(name)):
        data.append(float(generate_normal_random()))

    while True:
        for index, value in enumerate(data):
            diff = np.random.normal(0, 0.5, 10)[0] * 0.1
            new_value = value + diff
            if new_value > max:
                new_value -= diff
                new_value -= 0.04
            elif new_value < min:
                new_value -= diff
                new_value += 0.04
            data[index] = float(new_value)
            spots.append((float(new_value), name[index][0]))

        db =POOL.connection()
        cursor = db.cursor()
        update_sql = "UPDATE node SET capacity_rate = %s WHERE name = %s"
        
        try:
            cursor.executemany(update_sql, spots)
            db.commit()
        except:
            db.rollback()

        cursor.close()
        db.close()

        time.sleep(sleep_time)
