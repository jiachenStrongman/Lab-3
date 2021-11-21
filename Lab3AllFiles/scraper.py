#lab 3 scraper file
#scrape the table from - https://www.esrl.noaa.gov/gmd/aggi/aggi.html
#and store the data into database

from bs4 import BeautifulSoup
import requests
import pandas as pd
import webbrowser
import sqlite3

# https://www.esrl.noaa.gov/gmd/aggi/aggi.html

#creates beautifulSoup object from 'site' html text object
site = requests.get('https://www.esrl.noaa.gov/gmd/aggi/aggi.html').text
soup = BeautifulSoup(site, 'html.parser')

#i first use this to find all the tables on the page and from there i can determine which one to parse out
#for table in soup.find_all('table'):
#    print(table.get('class'))

#from the above ^ i got: ['table', 'table-bordered', 'table-condensed', 'table-striped', 'table-header']
#as the second table we need to work with on the assignment

table = soup.find('table', class_='table table-bordered table-condensed table-striped table-header')


#database functions from lab 1 and 2 with slight modifications to work here

class database:

    def __init__(self, ghouseDB):
        self.ghouseDB = sqlite3.connect('greenhouse.db')
        cursor = self.ghouseDB.cursor()
        print("Database connected")
        cursor.close()
        if(self.ghouseDB):
            self.ghouseDB.close()

    def table(self):
        self.ghouseDB = sqlite3.connect('greenhouse.db')
        greenTable = '''CREATE TABLE greenTable(
                        YEAR INTEGER PRIMARY KEY,
                        CO2 REAL, CH4 REAL,
                        N2O REAL, CFCs REAL,
                        HCFCs REAL, HFCs REAL);'''
        cursor = self.ghouseDB.cursor()
        print("Happy belated, table created")
        cursor.execute(greenTable)
        self.ghouseDB.commit()
        if(self.ghouseDB):
            self.ghouseDB.close()

    def insert(self, year, one, two, three, four, five, six):#its just easier to have it like this rather than the molecule
        self.ghouseDB = sqlite3.connect('greenhouse.db')
        cursor = self.ghouseDB.cursor()
        insertTab = '''INSERT INTO greenTable
                    (YEAR, CO2, CH4, N2O, CFCs, HCFCs, HFCs) VALUES (?, ?, ?, ?, ?, ?, ?)'''
        data_tuple = (year, one, two, three, four, five, six)
        cursor.execute(insertTab, data_tuple)
        self.ghouseDB.commit()
        cursor.close()
        if(self.ghouseDB):
            self.ghouseDB.close()

    def search(self): #retrieves data from specified year
        self.ghouseDB = sqlite3.connect('greenhouse.db')
        cursor = self.ghouseDB.cursor()
        cursor.execute('''SELECT YEAR, CO2, CH4, N2O, CFCs, HCFCs, HFCs FROM greenTable''')
        result = cursor.fetchall()
        return result
        

    def checkTable(self): #checks if the table already exsists so there isnt a runtime error everytime i test
        self.ghouseDB = sqlite3.connect('greenhouse.db')
        cursor = self.ghouseDB.cursor()
        cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name = 'greenTable' ''')
        if(cursor.fetchone()[0] == 1):
            return False
        else:
            return True
        cursor.close()
        if(self.ghouseDB):
            self.ghouseDB.close()
        
greenhouseDB = database([]) #initialize the database

if(greenhouseDB.checkTable()):
    greenhouseDB.table() #creates table if there isnt one

    for row in table.tbody.find_all('tr'): #inserts all the table data needed into database
        columns = row.find_all('td')
        if(columns != []):
            col = []
            for i in range(7):
                col.append(columns[i].text.strip())
            
            greenhouseDB.insert(col[0], col[1], col[2], col[3], col[4], col[5], col[6])
            
