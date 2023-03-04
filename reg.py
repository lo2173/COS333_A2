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
    #-------------parser------------------------------
    parser = ap.ArgumentParser(prog = "reg.py", 
    usage= "reg.py [-h] host port", 
    description= "Client for the registrar application")
    parser.add_argument('host', 
    help="the host on which the server is running")
    parser.add_argument('port', 
    help="the port at which the server is listening",
    type=int)
    args = parser.parse_args()
    host = args.host
    port = args.port 
    #-----------gui-----------------------------------
    app = widget.QApplication(sys.argv)
        #--------------text fields--------------------
    dept = widget.QLineEdit('dept')
    coursenum = widget.QLineEdit('coursenum')
    area = widget.QLineEdit('area')
    title = widget.QLineEdit('title')
        #-------------submit button-------------------
    submit = widget.QPushButton('submit')
        #-------------list box------------------------
    result_list = widget.QListWidget
        #--------------text data----------------------
    dept_text = dept.text()
    coursenum_text = coursenum.text()
    area_text = area.text()
    title_text = title.text()
    inputlist = [dept_text, coursenum_text, area_text, title_text]
        #--------------submit button slot------------------
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
                # will need to recieve a list where each item is a row of the query result
                query_result = pickle.load(flo)
                for result in query_result: 
                    result_list.insertItem(result) 
                    result_list.setCurrentRow(1)
    submit.clicked.connect(submit_slot)
        #-------------layout--------------------------
    layout = widget.QGridLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0,0,0,0)
    layout.addWidget(dept,0,0,1,2)
    layout.addWidget(area,1,0,1,2)
    layout.addWidget(coursenum,2,0,1,2)
    layout.addWidget(area,3,0,1,2)
    layout.addWidget(submit,2,2,1,1)
    layout.addWidget(result_list,4,0,1,3)
    layout.setRowStretch(4,2)
    layout.setColumnStretch(0,1)
    layout.setColumnStretch(1,1)
        #----------------frame--------------------------
    frame = widget.QFrame()
    frame.setLayout(layout)
        #-------------window----------------------------
    window = widget.QMainWindow()
    window.setCentralWidget(frame)
    screen_size = widget.QDesktopWidget().screenGeometry()
    window.resize = (screen_size.width()//2,screen_size.height()//2)
    window.setWindowTitle('Princeton University Class Search')
    window.show()
    sys.exit(app.exec_())
#----------------------------------------------------------------------
if __name__ == '__main__': 
    main()