# Sparkify Data Warehouse Project

This repository contains the code to build a star schema optimized for analyzing song play data from a music streaming startup called Sparkify.

## Overview

Sparkify needs to analyze user song play logs. To support this, we built a data warehouse on AWS Redshift that leverages a star schema. This schema includes a fact table (`songplays`) and four dimension tables (`users`, `songs`, `artists`, and `time`).


- **dwh.cfg:** Contains the configuration parameters for connecting to the Redshift cluster and S3.
- **create_tables.py:** Creates the necessary staging and analytics tables in the Redshift cluster.
- **etl.py:** Loads data from S3 into staging tables and then processes the data into the analytics tables.
- **sql_queries.py:** Defines all the SQL queries used to drop, create, copy, and insert data.

## Database Schema

The star schema for song play analysis includes:

- **Fact Table:**
  - **songplays:** Records in event data associated with song plays (with page = 'NextSong').
    - Columns: `songplay_id`, `start_time`, `user_id`, `level`, `song_id`, `artist_id`, `session_id`, `location`, `user_agent`

- **Dimension Tables:**
  - **users:** Information about users.
    - Columns: `user_id`, `first_name`, `last_name`, `gender`, `level`
  - **songs:** Information about songs.
    - Columns: `song_id`, `title`, `artist_id`, `year`, `duration`
  - **artists:** Information about artists.
    - Columns: `artist_id`, `name`, `location`, `latitude`, `longitude`
  - **time:** Timestamps broken down into specific units.
    - Columns: `start_time`, `hour`, `day`, `week`, `month`, `year`, `weekday`

## ETL Pipeline

The ETL pipeline performs the following steps:
1. **Extract:** Load raw JSON data from S3 (song and event logs) into staging tables on Redshift using the `COPY` command.
2. **Transform:** Process the data from staging tables and insert it into the analytics tables.
3. **Load:** Data is stored in a star schema design which is optimized for fast querying of song play analysis.

### How to Run

1. **Create Tables:**
   - Update your `dwh.cfg` with the proper connection details.
   - Run `python3 create_tables.py` to create the necessary tables.

2. **Run ETL Pipeline:**
   - Run `python3 etl.py` to load data from S3 into staging tables and then transform and load the data into the final tables.

3. **Verification:**
   - You can run sample queries on your Redshift cluster using the AWS Redshift Query Editor to verify that the data has been loaded correctly.

## Sample Queries

Here are a few example queries you might run on the analytics tables:

- **Most Played Song:**
  ```sql
  SELECT s.title, COUNT(sp.songplay_id) AS play_count
  FROM songplays sp
  JOIN songs s ON sp.song_id = s.song_id
  GROUP BY s.title
  ORDER BY play_count DESC
  LIMIT 1;
