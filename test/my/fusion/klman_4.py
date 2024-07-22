import numpy as np

class KalmanFilter2D:
    def __init__(self, initial_state, initial_covariance, process_covariance):
        self.state = initial_state
        self.covariance = initial_covariance
        self.Q = process_covariance  # 过程噪声协方差

    def predict(self):
        # 预测步骤，假设过程模型为恒速模型
        A = np.array([[1, 1],
                      [0, 1]])
        self.state = np.dot(A, self.state)
        self.covariance = np.dot(A, np.dot(self.covariance, A.T)) + self.Q

    def update(self, measurement, H, R):
        # 更新步骤
        y = measurement - np.dot(H, self.state)
        S = np.dot(H, np.dot(self.covariance, H.T)) + R
        K = np.dot(self.covariance, np.dot(H.T, np.linalg.inv(S)))
        
        # 更新状态和协方差
        self.state = self.state + np.dot(K, y)
        self.covariance = self.covariance - np.dot(K, np.dot(H, self.covariance))

    def get_state(self):
        return self.state


# 示例用法
initial_position = 0
initial_velocity = 0
initial_state = np.array([initial_position, initial_velocity])
initial_covariance = np.eye(2) * 0.1  # 初始协方差矩阵
process_covariance = np.eye(2) * 1e-5  # 过程噪声协方差矩阵

# 创建卡尔曼滤波器对象
kf = KalmanFilter2D(initial_state, initial_covariance, process_covariance)

# 测量矩阵 H （假设是单位矩阵）
H = np.eye(2)

# 定义测量噪声协方差 R
measurement_covariance1 = 0.1
measurement_covariance2 = 0.2

# 在每个时间步更新卡尔曼滤波器
num_samples = 10
for i in range(num_samples):
    kf.predict()
    # 假设有两组测量数据 measurement1 和 measurement2
    measurement1 = np.random.randn(2, 1) * measurement_covariance1
    measurement2 = np.random.randn(2, 1) * measurement_covariance2
    measurement_combined = (measurement1 + measurement2) / 2.0
    
    # 定义测量噪声协方差 R
    R = H @ Q @ H.T

    # 更新卡尔曼滤波器
    kf.update(measurement_combined, H, R)
    
    # 获取滤波后的状态
    filtered_state = kf.get_state()
    print(f"Filtered state after step {i+1}: {filtered_state}")