#Import necessary modules
import pandas as pd
import requests
from datetime import datetime
import pytz
import json

def lambda_handler(event, context):
    # TODO implement

    def get_weather_loop(cities):
      # API key for openweathermap
      print("API_key")
      API_key = "d5eae1f375b91d136f5a47b5c32c7f90"
    
      # Set timezone to Europe/Berlin
      tz = pytz.timezone('Europe/Berlin')
    
      # Get current date and time
      now = datetime.now().astimezone(tz)
    
      # My API_Key "d5eae1f375b91d136f5a47b5c32c7f90"
    
      # Initialize dictionary to store weather data
    
      Dict = {"City":[],
              "Country":[],
              "Date_Time":[],
              "Temperature":[],
              "Weather_desc":[],
              "Rain":[],
              "Snow":[],
              "Wind_speed":[],
              "Information_retrieved_at": []}
    
    
      # Loop over all cities provided
      for city in cities:
          url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_key}&units=metric"
    
          # Make the API request
          city_weather = requests.get(url)
    
          # Parse the response into JSON format
          city_weather_json =city_weather.json()
    
          # Loop over all the forecasts returned in the JSON response
          for item in city_weather_json["list"]:
    
          # Append the relevant pieces of data to the appropriate list in the weather_dict dictionary
              Dict['City'].append(city_weather_json['city']['name'])
              Dict['Country'].append(city_weather_json['city']['country'])
              if "rain" in item.keys():
                  Dict["Rain"].append(item["rain"]["3h"])
              else:
                  Dict["Rain"].append(0)
              if "snow" in item.keys():
                  Dict["Snow"].append(item["snow"]["3h"])
              else:
                  Dict["Snow"].append(0)
              Dict["Temperature"].append(item["main"]["temp"])
              Dict["Weather_desc"].append(item["weather"][0]["main"])
              Dict["Wind_speed"].append(item["wind"]["speed"])
              Dict["Date_Time"].append(item["dt_txt"])
              Dict["Information_retrieved_at"].append(now.strftime("%Y-%m-%d %H:%M:%S"))
    
      # Convert the weather_dict into a pandas DataFrame and return it
      return pd.DataFrame(Dict)
      
    cities = ["Munich", "Stuttgart", "Hanover", "Berlin", "Hamburg", "Leipzig", "Frankfurt"]
    cities_weather_df = get_weather_loop(cities)
    
    import sqlalchemy
    
    #Specify MySQL connection.
    schema="webcraped_aws"
    host="Your_AWS_host"
    user="admin"
    password="Your_Password"
    port=3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
    
    cities_weather_df.to_sql('cities_weather_data', # renamed from "iss_position"
                  if_exists='append', 
                  con=con, 
                  index=False)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
