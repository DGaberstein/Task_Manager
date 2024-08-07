# python test_psutil.py

try:
    import psutil
    print("psutil is installed and working.")
    print("CPU Percent:", psutil.cpu_percent(interval=1))
except ImportError:
    print("psutil is not installed.")
except AttributeError as e:
    print("AttributeError:", e)
