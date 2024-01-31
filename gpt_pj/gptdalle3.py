import requests
import random
import os
import ctypes
from PIL import Image
import openai

OPENWEATHER_API_KEY = '토근'
OPENAI_API_KEY = '토큰'

#busan
#seoul
city = 'New%20York,US'

def get_weather(city, api_key):
    WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(WEATHER_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return None

#기본적인 프롬프트는 넣어둬야 이미지 퀄리티가 이상하지 않음
def select_weather_pt(weather):
    if weather == 'Clear':
        return (
            'The photo appears to capture a scene from a lively city.\
 The photo shows people relaxing in a city park or square in sunny weather.\
 In the background are one or two buildings with a European architectural style,\
 with what appears to be a cafe or store on the lower level of the building. \
 Several people are sitting on the grass, chatting and enjoying their leisure time.\
 This scene shows the relaxed, social aspect of city life and\
 illustrates how urban spaces are integrated into the lives of their inhabitants.'
        )
    elif weather == 'Clouds':
        return 'The photo captures a peaceful natural scene along a quiet country road.\
 In the foreground, we see a winding dirt road, and to the side of the road is a large, green meadow.\
 Beyond the meadow is a multi-tiered forest and green trees, and beyond that, a mountain range rises. \
 The mountains are covered in green, dense trees, and their peaks are slightly obscured by clouds.\
 The sky is heavily clouded, but there are rays of sunlight peeking through, creating a dramatic contrast in the photo.\
 This landscape conveys a sense of tranquility and natural beauty, and the interplay of clouds and light creates a sense of drama.'
    elif weather == 'Rain':
        return (
            'The photo shows a view through a window on a rainy day.\
 There are many very realistic water droplets on the window glass,\
 and the background seen through them is blurred. The water droplets\
 are concentrated in the foreground of the image and are distributed in various sizes.\
 Some of the droplets appear to shine brighter due to light reflection.\
 You can see the outlines of buildings in the background,\
 and the sky is cloudy. As a whole, the photo has a serene, dreamy atmosphere after the rain.'
        )
    else:
        print("Weather not yet supported")
        return "Weather is unpredictable today."

#ex='Rain'
#print(select_weather_pt(ex))

def select_temp_pt(temperature):
    if temperature <= 5:
        return " It's probably cold."
    elif 5 < temperature < 20:
        return " It's probably warm."
    elif 20 <= temperature:
        return " The sun is intense."
    #더 추가 할 필요는 없을듯
    else:
        return " Temperature is unusual today."

def create_image():
    weather_data = get_weather(city, OPENWEATHER_API_KEY)
    if weather_data:
        weather_condition = weather_data['weather'][0]['main']
        temperature = weather_data['main']['temp']

        weather_pt = select_weather_pt(weather_condition)
        temp_pt = select_temp_pt(temperature)

        print(weather_pt)
        print(temp_pt)
    else:
        print("Can't load the weather.")

    openai.api_key = OPENAI_API_KEY
    prompt = f"Create a image using the description below as a guide. '{weather_pt} Also {temp_pt}'"
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt, 
            n=1, 
            size="1792x1024"
        )

        image_url = response.data[0].url
    except AttributeError:
        print("error access image url")
        return
    
    img_data = requests.get(image_url).content
    with open('wallpaper.png', 'wb') as handler:
        handler.write(img_data)

create_image()

def set_wallpaper(image_path):

    full_image_path = os.path.abspath(image_path)
    
    img = Image.open(full_image_path)
    bmp_image_path = full_image_path.replace('.png', '.bmp')
    img.save(bmp_image_path)

    ctypes.windll.user32.SystemParametersInfoW(20, 0, bmp_image_path, 0)

set_wallpaper('wallpaper.png')