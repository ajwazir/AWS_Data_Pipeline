import json
import pandas as pd
from datetime import datetime, date, timedelta
import requests
from pytz import timezone


def lambda_handler(event, context):
    # TODO implement
    
    def tomorrows_flight_arrivals(icao_list):
      # Get today's date in Berlin timezone
      today = datetime.now().astimezone(timezone('Europe/Berlin')).date()
      # Calculate tomorrow's date
      tomorrow = (today + timedelta(days=1))
    
      # Initialize an empty list to store flight data
      list_for_df = []
    
      # Loop over each ICAO code in the input list
      for icao in icao_list:
        # Define the two time periods for which to fetch data
        times = [["00:00","11:59"],["12:00","23:59"]]
    
        # Loop over each time period
        for time in times:
          # Construct the URL for the API request
          url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{icao}/{tomorrow}T{time[0]}/{tomorrow}T{time[1]}"
          # Define the query parameters for the API request
          querystring = {"withLeg":"true","direction":"Arrival","withCancelled":"false","withCodeshared":"true","withCargo":"false","withPrivate":"false"}
          # Define the headers for the API request
          headers = {
              'x-rapidapi-host': "aerodatabox.p.rapidapi.com",
              'x-rapidapi-key': "3d79fb886emsh9a1237e915fade5p15bf46jsn415d2b9f8d79"
              }
          # Make the API request
          response = requests.request("GET", url, headers=headers, params=querystring)
          # Parse the JSON response
          flights_json = response.json()
    
          # Loop over each flight in the response
          for flight in flights_json['arrivals']:
            # Initialize an empty dictionary to store flight data
            flights_dict = {}
            # Store the ICAO code and flight data in the dictionary
            flights_dict['arrival_icao'] = icao
            # Use the .get() method to avoid KeyError if a key doesn't exist in the dictionary
            flights_dict['arrival_time_local'] = flight['arrival'].get('scheduledTimeLocal', None)
            flights_dict['arrival_terminal'] = flight['arrival'].get('terminal', None)
            flights_dict['departure_city'] = flight['departure']['airport'].get('name', None)
            flights_dict['departure_icao'] = flight['departure']['airport'].get('icao', None)
            flights_dict['departure_time_local'] = flight['departure'].get('scheduledTimeLocal', None)
            flights_dict['airline'] = flight['airline'].get('name', None)
            flights_dict['flight_number'] = flight.get('number', None)
            # Store the current date in Berlin timezone
            flights_dict['data_retrieved_on'] = datetime.now().astimezone(timezone('Europe/Berlin')).date()
            # Append the flight dictionary to the list
            list_for_df.append(flights_dict)
    
      # Convert the list of flight dictionaries to a DataFrame and return it
      return pd.DataFrame(list_for_df)    
    
    #icao_list = ["EDDM"]
    icao_list = ["EDDM", "EDDS", "EDDV","EDDB", "EDDH", "EDDP", "EDDF"]
    Flights_df = tomorrows_flight_arrivals(icao_list)
    
    Flights_df["arrival_time_local"] = Flights_df["arrival_time_local"].str[:-6]
    Flights_df["departure_time_local"] = Flights_df["departure_time_local"].str[:-6]
    
    import sqlalchemy
    
    #Specify MySQL connection.
    schema="webcraped_aws"
    host="Your_AWS_host"
    user="admin"
    password="Your_Password"
    port=3306
    con = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
    # export df to sql
    Flights_df.to_sql('cities_flights_data', # renamed from "iss_position"
              if_exists='append', 
              con=con, 
              index=False)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
