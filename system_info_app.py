import tkinter as tk
from tkinter import ttk
import psutil
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

class SystemInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Information")
        self.root.configure(bg='#333333')
        self.root.geometry('800x600')

        # Create a canvas for the animated background
        self.background_canvas = tk.Canvas(root, bg='#333333', highlightthickness=0)
        self.background_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create a frame for the graph
        self.graph_frame = tk.Frame(root, bg='#333333')
        self.graph_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create the figure and axis for the graph
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor('#333333')
        self.ax.set_facecolor('#333333')
        self.ax.tick_params(axis='both', colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')

        # Set up the canvas for the figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize data
        self.start_time = time.time()
        self.x_data = deque(maxlen=60)
        self.cpu_data = deque(maxlen=60)
        self.memory_data = deque(maxlen=60)
        self.disk_data = deque(maxlen=60)

        # Initialize color index for background animation
        self.color_index = 0

        # Plot initialization
        self.cpu_line, = self.ax.plot([], [], label='CPU Usage (%)', color='red')
        self.memory_line, = self.ax.plot([], [], label='Memory Usage (%)', color='blue')
        self.disk_line, = self.ax.plot([], [], label='Disk Usage (%)', color='green')
        self.ax.set_xlabel('Time (s)', color='white')
        self.ax.set_ylabel('Usage (%)', color='white')
        self.ax.legend()
        self.ax.grid(True, linestyle='--', color='gray')

        # Start background animation and data update using Tkinter's after method
        self.animate_background()
        self.update_info()

    def get_system_info(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')

        return cpu_usage, memory_info.percent, disk_info.percent

    def update_info(self):
        cpu_usage, memory_usage, disk_usage = self.get_system_info()
        current_time = time.time() - self.start_time
        self.x_data.append(current_time)
        self.cpu_data.append(cpu_usage)
        self.memory_data.append(memory_usage)
        self.disk_data.append(disk_usage)

        self.update_graph()

        # Schedule the next update
        self.root.after(1000, self.update_info)  # Update every 1 second

    def update_graph(self):
        self.cpu_line.set_data(self.x_data, self.cpu_data)
        self.memory_line.set_data(self.x_data, self.memory_data)
        self.disk_line.set_data(self.x_data, self.disk_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def animate_background(self):
        colors = ['#333333', '#444444', '#555555']
        self.color_index = (self.color_index + 1) % len(colors)
        self.background_canvas.config(bg=colors[self.color_index])
        self.root.after(1000, self.animate_background)  # Change color every 1 second

# Initialize the main window
root = tk.Tk()
app = SystemInfoApp(root)
root.mainloop()
