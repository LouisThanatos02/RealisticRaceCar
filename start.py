import os
import time
import threading
if __name__ == "__main__":
    os.system("gnome-terminal -e 'sudo python3 Thread_cam.py'")
    t2 = threading.Thread(target = os.system("gnome-terminal -e 'sudo python3 CarJoy_MotorOnly.py'"))
    t3 = threading.Thread(target =os.system("gnome-terminal -e 'sudo python3 CarJoy_ServoOnly.py'"))
    t2.start()
    t3.start()
