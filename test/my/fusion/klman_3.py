import numpy as np
import matplotlib.pyplot as plt

def kalman_filter(initial_state, initial_estimate_error, process_variance, measurement_variance, measurements):
    num_measurements = len(measurements)
    state_estimate = initial_state
    estimate_error = initial_estimate_error
    filtered_state_estimates = []
    
    for i in range(num_measurements):
        # Prediction step
        predicted_state = state_estimate
        predicted_estimate_error = estimate_error + process_variance
        
        # Update step
        kalman_gain = predicted_estimate_error / (predicted_estimate_error + measurement_variance)
        state_estimate = predicted_state + kalman_gain * (measurements[i] - predicted_state)
        estimate_error = (1 - kalman_gain) * predicted_estimate_error
        
        filtered_state_estimates.append(state_estimate)
    
    return filtered_state_estimates

# Generate some noisy measurements
np.random.seed(0)
true_values = np.linspace(0, 10, num=50)
measurements = true_values + np.random.normal(0, 0.5, size=len(true_values))

# Kalman filter parameters
initial_state = measurements[0]
initial_estimate_error = 1
process_variance = 0.1
measurement_variance = 0.5

# Apply Kalman filter
filtered_estimates = kalman_filter(initial_state, initial_estimate_error, process_variance, measurement_variance, measurements)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(true_values, label='True Values', linestyle='dashed')
plt.plot(measurements, label='Noisy Measurements', marker='o', markersize=5)
plt.plot(filtered_estimates, label='Filtered Estimates', linestyle='dotted')
plt.legend()
plt.xlabel('Time Step')
plt.ylabel('Value')
plt.title('Kalman Filter Example')
plt.show()
