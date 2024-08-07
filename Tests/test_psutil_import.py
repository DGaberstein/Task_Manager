# python test_psutil_import.py

try:
    import psutil
    print("psutil is installed and working.")
except ImportError:
    print("psutil is not installed.")

try:
    print("CPU Percent:", psutil.cpu_percent(interval=1))
except AttributeError as e:
    print("AttributeError:", e)
