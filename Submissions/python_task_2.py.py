#!/usr/bin/env python
# coding: utf-8

# Question 1: Distance Matrix Calculation
# Create a function named calculate_distance_matrix that takes the dataset-3.csv as input and generates a DataFrame representing distances between IDs.
# 
# The resulting DataFrame should have cumulative distances along known routes, with diagonal values set to 0. If distances between toll locations A to B and B to C are known, then the distance from A to C should be the sum of these distances. Ensure the matrix is symmetric, accounting for bidirectional distances between toll locations (i.e. A to B is equal to B to A).

# In[1]:


import pandas as pd

data = pd.read_csv('dataset-3.csv')
data


# In[2]:


# Create a list of all unique IDs
unique_ids = sorted(list(set(data['id_start'].unique()) | set(data['id_end'].unique())))

# Create an empty DataFrame for the distance matrix
distance_matrix = pd.DataFrame(float('inf'), index=unique_ids, columns=unique_ids)

# Fill in the distance matrix
for index, row in data.iterrows():
    start_id = row['id_start']
    end_id = row['id_end']
    distance = row['distance']
    
# Assign distances to the corresponding IDs in the matrix
    distance_matrix.at[start_id, end_id] = distance
    distance_matrix.at[end_id, start_id] = distance  # Since the distances are bidirectional

# Set diagonal elements to zero
for i in distance_matrix.index:
    distance_matrix.at[i, i] = 0

# Floyd-Warshall algorithm for calculating shortest paths
for k in distance_matrix.index:
    for i in distance_matrix.index:
        for j in distance_matrix.index:
            if distance_matrix.at[i, j] > distance_matrix.at[i, k] + distance_matrix.at[k, j]:
                distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

print(distance_matrix)


# Question 2: Unroll Distance Matrix
# Create a function unroll_distance_matrix that takes the DataFrame created in Question 1. The resulting DataFrame should have three columns: columns id_start, id_end, and distance.
# 
# All the combinations except for same id_start to id_end must be present in the rows with their distance values from the input DataFrame.

# In[3]:


import itertools

def unroll_distance_matrix(df):
    rows = []
    for i, j in itertools.combinations(df.index, 2):
        distance = df.loc[i, j]
        rows.append([i, j, distance])
    result = pd.DataFrame(rows, columns=['id_start', 'id_end', 'distance'])
    return result

result = unroll_distance_matrix(distance_matrix)
print(result)


# Question 3: Finding IDs within Percentage Threshold
# Create a function find_ids_within_ten_percentage_threshold that takes the DataFrame created in Question 2 and a reference value from the id_start column as an integer.
# 
# Calculate average distance for the reference value given as an input and return a sorted list of values from id_start column which lie within 10% (including ceiling and floor) of the reference value's average.

# In[4]:


def find_ids_within_ten_percentage_threshold(df, reference_value):
# Calculate average distance for the reference value
    average_distance = df[df['id_start'] == reference_value]['distance'].mean()
    
# Calculate the threshold range (10% of the average distance)
    threshold = 0.1 * average_distance
    
# Find IDs within the threshold range
    within_threshold = df[(df['id_start'] != reference_value) & 
                          (df['distance'] >= (average_distance - threshold)) & 
                          (df['distance'] <= (average_distance + threshold))]
    
# Get unique IDs within the threshold
    unique_ids_within_threshold = sorted(within_threshold['id_start'].unique())
    
    return unique_ids_within_threshold

reference_value = 1001400
result_within_threshold = find_ids_within_ten_percentage_threshold(result, reference_value)
print(result_within_threshold)


# Question 4: Calculate Toll Rate
# Create a function calculate_toll_rate that takes the DataFrame created in Question 2 as input and calculates toll rates based on vehicle types.
# 
# The resulting DataFrame should add 5 columns to the input DataFrame: moto, car, rv, bus, and truck with their respective rate coefficients. The toll rates should be calculated by multiplying the distance with the given rate coefficients for each vehicle type:
# 
# 0.8 for moto
# 1.2 for car
# 1.5 for rv
# 2.2 for bus
# 3.6 for truck
# 

# In[5]:


def calculate_toll_rate(df):
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    for vehicle, rate in rate_coefficients.items():
        df[vehicle] = df['distance'] * rate

    return df


result_with_rates = calculate_toll_rate(result)
print(result_with_rates.head())  


# Question 5: Calculate Time-Based Toll Rates
# Create a function named calculate_time_based_toll_rates that takes the DataFrame created in Question 3 as input and calculates toll rates for different time intervals within a day.
# 
# The resulting DataFrame should have these five columns added to the input: start_day, start_time, end_day, and end_time.
# 
# start_day, end_day must be strings with day values (from Monday to Sunday in proper case)
# start_time and end_time must be of type datetime.time() with the values from time range given below.
# Modify the values of vehicle columns according to the following time ranges:
# 
# Weekdays (Monday - Friday):
# 
# From 00:00:00 to 10:00:00: Apply a discount factor of 0.8
# From 10:00:00 to 18:00:00: Apply a discount factor of 1.2
# From 18:00:00 to 23:59:59: Apply a discount factor of 0.8
# Weekends (Saturday and Sunday):
# 
# Apply a constant discount factor of 0.7 for all times.
# For each unique (id_start, id_end) pair, cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).

# In[6]:


import datetime

def calculate_time_based_toll_rates(df):
# Define time intervals and discount factors
    weekday_intervals = [
        (datetime.time(0, 0, 0), datetime.time(10, 0, 0), 0.8),
        (datetime.time(10, 0, 0), datetime.time(18, 0, 0), 1.2),
        (datetime.time(18, 0, 0), datetime.time(23, 59, 59), 0.8)
    ]
    weekend_factor = 0.7

# Create empty columns for start_day, start_time, end_day, and end_time
    df['start_day'] = ''
    df['start_time'] = ''
    df['end_day'] = ''
    df['end_time'] = ''

# Iterate over each row and calculate time-based toll rates
    for index, row in df.iterrows():
        id_start = row['id_start']
        id_end = row['id_end']

# For each unique pair, cover a full 24-hour period and all 7 days of the week
        for day in range(7):
            start_day = (datetime.datetime.now() + datetime.timedelta(days=day)).strftime('%A')
            end_day = (datetime.datetime.now() + datetime.timedelta(days=day)).strftime('%A')

# Apply discount factors based on weekdays or weekends
            if start_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
                for interval in weekday_intervals:
                    df.loc[index, 'start_day'] = start_day
                    df.loc[index, 'start_time'] = interval[0]
                    df.loc[index, 'end_day'] = end_day
                    df.loc[index, 'end_time'] = interval[1]
                    df.loc[index, 'moto'] *= interval[2]
                    df.loc[index, 'car'] *= interval[2]
                    df.loc[index, 'rv'] *= interval[2]
                    df.loc[index, 'bus'] *= interval[2]
                    df.loc[index, 'truck'] *= interval[2]
            else:  # Weekend
                df.loc[index, 'start_day'] = start_day
                df.loc[index, 'start_time'] = datetime.time(0, 0, 0)
                df.loc[index, 'end_day'] = end_day
                df.loc[index, 'end_time'] = datetime.time(23, 59, 59)
                df.loc[index, 'moto'] *= weekend_factor
                df.loc[index, 'car'] *= weekend_factor
                df.loc[index, 'rv'] *= weekend_factor
                df.loc[index, 'bus'] *= weekend_factor
                df.loc[index, 'truck'] *= weekend_factor
                return df

result_with_time_based_rates = calculate_time_based_toll_rates(result)
print(result_with_time_based_rates.head())

