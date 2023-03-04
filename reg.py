#----------------------------------------------------------------------
# reg.py
# Author: Lois I Omotara
#----------------------------------------------------------------------
import argparse as ap
import PyQt5.QtWidgets as widget
import sys
#----------------------------------------------------------------------
def main(): 
    #-------------parser------------------------------
    parser = ap.ArgumentParser(prog = "reg.py", 
    usage= "reg.py [-h] host port", 
    description= "Client for the registrar application")
    parser.add_argument('host', 
    help="the host on which the server is running")
    parser.add_argument('port', 
    help="the port at which the server is listening")
    #-----------gui-----------------------------------
    app = widget.QApplication(sys.argv)
        #--------------text fields--------------------
    dept = widget.QLineEdit('dept')
    coursenum = widget.QLineEdit('coursenum')
    area = widget.QLineEdit('area')
    title = widget.QLineEdit('title')
        #--------------text data----------------------
    dept_text = dept.text()
    coursenum_text = coursenum.text()
    area_text = area.text()
    title_text = title.text()
        #--------------submit button------------------
    submit = widget.QPushButton('submit')
    def submit_slot(): 
        # communicate with server to get query searches 
    query_result = #response from server
    submit.clicked.connect(submit_slot)
        #-------------list box------------------------
    result_list = widget.QListWidget
    for result in query_result: 
        result_list.insertItem(result) 
    result_list.setCurrentRow(1)
        #------------layout--------------------------
        


    




#----------------------------------------------------------------------
if __name__ == '__main__': 
    main()