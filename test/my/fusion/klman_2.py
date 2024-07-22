import numpy as np
import matplotlib.pyplot as plt

class KalmanFilter2D:
    def __init__(self, initial_state, initial_covariance, process_covariance, measurement_covariance):
        self.state = initial_state
        self.covariance = initial_covariance
        self.process_covariance = process_covariance
        self.measurement_covariance = measurement_covariance

    def predict(self):
        # Prediction step (assuming constant velocity model)
        A = np.array([[1, 0, 1, 0],
                      [0, 1, 0, 1],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])  # State transition matrix for constant velocity
        self.state = np.dot(A, self.state)
        self.covariance = np.dot(A, np.dot(self.covariance, A.T)) + self.process_covariance

    def update(self, measurement):
        # Update step
        H = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0]])  # Measurement matrix
        measurement_residual = measurement - np.dot(H, self.state)
        S = np.dot(H, np.dot(self.covariance, H.T)) + self.measurement_covariance
        K = np.dot(self.covariance, np.dot(H.T, np.linalg.inv(S)))
        
        # Update state and covariance
        self.state = self.state + np.dot(K, measurement_residual)
        self.covariance = np.dot((np.eye(self.state.shape[0]) - np.dot(K, H)), self.covariance)

    def get_state(self):
        return self.state
    
# np.random.seed(0)
# num_samples = 50
# true_values = np.random.randn(2, num_samples)  # 真实状态变量 (2维)
# measurements = true_values + 0.1 * np.random.randn(2, num_samples)  # 模拟测量数据

# # 初始化卡尔曼滤波器
# initial_state = np.array([measurements[0, 0], measurements[1, 0], 0, 0])  # 初始状态
# initial_covariance = np.eye(4) * 0.1  # 初始协方差矩阵
# process_covariance = np.eye(4) * 1e-5  # 过程噪声协方差
# measurement_covariance = np.eye(2) * 0.1  # 测量噪声协方差
# kf = KalmanFilter2D(initial_state, initial_covariance, process_covariance, measurement_covariance)

# # 用卡尔曼滤波器处理数据
# filtered_states = []
# for i in range(num_samples):
#     kf.predict()
#     kf.update(measurements[:, i])
#     filtered_states.append(kf.get_state()[:2])  # 只保留位置信息

# # 绘图比较
# plt.figure(figsize=(10, 6))
# plt.plot(true_values[0], true_values[1], label='True Values')
# plt.scatter(measurements[0], measurements[1], color='r', marker='x', label='Measurements')
# filtered_states = np.array(filtered_states).T
# plt.plot(filtered_states[0], filtered_states[1], label='Filtered States', linestyle='--')
# plt.title('Kalman Filter Example (2D)')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend()
# plt.grid(True)
# plt.show()
m1=[('4', 1.0), ('5', 0.0), ('6', 0.0)]
m2=[('4', 0.5), ('5', 0.375), ('6', 0.375)]
initial_state = np.array([m1[0][1], m2[0][1]])  # 初始状态
initial_covariance = np.eye(2) * 0.1  # 初始协方差矩阵
process_covariance = np.eye(2) * 1e-5  # 过程噪声协方差
measurement_covariance = np.eye(1) * 0.1  # 第一组测量噪声协方差  # 第二组测量噪声协方差
kf = KalmanFilter2D(initial_state, initial_covariance, process_covariance, measurement_covariance)


filtered_state=[]
# 在每个时间步更新卡尔曼滤波器
for i in range(3):
    kf.predict()
    kf.update(np.array([m1[i][1]]))  # 更新第一组测量
    kf.update(np.array([m2[i][1]]))  # 更新第二组测量
    filtered_state = kf.get_state()
print(filtered_state)
    # 处理filtered_state