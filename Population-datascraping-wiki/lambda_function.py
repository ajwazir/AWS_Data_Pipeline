# import libraries
import json
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
list_of_cities = ["Munich", "Stuttgart", "Hanover"]

# coordinates correction function

def lambda_handler(event, context):
    # TODO implement
    
    
    # coordinates correction function
    def convert_to_decimal(coordinate):
      degrees, minutes = coordinate.split('°')[0], coordinate.split('°')[1].split('′')[0]
      if '″' in coordinate:
          seconds = coordinate.split('′')[1].split('″')[0]
      else:
          seconds = 0
      decimal_value = int(degrees) + (int(minutes) / 60) + (int(seconds) / 3600)
      return decimal_value
    
    # data scraping function
    def webscrape_wiki(list_of_cities):
      
      list_for_df = []
      
      for city in list_of_cities:
      
        url = f"https://en.wikipedia.org/wiki/{city}"
      
        headers = {'Accept-Language': 'en-US,en;q=0.8'}
        response = requests.get(url, headers = headers)
        if response.status_code != 200: break
      
        wiki_soup = BeautifulSoup(response.content, "html.parser")
      
        response_dict = {}
      
        response_dict["city"] = wiki_soup.select("span.mw-page-title-main")[0].getText()
        response_dict["country"] = wiki_soup.select("table.infobox td.infobox-data")[0].getText()
        response_dict["latitude"] = wiki_soup.select("span.latitude")[0].getText()
        for key in ['latitude']:
          # Convert degrees, minutes, and seconds to decimal format
          response_dict["latitude"] = convert_to_decimal(response_dict[key])
        response_dict["longitude"] = wiki_soup.select("span.longitude")[0].getText()
        for key in ['longitude']:
          # Convert degrees, minutes, and seconds to decimal format
          response_dict["longitude"] = convert_to_decimal(response_dict[key])
        if wiki_soup.select_one('th.infobox-header:-soup-contains("Population")'):
          response_dict["population"] = wiki_soup.select_one('th.infobox-header:-soup-contains("Population")').parent.find_next_sibling().find(text=re.compile(r'\d+'))
      
        list_for_df.append(response_dict)
      
        cities_df = pd.DataFrame(list_for_df)
        cities_df["population"] = cities_df["population"].str.replace(",", "") 
        cities_df["population"] = pd.to_numeric(cities_df["population"], downcast="integer")
      
      
      return  cities_df

    Cities_data_df = webscrape_wiki(list_of_cities)

    
    #import sqlalchemy 
    import sqlalchemy
    #Specify MySQL connection.
    schema="webcraped_aws" 
    host="Your_AWS_host"
    user="admin"
    password="Your_Password"
    port=3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
    
    #Use pandas method to_sql with the argument if_exists=append to create the table (only the first time we run it) and insert the new rows into it.
    Cities_data_df.to_sql('cities_wiki_data', # renamed from "iss_position"
                  if_exists='append', 
                  con=con, 
                  index=False)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
