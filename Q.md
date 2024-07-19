# Geo UAT Server and Weather Data

## Background
At the start of the week, we encountered a space issue with PostgreSQL on the Geo UAT server. Although I was able to load small datasets into the database, any dataset larger than 1.5 gigabytes could not be loaded due to insufficient storage space.

## Resolution
We met with AWS support to address the storage issue. After their assistance, we successfully resolved the storage constraints and were able to load large datasets without any problems.

## New Issues
However, fixing the storage issue led to new problems with Docker permissions. Attempts to resolve these Docker permission issues further destabilized the server, rendering it unusable. I could not even build a Docker image after these complications.

## Interim Solution
When the Geo UAT server became unusable, I switched to the GEO Prod server, an adhoc server that requires manual intervention to start PostgreSQL. With Shiv's assistance, we successfully started PostgreSQL on the GEO Prod server. Despite its limited storage, I wrote a Python script to process and run the Nearest Neighbour analysis for 1% of the data at a time. This approach allowed me to obtain results for all the SRM subscribers.

## Nearest Neighbour Configuration
I configured the nearest weather station search for each subscriber in the `srm_model_data` table for the date of 2024-06-01, considering a radius of 50,000 meters (~30 miles).

## Results
Out of 26,272,931 subscribers, 25,096,683 were within the 30-mile radius and were successfully matched with a weather station.

The NN results are in `dlbiadvdanltcs.nn_srm_weather_stations`.

## Table Creation in Redshift
I created a table in Redshift to store the nearest weather station data for SRM subscribers.

```sql
CREATE TABLE dlbiadvdanltcs.nn_srm_weather_stations (
    dimsvcunitsk INT, -- SRM JOIN KEY
    station VARCHAR(150), -- WEATHER STATION JOIN KEY
    d_meters INT, -- DISTANCE IN METERS BETWEEN THE SUBSCRIBER AND THE NEAREST WEATHER STATION
    pt_srm VARCHAR(150), -- SUBSCRIBER LOCATION GEOMETRY FOR MAPPING
    pt_station VARCHAR(150) -- LOCATION OF CLOSEST WEATHER STATION FOR MAPPING
);

