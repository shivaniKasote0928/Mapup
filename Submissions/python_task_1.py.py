#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
df = pd.read_csv('dataset-1.csv')#To import the dataset-1
df


# Question 1: Car Matrix Generation
# Under the function named generate_car_matrix write a logic that takes the dataset-1.csv as a DataFrame. Return a new DataFrame that follows the following rules:
# 
# values from id_2 as columns
# values from id_1 as index
# dataframe should have values from car column
# diagonal values should be 0.

# In[2]:


def generate_car_matrix(data):
    
# Pivot the DataFrame to create the matrix
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

# Set diagonal values to 0
    for col in car_matrix.columns:
        car_matrix.loc[col, col] = 0
        return car_matrix

result_matrix = generate_car_matrix('dataset-1.csv')
print(result_matrix)


# Question 2: Car Type Count Calculation
# Create a Python function named get_type_count that takes the dataset-1.csv as a DataFrame. Add a new categorical column car_type based on values of the column car:
# 
# low for values less than or equal to 15,
# medium for values greater than 15 and less than or equal to 25,
# high for values greater than 25.
# Calculate the count of occurrences for each car_type category and return the result as a dictionary. Sort the dictionary alphabetically based on keys.

# In[3]:


def get_type_count(data):
 
 # For Creating a new column 'car_type' based on conditions
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]
    labels = ['low', 'medium', 'high']
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],labels=labels, right=False)

# Calculate the count of occurrences for each car_type category
    count_dict = df['car_type'].value_counts().sort_index().to_dict()
    return count_dict

result = get_type_count('dataset-1.csv')
print(result)


# Question 3: Bus Count Index Retrieval
# Create a Python function named get_bus_indexes that takes the dataset-1.csv as a DataFrame. The function should identify and return the indices as a list (sorted in ascending order) where the bus values are greater than twice the mean value of the bus column in the DataFrame.

# In[4]:


def get_bus_indexes(data):

#Calculate the mean of the 'bus' column
    bus_mean = df['bus'].mean()

#Identify indices where 'bus' values are greater than twice the mean
    bus_indexes = sorted(df[df['bus'] > 2 * bus_mean].index)
    return bus_indexes

result = get_bus_indexes('dataset-1.csv')
print(result)


# Question 4: Route Filtering
# Create a python function filter_routes that takes the dataset-1.csv as a DataFrame. The function should return the sorted list of values of column route for which the average of values of truck column is greater than 7.

# In[5]:


def filter_routes(data):
    
# Calculate average 'truck' values for each route
    route_avg_truck = df.groupby('route')['truck'].mean()

# Filter routes where the average 'truck' value is greater than 7
    filtered_routes = sorted(route_avg_truck[route_avg_truck > 7].index)
    return filtered_routes

result = filter_routes('dataset-1.csv')
print(result)


# Question 5: Matrix Value Modification
# Create a Python function named multiply_matrix that takes the resulting DataFrame from Question 1, as input and modifies each value according to the following logic:
# 
# If a value in the DataFrame is greater than 20, multiply those values by 0.75,
# If a value is 20 or less, multiply those values by 1.25.
# The function should return the modified DataFrame which has values rounded to 1 decimal place.

# In[6]:


def multiply_matrix(data):
    modified_matrix = data.copy()
    modified_matrix[data > 20] *= 0.75
    modified_matrix[data <= 20] *= 1.25
    modified_matrix = modified_matrix.round(1)
    return modified_matrix


# In[7]:


modified_result_matrix = multiply_matrix(result_matrix)
print(modified_result_matrix)


# Question 6: Time Check
# You are given a dataset, dataset-2.csv, containing columns id, id_2, and timestamp (startDay, startTime, endDay, endTime). The goal is to verify the completeness of the time data by checking whether the timestamps for each unique (id, id_2) pair cover a full 24-hour period (from 12:00:00 AM to 11:59:59 PM) and span all 7 days of the week (from Monday to Sunday).
# 
# Create a function that accepts dataset-2.csv as a DataFrame and returns a boolean series that indicates if each (id, id_2) pair has incorrect timestamps. The boolean series must have multi-index (id, id_2).

# In[9]:


data = pd.read_csv('dataset-2.csv')

# Check for NaN values in the crucial columns
print("Rows with NaN values in startDay, startTime, endDay, or endTime columns:")
print(data[data[['startDay', 'startTime', 'endDay', 'endTime']].isnull().any(axis=1)])


# In[10]:


print("Unique values in startDay column:")
print(data['startDay'].unique())

print("\nUnique values in startTime column:")
print(data['startTime'].unique())

print("\nUnique values in endDay column:")
print(data['endDay'].unique())

print("\nUnique values in endTime column:")
print(data['endTime'].unique())


# In[ ]:


Sorry to say I tried too much but i am ynot getting proper answer

