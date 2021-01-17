# -*- coding: utf-8 -*-
"""

@author: Argho
"""

import sqlite3
import uuid

from selenium import webdriver


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
        if (element[4][0] != '$'):
            i = i-1
        else:
            GameList.append(element[0])
            PriceList.append(element[4])
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
        driver.get('https://www.toysrus.ca/en/toysrus/Category/Video-Games#12')
        
        
        
        while True:
            try:
                max_count = driver.find_element_by_class_name('b-plp_header-results_count').text.split(" ")
                number = max_count[3]
                break
            except IndexError:
                number = max_count[1]
                break
            except AttributeError:
                pass
            except:
                pass
            
        print("boom")
        while True:
            try:
                total_count = driver.find_element_by_class_name('b-plp_header-results_count').text.split(" ")[1]
                if total_count == number:
                    break
            except:
                pass
        
        my_element = driver.find_elements_by_class_name('b-product_tile-caption')
        my_element = list(my_element)
        
        Item_dictionary = {}
        Item_dictionary = DictionaryFill(my_element, Item_dictionary)
        database(c,conn,Item_dictionary.items())
        driver.quit()

    display_items(c,conn)


def database(c,conn,items):    
    c.execute('''DELETE FROM items_2''')
    conn.commit()

    c.execute('''VACUUM''')
    conn.commit()
    
    add_items(c,conn,items)
    
    
def add_items(c, conn, items):
                
    for game,price in items:
        uid = str(uuid.uuid4())[:4]
        c.execute('''INSERT INTO items_2 VALUES (:uid, :name, :availability, :price)''',
                      {'uid': uid, 'name': game, 'availability': '1', 'price': price})
        conn.commit()

def display_items(c,conn):
    c.execute(''' SELECT * FROM items_2 ''')
    temp = c.fetchall()
    conn.commit()
    
    i = 1
    for element in temp:
        print(str(i) + ")    " + element[1] + "        " + element[3])
        i = i + 1



    
main()