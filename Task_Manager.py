import tkinter as tk
from tkinter import ttk
import psutil
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

try:
    import GPUtil
    gpu_available = True
except ImportError:
    gpu_available = False

class TaskManagerReplica:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', background='#1e1e1e', foreground='white')
        style.configure('TNotebook', background='#1e1e1e')
        style.configure('TNotebook.Tab', background='#2d2d2d', foreground='white')
        style.map('TNotebook.Tab', background=[('selected', '#3c3c3c')])

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.cpu_tab = ttk.Frame(self.notebook)
        self.memory_tab = ttk.Frame(self.notebook)
        self.disks_tab = ttk.Frame(self.notebook)
        self.ethernet_tab = ttk.Frame(self.notebook)
        self.gpu_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.cpu_tab, text="CPU")
        self.notebook.add(self.memory_tab, text="Memory")
        self.notebook.add(self.disks_tab, text="Disks")
        self.notebook.add(self.ethernet_tab, text="Ethernet")
        self.notebook.add(self.gpu_tab, text="GPU")

        self.setup_tabs()
        self.timestamps = deque(maxlen=60)

    def setup_tabs(self):
        self.setup_cpu_tab()
        self.setup_memory_tab()
        self.setup_disks_tab()
        self.setup_ethernet_tab()
        self.setup_gpu_tab()

    def setup_cpu_tab(self):
        self.cpu_panel = ttk.Frame(self.cpu_tab)
        self.cpu_panel.pack(expand=True, fill="both")

        ttk.Label(self.cpu_panel, text="CPU Usage", font=('Arial', 16), foreground='#00BFFF').pack(pady=10)

        self.fig_cpu, self.ax_cpu = plt.subplots(figsize=(6, 4), facecolor='#1e1e1e')
        self.ax_cpu.set_facecolor('#2d2d2d')
        self.canvas_cpu = FigureCanvasTkAgg(self.fig_cpu, master=self.cpu_panel)
        self.canvas_cpu.draw()
        self.canvas_cpu.get_tk_widget().pack(expand=True, fill="both")

        self.cpu_values = deque(maxlen=60)
        self.cpu_info_label = ttk.Label(self.cpu_panel, text="", font=('Arial', 12), foreground='white')
        self.cpu_info_label.pack(pady=10)

    def setup_memory_tab(self):
        self.memory_panel = ttk.Frame(self.memory_tab)
        self.memory_panel.pack(expand=True, fill="both")

        ttk.Label(self.memory_panel, text="Memory Usage", font=('Arial', 16), foreground='#7CFC00').pack(pady=10)

        self.fig_memory, self.ax_memory = plt.subplots(figsize=(6, 4), facecolor='#1e1e1e')
        self.ax_memory.set_facecolor('#2d2d2d')
        self.canvas_memory = FigureCanvasTkAgg(self.fig_memory, master=self.memory_panel)
        self.canvas_memory.draw()
        self.canvas_memory.get_tk_widget().pack(expand=True, fill="both")

        self.memory_values = deque(maxlen=60)
        self.memory_info_label = ttk.Label(self.memory_panel, text="", font=('Arial', 12), foreground='white')
        self.memory_info_label.pack(pady=10)

    def setup_disks_tab(self):
        self.disks_panel = ttk.Frame(self.disks_tab)
        self.disks_panel.pack(expand=True, fill="both")

        ttk.Label(self.disks_panel, text="Disk Usage", font=('Arial', 16), foreground='#FF69B4').pack(pady=10)

        self.fig_disks, self.ax_disks = plt.subplots(figsize=(6, 4), facecolor='#1e1e1e')
        self.ax_disks.set_facecolor('#2d2d2d')
        self.canvas_disks = FigureCanvasTkAgg(self.fig_disks, master=self.disks_panel)
        self.canvas_disks.draw()
        self.canvas_disks.get_tk_widget().pack(expand=True, fill="both")

        self.disks_values = deque(maxlen=60)
        self.disks_info_label = ttk.Label(self.disks_panel, text="", font=('Arial', 12), foreground='white')
        self.disks_info_label.pack(pady=10)

    def setup_ethernet_tab(self):
        self.ethernet_panel = ttk.Frame(self.ethernet_tab)
        self.ethernet_panel.pack(expand=True, fill="both")

        ttk.Label(self.ethernet_panel, text="Ethernet Usage", font=('Arial', 16), foreground='#FFA500').pack(pady=10)

        self.fig_ethernet, self.ax_ethernet = plt.subplots(figsize=(6, 4), facecolor='#1e1e1e')
        self.ax_ethernet.set_facecolor('#2d2d2d')
        self.canvas_ethernet = FigureCanvasTkAgg(self.fig_ethernet, master=self.ethernet_panel)
        self.canvas_ethernet.draw()
        self.canvas_ethernet.get_tk_widget().pack(expand=True, fill="both")

        self.ethernet_values = deque(maxlen=60)
        self.ethernet_info_label = ttk.Label(self.ethernet_panel, text="", font=('Arial', 12), foreground='white')
        self.ethernet_info_label.pack(pady=10)

    def setup_gpu_tab(self):
        self.gpu_panel = ttk.Frame(self.gpu_tab)
        self.gpu_panel.pack(expand=True, fill="both")

        ttk.Label(self.gpu_panel, text="GPU Usage", font=('Arial', 16), foreground='#FF4500').pack(pady=10)

        self.fig_gpu, self.ax_gpu = plt.subplots(figsize=(6, 4), facecolor='#1e1e1e')
        self.ax_gpu.set_facecolor('#2d2d2d')
        self.canvas_gpu = FigureCanvasTkAgg(self.fig_gpu, master=self.gpu_panel)
        self.canvas_gpu.draw()
        self.canvas_gpu.get_tk_widget().pack(expand=True, fill="both")

        self.gpu_values = deque(maxlen=60)
        self.gpu_info_label = ttk.Label(self.gpu_panel, text="", font=('Arial', 12), foreground='white')
        self.gpu_info_label.pack(pady=10)

    def update_graphs(self):
        current_time = time.time()

        # Memory
        memory = psutil.virtual_memory()
        # Convert to GB
        used_memory = memory.used / (1024 ** 3)
        total_memory = memory.total / (1024 ** 3)
        percent_memory_used = memory.percent

        self.memory_values.append(used_memory)
        self.timestamps.append(current_time)

        self.ax_memory.clear()
        self.ax_memory.plot(self.timestamps, self.memory_values, color='#7CFC00', linewidth=2)
        self.ax_memory.set_ylim(0, total_memory)
        self.ax_memory.set_xlim(self.timestamps[0] if len(self.timestamps) > 1 else current_time - 60, current_time)
        self.ax_memory.set_yticks([0, total_memory/2, total_memory])
        self.ax_memory.set_yticklabels([f'{0:.1f}', f'{total_memory/2:.1f}', f'{total_memory:.1f}'])
        self.ax_memory.set_xticks([])
        self.ax_memory.set_title(f"Memory usage: {used_memory:.1f} GB / {total_memory:.1f} GB ({percent_memory_used:.1f}%)", color='white')
        self.ax_memory.grid(True, linestyle='--', alpha=0.3)
        self.ax_memory.fill_between(self.timestamps, self.memory_values, color='#7CFC00', alpha=0.2)
        self.canvas_memory.draw()

        self.memory_info_label.config(text=(
            f"Total Memory: {total_memory:.1f} GB\n"
            f"Used Memory: {used_memory:.1f} GB\n"
            f"Memory Usage: {percent_memory_used:.1f}%"
        ))

        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        self.cpu_values.append(cpu_percent)

        self.ax_cpu.clear()
        self.ax_cpu.plot(self.timestamps, self.cpu_values, color='#00BFFF', linewidth=2)
        self.ax_cpu.set_ylim(0, 100)
        self.ax_cpu.set_xlim(self.timestamps[0] if len(self.timestamps) > 1 else current_time - 60, current_time)
        self.ax_cpu.set_yticks([0, 50, 100])
        self.ax_cpu.set_yticklabels([f'{0:.1f}', f'{50:.1f}', f'{100:.1f}'])
        self.ax_cpu.set_xticks([])
        self.ax_cpu.set_title(f"CPU Usage: {cpu_percent:.1f}%", color='white')
        self.ax_cpu.grid(True, linestyle='--', alpha=0.3)
        self.ax_cpu.fill_between(self.timestamps, self.cpu_values, color='#00BFFF', alpha=0.2)
        self.canvas_cpu.draw()

        self.cpu_info_label.config(text=(
            f"CPU Usage: {cpu_percent:.1f}%"
        ))

        # Disk Usage
        disk_usage = psutil.disk_usage('/')
        # Convert to GB
        used_disk = disk_usage.used / (1024 ** 3)
        total_disk = disk_usage.total / (1024 ** 3)
        percent_disk_used = disk_usage.percent

        self.disks_values.append(percent_disk_used)

        self.ax_disks.clear()
        self.ax_disks.plot(self.timestamps, self.disks_values, color='#FF69B4', linewidth=2)
        self.ax_disks.set_ylim(0, 100)
        self.ax_disks.set_xlim(self.timestamps[0] if len(self.timestamps) > 1 else current_time - 60, current_time)
        self.ax_disks.set_yticks([0, 50, 100])
        self.ax_disks.set_yticklabels(['0', '50', '100'])
        self.ax_disks.set_xticks([])
        self.ax_disks.set_title(f"Disk Usage: {used_disk:.1f} GB / {total_disk:.1f} GB ({percent_disk_used:.1f}%)", color='white')
        self.ax_disks.grid(True, linestyle='--', alpha=0.3)
        self.ax_disks.fill_between(self.timestamps, self.disks_values, color='#FF69B4', alpha=0.2)
        self.canvas_disks.draw()

        self.disks_info_label.config(text=(
            f"Total Disk Space: {total_disk:.1f} GB\n"
            f"Used Disk Space: {used_disk:.1f} GB\n"
            f"Disk Usage: {percent_disk_used:.1f}%"
        ))

        # Ethernet / Internet
        net_io = psutil.net_io_counters()
        net_usage = net_io.bytes_sent + net_io.bytes_recv
        # Convert to MB
        self.ethernet_values.append(net_usage / (1024 ** 2))

        self.ax_ethernet.clear()
        self.ax_ethernet.plot(self.timestamps, self.ethernet_values, color='#FFA500', linewidth=2)
        self.ax_ethernet.set_ylim(0, max(self.ethernet_values) if self.ethernet_values else 1)
        self.ax_ethernet.set_xlim(self.timestamps[0] if len(self.timestamps) > 1 else current_time - 60, current_time)
        self.ax_ethernet.set_yticks([0, max(self.ethernet_values) / 2, max(self.ethernet_values)] if self.ethernet_values else [0])
        self.ax_ethernet.set_xticks([])
        self.ax_ethernet.set_title(f"Network Usage: {net_usage / (1024 ** 2):.1f} MB", color='white')
        self.ax_ethernet.grid(True, linestyle='--', alpha=0.3)
        self.ax_ethernet.fill_between(self.timestamps, self.ethernet_values, color='#FFA500', alpha=0.2)
        self.canvas_ethernet.draw()

        self.ethernet_info_label.config(text=(
            f"Network Usage: {net_usage / (1024 ** 2):.1f} MB"
        ))

        # GPU
        if gpu_available:
            try:
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    # Assuming we're interested in the first GPU
                    gpu = gpus[0]
                    temperature = gpu.temperature
                    utilization = gpu.load * 100
                    memory_total = gpu.memoryTotal
                    memory_free = gpu.memoryFree
                    memory_used = memory_total - memory_free

                    self.gpu_values.append(utilization)

                    self.ax_gpu.clear()
                    self.ax_gpu.plot(self.timestamps, self.gpu_values, color='#FF4500', linewidth=2)
                    self.ax_gpu.set_ylim(0, 100)
                    self.ax_gpu.set_xlim(self.timestamps[0] if len(self.timestamps) > 1 else current_time - 60, current_time)
                    self.ax_gpu.set_yticks([0, 50, 100])
                    self.ax_gpu.set_yticklabels(['0', '50', '100'])
                    self.ax_gpu.set_xticks([])
                    self.ax_gpu.set_title(f"GPU Utilization: {utilization:.1f}%", color='white')
                    self.ax_gpu.grid(True, linestyle='--', alpha=0.3)
                    self.ax_gpu.fill_between(self.timestamps, self.gpu_values, color='#FF4500', alpha=0.2)
                    self.canvas_gpu.draw()

                    self.gpu_info_label.config(text=(
                        f"Temperature: {temperature} C\n"
                        f"Memory Usage: {memory_used / (1024 ** 2):.1f} MB / {memory_total / (1024 ** 2):.1f} MB\n"
                        f"Video Encode: {gpu.memoryUsed / 1024:.1f} MB\n"
                        f"Video Decode: {gpu.memoryFree / 1024:.1f} MB\n"
                        f"Dedicated GPU Memory: {memory_total / (1024 ** 2):.1f} MB\n"
                        f"Shared GPU Memory: {memory_free / (1024 ** 2):.1f} MB"
                    ))

                else:
                    self.ax_gpu.clear()
                    self.ax_gpu.plot(self.timestamps, self.gpu_values, color='#FF4500', linewidth=2)
                    self.ax_gpu.set_ylim(0, 100)
                    self.ax_gpu.set_xlim(self.timestamps[0] if len(self.timestamps) > 1 else current_time - 60, current_time)
                    self.ax_gpu.set_yticks([0, 50, 100])
                    self.ax_gpu.set_yticklabels(['0', '50', '100'])
                    self.ax_gpu.set_xticks([])
                    self.ax_gpu.set_title("GPU Usage: N/A", color='white')
                    self.ax_gpu.grid(True, linestyle='--', alpha=0.3)
                    self.ax_gpu.fill_between(self.timestamps, self.gpu_values, color='#FF4500', alpha=0.2)
                    self.canvas_gpu.draw()

            except Exception as e:
                self.ax_gpu.clear()
                self.ax_gpu.plot(self.timestamps, self.gpu_values, color='#FF4500', linewidth=2)
                self.ax_gpu.set_ylim(0, 100)
                self.ax_gpu.set_xlim(self.timestamps[0] if len(self.timestamps) > 1 else current_time - 60, current_time)
                self.ax_gpu.set_yticks([0, 50, 100])
                self.ax_gpu.set_yticklabels(['0', '50', '100'])
                self.ax_gpu.set_xticks([])
                self.ax_gpu.set_title("GPU Usage: Error", color='white')
                self.ax_gpu.grid(True, linestyle='--', alpha=0.3)
                self.ax_gpu.fill_between(self.timestamps, self.gpu_values, color='#FF4500', alpha=0.2)
                self.canvas_gpu.draw()
                print(f"Error retrieving GPU information: {e}")

        else:
            self.ax_gpu.clear()
            self.ax_gpu.plot(self.timestamps, self.gpu_values, color='#FF4500', linewidth=2)
            self.ax_gpu.set_ylim(0, 100)
            self.ax_gpu.set_xlim(self.timestamps[0] if len(self.timestamps) > 1 else current_time - 60, current_time)
            self.ax_gpu.set_yticks([0, 50, 100])
            self.ax_gpu.set_yticklabels(['0', '50', '100'])
            self.ax_gpu.set_xticks([])
            self.ax_gpu.set_title("GPU Usage: N/A", color='white')
            self.ax_gpu.grid(True, linestyle='--', alpha=0.3)
            self.ax_gpu.fill_between(self.timestamps, self.gpu_values, color='#FF4500', alpha=0.2)
            self.canvas_gpu.draw()

            # Update every 1 second
        self.root.after(1000, self.update_graphs)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerReplica(root)
    # Initial call to start updating graphs
    root.after(1000, app.update_graphs)
    root.mainloop()
