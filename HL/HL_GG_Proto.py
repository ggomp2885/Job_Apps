#!/usr/bin/env python
# coding: utf-8

# # Greg Gompers completed notebook for the HL_GG Proto Project 
# In this notebook, I have parsed the binary file with python to read and display the 5 necessary outputs

# ##### General Imports

# In[9]:


import numpy as np
import pandas as pd


# ##### Pandas Settings

# In[10]:


pd.set_option('max_rows', 500)


# ##### Setting up empty DataFrame with format from file

# In[11]:


with open('txnlog.dat', 'rb') as file:
    dt = np.dtype([('Record_type', '>V1'), ('Unix_timestamp', '>u4'),
                           ('User_ID', '>u8'),('Amount_in_dollars', '>f8')])
    records = np.fromfile('txnlog.dat', dt, count=0, offset=9)
    df = pd.DataFrame(records)


# ##### Large Loop to read binary file and assign binary format based on the byte that is found

# In[12]:


# Initialization of variables
byte_count = -1
last_byte = -12
auto_start_count = 0
auto_end_count = 0

# This function starts by opening the .dat file, and runs a for loop over each individual byte.
# I have used several conditional statements to check for the appearance of the enum characters,
# depending on the enum character found, the format is then setup for recording the following bytes,
# first, into a temporary dataframe to get the format setup, and then I appended this into the master dataframe (df)
# Because the bytes 'b\x00' and b'\x01' had a tendancy to appear even when not signifying the enum character,
# I built in a "distance_between_bytes" variable to ensure that the loop was only picking up
# the enum bytes when they appeared in the expected position. Lastly, I commented out the print
# statements I had been using along the way to ensure it was working as intended.
# These can be re-commented in and you will be able to see the process I was using. 
# Great Project!

with open('txnlog.dat', 'rb') as file:
    for byte in iter(lambda: file.read(1), b''):
        byte_count += 1
#         print('byte_count = {}'.format(byte_count))
        d_between_bytes = byte_count - last_byte
        if byte_count > 8:
            if (b'\x00' in byte or b'\x01' in byte) and d_between_bytes in [13, 21]:
#                 print()
#                 print('bytes between last entry = {}'.format(byte_count - last_byte))
#                 print(byte)
#                 print('^this byte indicates a DEBIT or CREDIT')
#                 print('last_byte = {}'.format(last_byte))
                dt = np.dtype([('Record_type', '>V1'), ('Unix_timestamp', '>u4'),
                               ('User_ID', '>u8'),('Amount_in_dollars', '>f8')])
                records = np.fromfile('txnlog.dat', dt, count=1, offset=byte_count)
                temp_df = pd.DataFrame(records)
                df = df.append(temp_df, ignore_index=True)
                last_byte = byte_count
    
            elif (b'\x02' in byte or b'\x03' in byte) and d_between_bytes in [13, 21]:
#                 print()
#                 print('bytes between last entry = {}'.format(byte_count - last_byte))
#                 print(byte)
#                 print('^ this byte indicates starting autopay or ending autopay')
#                 print('last_byte = {}'.format(last_byte))
                dt = np.dtype([('Record_type', '>V1'), ('Unix_timestamp', '>u4'),
                               ('User_ID', '>u8')])
                records = np.fromfile('txnlog.dat', dt, count=1, offset=byte_count)
                temp_df = pd.DataFrame(records)
                df = df.append(temp_df, ignore_index=True)
                last_byte = byte_count
                if b'\x02' in byte:
                    auto_start_count +=1
                if b'\x03' in byte:
                    auto_end_count +=1

# display(df)


# ##### Summations and count calculations

# In[13]:


# Here I have done the pandas calculations to sum for the variables needed,
# I also commented out the print statements I used while building, these can
# be re-commented in and you will be able to see the process I was using


# Summation of credits
total_c_df = df[df['Record_type'] == b'\x01']
total_c = total_c_df['Amount_in_dollars'].sum()
# display(len(total_c_df))
# display(total_c_df)
# print(total_c)

# Summation of debits
total_d_df = df[df['Record_type'] == b'\x00']
total_d = total_d_df['Amount_in_dollars'].sum()
# display(len(total_d_df))
# display(total_d_df)
# print(total_d)

# Summation of User 245's balance
user_df = df[df['User_ID'] == 2456938384156277127]
user_bal = user_df.iloc[0,3] - user_df.iloc[1,3]
# display(len(user_df))
# display(user_df)
# print(user_bal)


# ##### Complete printout

# In[14]:


print('total credit amount = {}'.format(total_c))
print('total debit amount = {}'.format(total_d))
print("autopays started = {}".format(auto_start_count))
print("autopays ended = {}".format(auto_end_count))
print('balance for user 2456938384156277127 = {}'.format(user_bal))


# #### Greg Gompers - HL_Proto Project complete
