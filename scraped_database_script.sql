-- CREATE DATABASE sql_combined_scraped_cities_data_asim;

USE webscraped_aws;

-- DROP TABLE cities_weather_data;
-- CREATE TABLE cities_weather_data
CREATE TABLE cities_weather_data (
	id INT AUTO_INCREMENT, 
    City VARCHAR(50),
    Country VARCHAR(50),	
    Date_Time DATETIME,
    Temperature FLOAT(2),	
    Weather_desc VARCHAR(50),	
    Rain FLOAT(6),	
    Snow FLOAT(6),	
    Wind_speed FLOAT(6),
    Information_retrieved_at DATETIME,
    PRIMARY KEY (id, city)
);

-- DROP TABLE cities_flights_data;
-- CREATE TABLE cities_flights_data

CREATE TABLE cities_flights_data (
	id INT AUTO_INCREMENT, 
    arrival_icao VARCHAR(50),
    arrival_time_local VARCHAR(50),
    arrival_terminal VARCHAR(50),
    departure_city VARCHAR(50),
	departure_icao VARCHAR(50),
	departure_time_local  VARCHAR(50),
	airline VARCHAR(50),
    flight_number VARCHAR(50),
    data_retrieved_on DATETIME,
    PRIMARY KEY (id)
);

-- CREATE TABLE wiki_cities_data
CREATE TABLE cities_wiki_data (
	id INT AUTO_INCREMENT, 
    city VARCHAR(50),
    country	 VARCHAR(50),
    latitude FLOAT(6),
    longitude FLOAT(6),
	population FLOAT(0),
	PRIMARY KEY (id)
);

SELECT * FROM cities_weather_data;
SELECT * FROM cities_flights_data;
SELECT * FROM cities_wiki_data;
SELECT * FROM airports_data;
DELETE FROM airports_data WHERE ICAO = '';