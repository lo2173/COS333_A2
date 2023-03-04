#----------------------------------------------------------------------
# formatable.py
# Author: Lois I Omotara
#----------------------------------------------------------------------
import textwrap as tw
class FormatTable:
    def create_columns(self,listcols):
        for title in listcols:
            if title == listcols[len(listcols)-1]:
                print(title,end='')
            else:
                print(title, end=' ')
        print()
        for title in listcols :
            for i in range(len(title)):
                print('-', end='')
            if title != listcols[len(listcols)-1]:
                print(' ', end='')
        print()
    def fill_reg(self,table):
        wrapper = tw.TextWrapper(width=49,break_long_words=False)
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
            titlelist = wrapper.wrap(row[4])
            print('',titlelist[0])
            for title in titlelist:
                if title !=titlelist[0]:
                    for i in range(23):
                        print(' ',end='')
                    print(title)
