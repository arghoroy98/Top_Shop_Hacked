# -*- coding: utf-8 -*-

"""

@author: Argho
"""

import sqlite3
import uuid

from selenium import webdriver
from collections import OrderedDict
from operator import itemgetter

def SortDict(my_dict, key):
    if (key == 'n'):
        my_dict = OrderedDict(sorted(my_dict.items(), key = itemgetter(0)))
    else:
        my_dict = OrderedDict(sorted(my_dict.items(), key = itemgetter(1)))
    
    return my_dict


def DictionaryFill(my_element, dict_main):
    #To avoid page loading problems, we will use a while loop to check if each element has loaded correctly
    i = 0
    PriceList = []
    GameList = []
    
    length = len(my_element)
    #print(length)
    
    
    while (i<length):
        element = my_element[i].text
        element = element.split('\n')
        
        #Sometimes, the price doesn't load correctly, so I keep loading the element text
        #until the price is in the correct position
        if (element[3][0] != '$'):
            i = i-1
        else:
            GameList.append(element[0])
            PriceList.append(element[3])
        i = i+1
    
    #print(GameList)
    #print(PriceList)
    
    for game in GameList:
        for price in PriceList:
            dict_main[game] = price
            PriceList.remove(price)
            break

    return dict_main

def main():
    conn = sqlite3.connect('./' + 'walmart.db')
    c = conn.cursor()
    user_input = input("Press u to update database:\nPress d to display database:").lower()
    if user_input == 'u':
        driver = webdriver.Chrome()
        driver.get('https://www.walmart.ca/en/video-games/N-22+120')
        my_element = driver.find_elements_by_class_name('product-details-container')
        my_element = list(my_element)
        
        Item_dictionary = {}
        
        Item_dictionary = DictionaryFill(my_element, Item_dictionary)
            
        while(True):
            try:
                next_page = driver.find_element_by_id('loadmore')
            except Exception:
                break
            link = next_page.get_attribute('href')
            driver.get(link)
            next_element = driver.find_elements_by_class_name('product-details-container')
            next_element = list(next_element)
            Item_dictionary = DictionaryFill(next_element, Item_dictionary)
        
        
        user_input = input("Sort by name or price? Enter 'n' for name or 'p' for price: ").lower() 
        #This will sort the dictionary by name or by price
        Item_dictionary = SortDict(Item_dictionary, user_input)
        
        database(c,conn,Item_dictionary.items())   
        driver.quit()
        
    display_items(c,conn)
    


def database(c,conn,items):    
    c.execute('''DELETE FROM items''')
    conn.commit()

    c.execute('''VACUUM''')
    conn.commit()
    
    add_items(c,conn,items)
    
    
def add_items(c, conn, items):
                
    for game,price in items:
        uid = str(uuid.uuid4())[:4]
        c.execute('''INSERT INTO items VALUES (:uid, :name, :availability, :price)''',
                      {'uid': uid, 'name': game, 'availability': '1', 'price': price})
        conn.commit()

def display_items(c,conn):
    c.execute(''' SELECT * FROM items ''')
    temp = c.fetchall()
    conn.commit()
    
    i = 1
    for element in temp:
        print(str(i) + ")    " + element[1] + "        " + element[3])
        i = i + 1


main()





































