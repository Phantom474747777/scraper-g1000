import os
import signal
import psutil

# Kill all Python processes except this one
current_pid = os.getpid()
for proc in psutil.process_iter(['pid', 'name']):
    try:
        if 'python' in proc.info['name'].lower() and proc.info['pid'] != current_pid:
            print(f"Killing PID {proc.info['pid']}: {proc.info['name']}")
            os.kill(proc.info['pid'], signal.SIGTERM)
    except:
        pass
print("All Python processes killed")
