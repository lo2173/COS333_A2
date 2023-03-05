#----------------------------------------------------------------------
# reg.py
# Author: Lois I Omotara
#----------------------------------------------------------------------
import argparse as ap
import PyQt5.QtWidgets as widget
import sys
import socket 
import pickle
# 
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
        #--------------labels------------------------
    dept_label = widget.QLabel(' Dept:')
    num_label = widget.QLabel(' Number: ')
    area_label = widget.QLabel(' Area: ')
    title_label = widget.QLabel(' Title: ')
        #--------------text fields--------------------
    dept = widget.QLineEdit('')
    coursenum = widget.QLineEdit('')
    area = widget.QLineEdit('')
    title = widget.QLineEdit('')
        #-------------submit button-------------------
    submit = widget.QPushButton('submit')
        #-------------list box------------------------
    result_list = widget.QListWidget()
        #--------------text data----------------------
    dept_text = dept.text()
    coursenum_text = coursenum.text()
    area_text = area.text()
    title_text = title.text()
    inputlist = [dept_text, coursenum_text, area_text, title_text]
        #--------------submit button slot------------------
    def submit_slot(result): 
            #-------------client----------------------
            # have to deal with security 
            with socket.socket() as sock: 
                sock.connect((host,port))
                print('Connected to server')
                input = sock.makefile(mode='wb')
                pickle.dump(inputlist,input)
                input.flush
                print("Sent command: get overviews")
                flo = sock.makefile(mode='rb')
                # will need to recieve a list where each item is a row of the query result
                query_result = pickle.load(flo)
                i = 0 
                for result in query_result: 
                    result_list.insertItem(i, result) 
                    result_list.setCurrentRow(1)
                    i+=1

    submit.clicked.connect(submit_slot)
        #--------------list option slot------------------
    def class_slot(selected_item):
        selected = selected_item.text()
        with socket.socket() as sock: 
            sock.connect((host,port))
            print('Connected to server')
            selected_split = selected.split(' ')
            print("FIRST: "+selected_split[0])
            print("SECOND: "+selected_split[1])
            classid = 0
            if len(selected_split[0])< 3: 
                classid += int(selected_split[1])
            else: 
                classid += int(selected_split[0])
            input = sock.makefile(mode='wb')
            print('sent classid')
            pickle.dump(classid,input)
            input.flush 
            flo = sock.makefile('rb')
            class_info = pickle.load(flo)
            widget.QMessageBox.information(window, 'Class Details',
            class_info)
            
    result_list.itemActivated.connect(class_slot)         
        #-------------layout--------------------------
    layout = widget.QGridLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0,0,0,0)
            #--------------labels---------------------
    layout.addWidget(dept_label,0,0,1,1)
    layout.addWidget(area_label,1,0,1,1)
    layout.addWidget(num_label,2,0,1,1)
    layout.addWidget(title_label,3,0,1,1)
            #-------------textfields-------------------
    layout.addWidget(dept,0,1,1,1)
    layout.addWidget(area,1,1,1,1)
    layout.addWidget(coursenum,2,1,1,1)
    layout.addWidget(title,3,1,1,1)
            #-----------button-------------------------
    layout.addWidget(submit,2,2,1,1)
            #------------list--------------------------
    layout.addWidget(result_list,4,0,1,3)
            #---------formatting-----------------------
    layout.setRowStretch(4,3)
    layout.setColumnStretch(1,3)
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
