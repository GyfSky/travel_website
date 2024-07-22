import numpy as np

class KalmanFilter1D:
    def __init__(self, initial_state, initial_covariance, process_variance, measurement_variance):
        self.state = initial_state
        self.covariance = initial_covariance
        self.Q = process_variance  # 过程噪声协方差
        self.R = measurement_variance  # 测量噪声方差

    def predict(self):
        # 预测步骤，假设过程模型为恒速模型
        A = 1  # 状态转移矩阵
        self.state = A * self.state
        self.covariance = A * self.covariance * A + self.Q

    def update(self, measurement):
        # 更新步骤
        H = 1  # 测量矩阵，假设直接测量物理量
        y = measurement - H * self.state
        S = H * self.covariance * H + self.R
        K = self.covariance * H / S
        
        # 更新状态和协方差
        self.state = self.state + K * y
        self.covariance = (1 - K * H) * self.covariance

    def get_state(self):
        return self.state


# 示例用法
initial_state = 0
initial_covariance = 0.1  # 初始协方差
process_variance = 1e-5  # 过程噪声方差
measurement_variance = 0.1  # 测量噪声方差

# 创建卡尔曼滤波器对象
kf = KalmanFilter1D(initial_state, initial_covariance, process_variance, measurement_variance)

# 假设有两组测量数据
m1=[('4', 1.0), ('5', 0.0), ('6', 0.0)]
m2=[('4', 0.5), ('5', 0.375), ('6', 0.375)]
measurements1 = [i[1] for i in m1]
measurements2 = [i[1] for i in m2]

# 在每个时间步更新卡尔曼滤波器
for i in range(len(measurements1)):
    kf.predict()
    measurement_combined = (measurements1[i] + measurements2[i]) / 2.0  # 假设简单地取平均作为融合测量值
    kf.update(measurement_combined)
    
    # 获取滤波后的状态
    filtered_state = kf.get_state()
    print(f"Filtered state after step {i+1}: {filtered_state}")