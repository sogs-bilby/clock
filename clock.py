import datetime
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from pathlib import Path

class ClockApp:
    def __init__(self, root):
        self.path_images = Path(__file__).parent / 'Images'
        self.root = root
        self.root.title("Clock")
        self.root.geometry("250x180+600+200")
        self.time_zones_image = Image.open( self.path_images / "World_Time_Zones_Map.png")
        aspect_ratio = self.time_zones_image.size[0] / self.time_zones_image.size[1]
        self.time_zones_image_resized = self.time_zones_image.resize((1500, round(1500 / aspect_ratio)))
        self.time_zones_image_final = ImageTk.PhotoImage(self.time_zones_image_resized)
        self.utc_offsets = {
            "UTC-12:00": -12,
            "UTC-11:00": -11,
            "UTC-10:00": -10,
            "UTC-09:30": -9.5,
            "UTC-09:00": -9,
            "UTC-08:00": -8,
            "UTC-07:00": -7,
            "UTC-06:00": -6,
            "UTC-05:00": -5,
            "UTC-04:00": -4,
            "UTC-03:30": -3.5,
            "UTC-03:00": -3,
            "UTC-02:00": -2,
            "UTC-01:00": -1,
            "UTC±00:00": 0,
            "UTC+01:00": 1,
            "UTC+02:00": 2,
            "UTC+03:00": 3,
            "UTC+03:30": 3.5,
            "UTC+04:00": 4,
            "UTC+04:30": 4.5,
            "UTC+05:00": 5,
            "UTC+05:30": 5.5,
            "UTC+05:45": 5.75,
            "UTC+06:00": 6,
            "UTC+06:30": 6.5,
            "UTC+07:00": 7,
            "UTC+08:00": 8,
            "UTC+08:45": 8.75,
            "UTC+09:00": 9,
            "UTC+09:30": 9.5,
            "UTC+10:00": 10,
            "UTC+10:30": 10.5,
            "UTC+11:00": 11,
            "UTC+12:00": 12,
            "UTC+12:45": 12.75,
            "UTC+13:00": 13,
            "UTC+14:00": 14,
        }
        current_time = datetime.datetime.now()
        just_time, just_date = self.get_time_objects(current_time)
        self.local_utc_offset = StringVar()
        self.local_utc_offset.set(current_time.astimezone().utcoffset().seconds / 3600)
        self.utc_offset = StringVar()
        print(current_time.astimezone().utcoffset().seconds / 3600)
        self.utc_offset.set(list(self.utc_offsets.keys())[list(self.utc_offsets.values()).index(float(self.local_utc_offset.get()))])

        self.clock_label = tk.Label(self.root, text=just_time, font=("Arial", 40, "bold"))
        self.clock_label.pack()

        self.date_label = tk.Label(self.root, text=just_date, font=("Arial", 15))
        self.date_label.pack()

        self.utc_offset_menu = tk.OptionMenu(self.root, self.utc_offset, *list(self.utc_offsets.keys()))
        self.utc_offset_menu.pack()

        self.set_local_button = tk.Button(self.root, text=f"Local: {self.utc_offset.get()}", command=self.set_utc_offset_to_local)
        self.set_local_button.pack()

        time_zones_window_button = tk.Button(self.root, text="Show time zones", command=self.open_time_zones_window)
        time_zones_window_button.pack()

    def open_time_zones_window(self, *args):
        time_zones_window = Toplevel(self.root)
        time_zones_window.title("Time Zones")
        time_zones_window.geometry(f"{self.time_zones_image_resized.size[0]}x{self.time_zones_image_resized.size[1]}")
    
        time_zones_image = tk.Label(time_zones_window, image=self.time_zones_image_final)
        time_zones_image.pack()

    def set_utc_offset_to_local(self, *args):
        self.utc_offset.set(list(self.utc_offsets.keys())[list(self.utc_offsets.values()).index(float(self.local_utc_offset.get()))])

    def get_time_objects(self, time_object):
        just_time = datetime.datetime.strftime(time_object, "%H:%M:%S")
        just_date = datetime.datetime.strftime(time_object, "%A %-d %B %Y")

        return (just_time, just_date)

    def update_clock(self, *args):
        #print(self.utc_offsets[self.utc_offset.get()])
        just_time, just_date = self.get_time_objects(datetime.datetime.now() + datetime.timedelta(hours=self.utc_offsets[self.utc_offset.get()] - float(self.local_utc_offset.get())))

        self.clock_label.config(text=just_time)
        self.date_label.config(text=just_date)
        #print(self.utc_offset.get())
        self.root.after(50, self.update_clock)


root = Tk()
clock_app = ClockApp(root)
root.after(0, clock_app.update_clock)
root.mainloop()