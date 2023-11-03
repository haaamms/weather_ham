# -*- coding: utf-8 -*-
"""
Created on Tue May 16 21:46:50 2023

@author: steve
"""

from flask import Flask, render_template
import requests
import threading
from PIL import ImageTk, Image
import io
import time
from time import strftime
import tkinter as tk

app = Flask(__name__)

def fetch_weather():
    def _fetch_weather():
        url = 'https://api.weather.gov/zones/forecast/TXZ163/forecast'
        response = requests.get(url)
        try:
            response.raise_for_status()  # Check for any request errors
            forecast = response.json()['properties']
            update_label.config(text='Forecast Updated: ' + forecast['updated'])
            forecast_text.delete(1.0, tk.END)

            num_days = 6

            for period in forecast['periods'][:num_days]:
                forecast_text.insert(tk.END, period['name'] + '\n')
                forecast_text.insert(tk.END, period['detailedForecast'] + '\n\n')
                
        except requests.HTTPError as e:
            print('Error occurred while retrieving weather data:', e)
        except json.JSONDecodeError:
            print('Error parsing JSON response')

    # Start a new thread to fetch the weather data
    thread = threading.Thread(target=_fetch_weather)
    thread.start()

def update_clock():
    current_time = strftime('%H:%M:%S')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Draw the window
    window = tk.Tk()
    window.title('Current Forecast')

    # Configure styles
    window.configure(background='#c46801')

    # Create widgets
    update_label = tk.Label(window, font=('Terminal', 12))
    update_label.pack()

    forecast_text = tk.Text(window, font=('Terminal', 12), width=150, height=25, bg='#263680', fg='#c5c3ca')
    forecast_text.pack()

    # Create the clock
    clock_label = tk.Label(window, font=('Terminal', 12), bg='#c46801', fg='#c5c3ca')
    clock_label.pack(pady=10)

    # Update clock initially
    update_clock()

    # Create the "Refresh Forecast" button
    fetch_button = tk.Button(window, text='Refresh Forecast', command=fetch_weather)
    fetch_button.pack()

    # Embed an image from a file path
    image_path = r"C:\Users\steve\Pictures\The_Weather_Channel_logo.gif"
    image = Image.open(image_path)
    image = image.resize((100, 100))  # Resizes to be smaller
    photo = ImageTk.PhotoImage(image)

    # Create the image label and place it in the top-right corner
    image_label = tk.Label(window, image=photo)
    image_label.image = photo  # Save reference to avoid garbage collection
    image_label.pack(anchor='ne', padx=10, pady=10)

    window.mainloop()

def index():
    # rendering main page
    return render_template('index.html')
