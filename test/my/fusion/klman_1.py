import numpy as np
import matplotlib.pyplot as plt

class KalmanFilter1D:
    def __init__(self, process_variance, measurement_variance, initial_guess):
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.posterior_estimate = initial_guess
        self.posterior_variance = 1.0

    def update(self, measurement):
        # Prediction step
        prior_estimate = self.posterior_estimate
        prior_variance = self.posterior_variance + self.process_variance

        # Update step
        kalman_gain = prior_variance / (prior_variance + self.measurement_variance)
        self.posterior_estimate = prior_estimate + kalman_gain * (measurement - prior_estimate)
        self.posterior_variance = (1 - kalman_gain) * prior_variance

        return self.posterior_estimate

    def get_latest_estimate(self):
        return self.posterior_estimate
    
np.random.seed(0)
num_samples = 50
true_values = np.sin(np.linspace(0, 10, num_samples))  # 真实状态变量
measurements = true_values + 0.1 * np.random.randn(num_samples)  # 模拟测量数据

m1=[('4', 1.0), ('5', 0.0), ('6', 0.0)]
m2=[('4', 0.5), ('5', 0.375), ('6', 0.375)]
m=[]
for i in  range(len(m1)):
    m.append((m1[i][0],(m1[i][1]+m2[i][1])/2))
print(m)
# 初始化卡尔曼滤波器
process_variance = 1e-5
measurement_variance = 0.1 ** 2
initial_guess = m[0][1]
kf = KalmanFilter1D(process_variance, measurement_variance, initial_guess)

# 用卡尔曼滤波器处理数据
filtered_states = []
for measurement in m:
    filtered_states.append(kf.update(measurement[1]))

print(filtered_states)
# 绘图比较
# plt.figure(figsize=(14, 7))
# plt.plot(range(3), measurements, label='Measurements')
# plt.plot(range(3), true_values, label='True Values')
# plt.plot(range(3), filtered_states, label='Filtered States')
# plt.title('Kalman Filter Example')
# plt.xlabel('Time')
# plt.ylabel('Value')
# plt.legend()
# plt.grid(True)
# plt.show()