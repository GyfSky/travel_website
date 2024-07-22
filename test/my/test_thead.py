import threading
import time

# 定义线程执行的函数
def thread_function(name, delay):
    print(f"Thread {name} starting...")
    time.sleep(delay)
    print(f"Thread {name} finishing...")

# 创建线程对象
thread1 = threading.Thread(target=thread_function, args=(1, 2))  # 第一个线程，延时 2 秒
thread2 = threading.Thread(target=thread_function, args=(2, 3))  # 第二个线程，延时 3 秒

# 启动线程
thread1.start()
thread2.start()

# 主线程可以做其他事情，或者等待所有线程完成
thread1.join()
thread2.join()

print("All threads finished.")