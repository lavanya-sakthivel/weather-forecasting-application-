import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime, timedelta
import requests
import pytz

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("890x470+300+200")
        self.root.configure(bg="#57adff")
        self.root.resizable(False,False)

        # Labels for current weather information
        self.l1 = tk.Label(self.root, text='Temperature', font=('Helvetica', 11, 'bold'), fg='white', bg='black')
        self.l1.place(x=30, y=90)

        self.l2 = tk.Label(self.root, text='Humidity', bg='black', font=('Helvetica', 11, 'bold'), fg='white')
        self.l2.place(x=30, y=120)

        self.l3 = tk.Label(self.root, text='Pressure', bg='black', font=('Helvetica', 11, 'bold'), fg='white')
        self.l3.place(x=30, y=150)

        self.l4 = tk.Label(self.root, text='Wind Speed', bg='black', font=('Helvetica', 11, 'bold'), fg='white')
        self.l4.place(x=30, y=180)

        self.l5 = tk.Label(self.root, text='Description', bg='black', font=('Helvetica', 11, 'bold'), fg='white')
        self.l5.place(x=30, y=210)

        # Search box and button
        self.txt_box = tk.Entry(self.root, justify='center', width=13, font=("poppins", 25, 'bold'), bg=("#203243"),
                                border=0, fg="white")
        self.txt_box.place(x=260, y=130)
        self.txt_box.focus()

        tk.Button(self.root, text="Search", borderwidth=0, width=10, height=2, cursor="hand2", bg="white",
                  command=self.get_weather).place(x=550, y=130)

        # Clock and timezone labels
        self.clock = tk.Label(self.root, bg="#57adff", font=('Helvetica', 30, 'bold'), fg='white')
        self.clock.place(x=30, y=20)

        self.timezone = tk.Label(self.root, bg="#57adff", font=('Helvetica', 20, 'bold'), fg='white')
        self.timezone.place(x=600, y=20)

        self.long_lat = tk.Label(self.root, bg="#57adff", font=('Helvetica', 10, 'bold'), fg='white')
        self.long_lat.place(x=700, y=50)

        # Frames for weather forecast cells
        self.frames = []
        self.days_labels = []
        self.dates_labels = []
        self.temps_labels = []  # List to hold temperature labels for each day

        for i in range(5):
            frame = tk.Frame(self.root, width=110, height=140, bg="#282829")
            frame.place(x=50 + i * 150, y=300)
            self.frames.append(frame)

            day_label = tk.Label(frame, bg="#282829", fg="#fff", font=('Helvetica', 12, 'bold'))
            day_label.place(x=10, y=5)
            self.days_labels.append(day_label)

            date_label = tk.Label(frame, bg="#282829", fg="#fff", font=('Helvetica', 10, 'bold'))
            date_label.place(x=10, y=30)
            self.dates_labels.append(date_label)

            temp_label = tk.Label(frame, bg="#282829", fg="#fff", font=('Helvetica', 12, 'bold'))
            temp_label.place(x=10, y=60)
            self.temps_labels.append(temp_label)

    

    def get_weather(self):
        city = self.txt_box.get()
        geolocator = Nominatim(user_agent="geoapiExercises")

        try:
            location = geolocator.geocode(city)
            if location:
                # Display location details
                obj = TimezoneFinder()
                result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
                self.timezone.config(text=result)
                self.long_lat.config(text=f"{round(location.latitude, 4)}°N,{round(location.longitude, 4)}°E")

                # Get local time
                home = pytz.timezone(result)
                local_time = datetime.now(home)
                current_time = local_time.strftime("%I:%M %p")
                self.clock.config(text=current_time)

                # Fetch current weather data
                weather_key = '31db3dafbe920fe0f6ae3ed90698b3ab'
                url = 'https://api.openweathermap.org/data/2.5/weather'
                params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
                response = requests.get(url, params=params)
                current_weather = response.json()

                # Update current weather information labels
                self.l1.config(text=f"Temperature: {current_weather['main']['temp']}°F")
                self.l2.config(text=f"Humidity: {current_weather['main']['humidity']}%")
                self.l3.config(text=f"Pressure: {current_weather['main']['pressure']} hPa")
                self.l4.config(text=f"Wind Speed: {current_weather['wind']['speed']} mph")
                self.l5.config(text=f"Description: {current_weather['weather'][0]['description']}")

                # Fetch weekly forecast data
                url = 'https://api.openweathermap.org/data/2.5/forecast'
                params = {'APPID': weather_key, 'q': city, 'units': 'imperial'}
                response = requests.get(url, params=params)
                forecast = response.json()

                # Update temperature labels for next 7 days
                daily_forecast = forecast['list']
                for i in range(5):
                    temp = daily_forecast[i * 8]['main']['temp']
                    self.temps_labels[i].config(text=f"{temp}°F")

                    day = datetime.now().date() + timedelta(days=i)
                    self.days_labels[i].config(text=day.strftime("%A"))
                    self.dates_labels[i].config(text=day.strftime("%d %b"))

            else:
                messagebox.showerror("Error", "City not found")

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
