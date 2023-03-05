#----------------------------------------------------------------------
# Author: Lois I Omotara
# alllist.py
#----------------------------------------------------------------------
import databasesearch as ds 

def fill_reg(table):
    for row in table:
        for i in range(5 - len(str(row[0]))):
            print(' ',end='')
        print(row[0], end='')
        print(' ', row[1], end='')
        for i in range (6 - len(str(row[2]))):
            print(' ', end='')
        print(' ',end='')
        print(row[2], end='')
        print(' ',end='')
        for i in range(4-len(str(row[3]))):
            print(' ',end='')
        print(row[3],end='')
        print('',row[4])

def main(): 
    search = ds.DatabaseSearch()
    allentries = search.getall()
    
