# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 10:39:37 2023

@author: hp
"""

from random import randint
from cryptography.fernet import Fernet
import pandas as pd
import random
import time

start_time = time.time()
# original dataset
path= "C:/Users/hp/OneDrive/Desktop/hotel_booking.csv"

# Fake names repository
WORD_FILE = 'C:/Users/hp/OneDrive/Desktop/names.csv'     

df = pd.read_csv(path)[0:20]  # sample test
# generate additional columns into dataset
df["Hotel_names"]=''
df["Mask_Hotel_names"]=''
df["encrypt_Hotel_names"]=''
df["decrypted_Hotel_names"]=''


# generate fake hotel name, code can generate more than one hotel in single cell
def fake_hotel_name(num):
                                                                                    
    WORDS = open(WORD_FILE).read().splitlines() 

    fake_hotel_names = []
    
    for i in range (num):
        # this loop to define length of hotel name (how many words in name)
        x=''
        for _ in range(randint(2, 4)):
            x += WORDS[randint(0, len(WORDS)-1)] + " " 
        fake_hotel_names.append(x)
    return (fake_hotel_names)

# masking technique
def replace_string_seed(s):
    result = ""
    #random.seed(2000)  # Use a fixed seed
    for ch in s:
        if ch.isalpha():
            result += random.choice([c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
        elif ch.isdigit():
            result += random.choice([c for c in "0123456789"])
        else:
            result += ch
    return result


def encrypt(s):
    decrypted=[]
    # Generate a Fernet key
    key = Fernet.generate_key()
    # Encrypt the column
    fernet = Fernet(key)
    encrypted_string = fernet.encrypt(bytes(s, encoding ='utf8'))
    decrypted_string = fernet.decrypt(bytes(encrypted_string))
    decrypted.append(decrypted_string)
    return [encrypted_string, decrypted_string]


# adding column with fake hotel names
for i in range (len (df["Hotel_names"])):
    df["Hotel_names"].loc[i]= fake_hotel_name(1)[0]
# masking for hotel_names column
    df["Mask_Hotel_names"].loc[i]= replace_string_seed(df["Hotel_names"].loc[i])
# encryption for hotel_names column
    df["encrypt_Hotel_names"].loc[i]= encrypt(df["Hotel_names"].loc[i])[0]
# decryption for hotel_names column
    df["decrypted_Hotel_names"].loc[i]= encrypt(df["Hotel_names"].loc[i])[1]
# save the dataframe into csv    
df.to_csv('outfile.csv', sep=',', encoding='utf-8')
    
    
# (print elapsed time since start)
print("--- %s seconds ---" % (time.time() - start_time))