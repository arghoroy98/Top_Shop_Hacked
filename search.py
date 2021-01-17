# -*- coding: utf-8 -*-
"""

@author: Argho
"""

import sqlite3


def main():
    conn = sqlite3.connect('./' + 'walmart.db')
    c = conn.cursor()
    user_input = input("What item would you like to search for")
    
    user_input = '%'+str(user_input)+'%' 
    c.execute('''SELECT * FROM items
                    WHERE name LIKE :user_input''',{
                    'user_input': user_input})
                  
    temp = c.fetchall()
    conn.commit()
    
    c.execute('''SELECT * FROM items_2
                    WHERE name LIKE :user_input''',{
                    'user_input': user_input})
                  
    temp_2 = c.fetchall()
    conn.commit()
    
    for element in temp:
        print('Walmart', end = ")       ")
        print(element[1:])
        
    for element in temp_2:
        print('ToysRUs', end = ")       ")
        print(element[1:])
        
        
main()