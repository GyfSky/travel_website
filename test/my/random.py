import numpy as np
import time
data=[]
sleep_time=6
def generate_normal_random():
    while True:
        u1 = np.random.rand()
        u2 = np.random.rand()
        
        z0 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
        
        # 将 z0 映射到 (0, 1) 区间
        if 0.01 < z0 < 1:
            return z0

# 测试生成 10 个符合正态分布的随机数
for _ in range(30):
    data.append(float(generate_normal_random()))
print(data)
max=1
min=0
while True:
    for index, value in enumerate(data):
        diff=np.random.normal(0, 0.5, 10)[0]*0.1
        new_value = value + diff
        if new_value > max:
            new_value -= diff
            new_value -= 0.04
        elif new_value < min:
            new_value -= diff
            new_value += 0.04
        data[index] = float(new_value)
    print(data)
    time.sleep(sleep_time)




