import matplotlib.pyplot as plt
from meteostat import Point, Daily
from datetime import datetime
import numpy as np

def select_data(start, end, point_x, point_y, point_z):
    geo_dot = Point(point_x, point_y, point_z) # Создаём точку
    # Получаем ежедневные данные за период
    data = Daily(geo_dot, start, end)
    data = data.fetch()
    return data

def calculate_weather_indices(data):
    # Индексы настроены на умеренную широту
    summed_data = data['prcp'].sum()
    prcp_year_idx = summed_data/len(data.index)
    # Индекс отношения дней с экстремальным кол-вом осадков к обычным
    prcp_to_day_ext = data['prcp'][data['prcp'] > 10]
    prcp_to_day_norm = data['prcp'][data['prcp'] < 10]
    ext_prcp_days_idx = len(prcp_to_day_ext)
    attitude_ext_norm_idx = round(len(prcp_to_day_ext)/len(prcp_to_day_norm), 4)
    
    print(f'Humidity index: {prcp_year_idx}')
    print(f'Days with extreme precipitation: {ext_prcp_days_idx}')
    print(f'Ratio of extreme to normal: {attitude_ext_norm_idx} | {len(prcp_to_day_ext)}/{len(prcp_to_day_norm)}')
    print(f'-------------------------\nTemperature trend: {round(trend[-1]-trend[0], 2)}')

def generate_linear_trend(data):
    # Линейная аппроксимация с учетом пропусков
    if data['tavg'].isnull().sum() > 0:
        data['tavg'].interpolate(method='linear', inplace=True)  # Заполнение пропусков методом линейной интерполяции
        
    x = np.arange(len(data['tavg']))
    coefficients = np.polyfit(x, data['tavg'], 1)
    trend = np.polyval(coefficients, x)
    return trend

def graphics_drawing(data):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    # Первый график: Температура и скорость ветра
    ax1.plot(data.index, data['tavg'], label='Average temperature (°C)', color='red')
    ax1.plot(data.index, trend, label='Average temperature (°C)', color='red', linestyle='--')
    ax1.plot(data.index, data['wspd'], label='Wind speed (m/s)', color='blue')
    ax1.set_title(f'Temperature and wind speed')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Value')
    ax1.legend()
    ax1.grid(True)
    # Второй график: Осадки
    ax2.plot(data.index, data['prcp'], label='Precipitation (mm)', color='green')
    ax2.set_title('Precipitation')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Precipitation (mm)')
    ax2.legend()
    ax2.grid(True)
    plt.tight_layout()
    plt.show()

# Пример:
start, end = datetime(2021, 1, 1), datetime(2022, 12, 31)
point_x, point_y, point_z = 48.9301, -93.4077, 70
weath_data = select_data(start, end, point_x, point_y, point_z)
trend = generate_linear_trend(weath_data)
