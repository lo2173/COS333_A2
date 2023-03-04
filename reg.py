#----------------------------------------------------------------------
# reg.py
# Author: Lois I Omotara
#----------------------------------------------------------------------
import argparse as ap
import PyQt5.QtWidgets as widget
import sys
import socket 
import pickle
#----------------------------------------------------------------------

def main(): 
    try: 
        #-------------parser------------------------------
        parser = ap.ArgumentParser(prog = "reg.py", 
        usage= "reg.py [-h] host port", 
        description= "Client for the registrar application")
        parser.add_argument('host', 
        help="the host on which the server is running")
        parser.add_argument('port', 
        help="the port at which the server is listening")
        args = parser.parse_args
        host = args.host
        port = args.port 
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
        inputlist = [dept_text, coursenum_text, area_text, title_text]
            #--------------submit button------------------
        submit = widget.QPushButton('submit')
        query_result_ = []
        def submit_slot(result): 
                #-------------server----------------------
                # have to deal with security 
                with socket.socket() as sock: 
                    sock.connect((host,port))
                    input = sock.makefile(mode='wb')
                    pickle.dump(inputlist,input)
                    input.flush
                    print("Sent command: get overviews")
                    flo = sock.makefile(mode='rb')
                    query_result_.append = pickle.load(flo)

        submit.clicked.connect(submit_slot)
            #-------------list box------------------------
        result_list = widget.QListWidget
        for result in query_result_[0]: 
            result_list.insertItem(result) 
        result_list.setCurrentRow(1)
            #------------layout--------------------------
            # question boxes in top 1/3 and list box in bottom 
        layout = widget.QGridLayout()

    except Exception as ex: 
        print(ex, file=sys.stderr); 
        sys.exit(1)

#----------------------------------------------------------------------
if __name__ == '__main__': 
    main()