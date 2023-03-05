#----------------------------------------------------------------------
# reg.py
# Author: Lois I Omotara
#----------------------------------------------------------------------
import argparse as ap
import sys
import socket
import pickle
import PyQt5.QtWidgets as widget
import PyQt5.QtGui as gui
#----------------------------------------------------------------------
def create_control_frame(dept, coursenum, area, title,submit):
    #------------- control frame layout------------
    dept_label = widget.QLabel(' Dept:')
    num_label = widget.QLabel(' Number: ')
    area_label = widget.QLabel(' Area: ')
    title_label = widget.QLabel(' Title: ')
        #-------------submit button-------------------
    layout = widget.QGridLayout()
    layout.setSpacing(4)
    layout.setContentsMargins(4,4,4,4)
    #--------------labels---------------------------
    layout.addWidget(dept_label,0,0,1,1)
    layout.addWidget(area_label,1,0,1,1)
    layout.addWidget(num_label,2,0,1,1)
    layout.addWidget(title_label,3,0,1,1)
    #-------------textfields------------------------
    layout.addWidget(dept,0,1,1,1)
    layout.addWidget(area,1,1,1,1)
    layout.addWidget(coursenum,2,1,1,1)
    layout.addWidget(title,3,1,1,1)
    #-----------button------------------------------
    layout.addWidget(submit,1,2,2,1)
    #---------formatting----------------------------
    layout.setRowStretch(0,0)
    layout.setRowStretch(1,0)
    layout.setRowStretch(2,0)
    layout.setRowStretch(3,0)
    layout.setColumnStretch(0,0)
    layout.setColumnStretch(1,1)
    layout.setColumnStretch(2,0)
    layout.setColumnStretch(3,0)
    #----------------control_frame------------------
    control_frame = widget.QFrame()
    control_frame.setLayout(layout)
    return control_frame

def create_list_frame(result_list):
    #---------------list frame layout---------------
    listlayout = widget.QGridLayout()
    listlayout.setSpacing(0)
    listlayout.setContentsMargins(0,0,0,0)
    listlayout.addWidget(result_list,0,0,1,1)
     #-------------list_frame------------------------
    list_frame = widget.QFrame()
    list_frame.setLayout(listlayout)
    return list_frame

def create_central_frame(control_frame, list_frame):
    central_frame_layout = widget.QGridLayout()
    central_frame_layout.setSpacing(0)
    central_frame_layout.setContentsMargins(0,0,0,0)
    central_frame_layout.setRowStretch(0,0)
    central_frame_layout.setRowStretch(1,1)
    central_frame_layout.setColumnStretch(0,1)
    central_frame_layout.addWidget(control_frame,0,0)
    central_frame_layout.addWidget(list_frame,1,0)
    #--------------central_frame-------------------
    central_frame = widget.QFrame()
    central_frame.setLayout(central_frame_layout)
    return central_frame

def parser(): 
    #-------------parser------------------------------
    parser = ap.ArgumentParser(prog = "reg.py",
    usage= "reg.py [-h] host port",
    description= "Client for the registrar application")
    parser.add_argument('host',
    help="the host on which the server is running")
    parser.add_argument('port',
    help="the port at which the server is listening",
    type=int)
    return parser.parse_args()

def initialize_list(host, port,window,result_list): 
    try: 
        with socket.socket() as sock: 
            sock.connect((host,port))
            print('Connected to server')
            #--------------text data----------------------
            inputlist = ['','','','']
            inputflo = sock.makefile(mode='wb')
            pickle.dump(inputlist,inputflo)
            inputflo.flush()
            print("Sent command get_classes")
            flo = sock.makefile(mode='rb')
            # will need to recieve a list where each item is a row of the query result
            query_result = pickle.load(flo)
            if query_result == 'Error': 
                widget.QMessageBox.critical(window, 'Server Error', 
                '''A server error occured.
                 Please contact the system administrator''')
                return
            i = 0
            for result in query_result:
                fontresult = widget.QListWidgetItem(result)
                fontresult.setFont(gui.QFont('Courier',10))
                result_list.insertItem(i, fontresult)
                result_list.setCurrentRow(0)
                i+=1
    except Exception as ex:
        widget.QMessageBox.critical(window,'Server Error', str(ex))

def submit_slot_helper(window, host,port,inputlist,result_list): 
    try:
        with socket.socket() as sock:
            sock.connect((host,port))
            print('Connected to server')
        #--------------text data----------------------
            inputflo = sock.makefile(mode='wb')
            pickle.dump(inputlist,inputflo)
            inputflo.flush()
            print("Sent command get_classes")
            flo = sock.makefile(mode='rb')
            query_result = pickle.load(flo)
            if query_result == 'Error':
                widget.QMessageBox.critical(window, 'Server Error',
                '''A server error occured.
                    Please contact the system administrator''')
                return 
            i=0
            result_list.clear()
            for result in query_result: 
                fontresult = widget.QListWidgetItem(result)
                fontresult.setFont(gui.QFont('Courier',10))
                result_list.insertItem(i, fontresult) 
                result_list.setCurrentRow(0)
                i+=1
    except Exception as ex: 
        widget.QMessageBox.critical(window, 'Server Error ', ex)
    
def main():
    args = parser()
    host = args.host
    port = args.port
    #-----------gui-----------------------------------
    app = widget.QApplication(sys.argv)
        #----------text fields------------------------
    dept = widget.QLineEdit('')
    coursenum = widget.QLineEdit('')
    area = widget.QLineEdit('')
    title = widget.QLineEdit('')
        #-------------submit button-------------------
    submit = widget.QPushButton('Submit')
        #-------------list box------------------------
    result_list = widget.QListWidget()
        #------------window---------------------------
    window = widget.QMainWindow()
        #--------------submit button slot------------------
    def submit_slot():
        #-------------client----------------------
        inputlist = [dept.text(), area.text(),
        coursenum.text(),title.text()]
        submit_slot_helper(window,host,port,inputlist,result_list)

    submit.clicked.connect(submit_slot)
        #--------------list option slot------------------
    def class_slot(selected_item):
        try: 
            selected = selected_item.text()
            with socket.socket() as sock: 
                sock.connect((host,port))
                print('Connected to server')
                selected_split = selected.split(' ')
                classid = 0
                if len(selected_split[0])< 3: 
                    classid += int(selected_split[1])
                else: 
                    classid += int(selected_split[0])
                input_data= sock.makefile(mode='wb')
                pickle.dump(classid,input_data)
                input_data.flush()
                print('Sent commmand get_overview')
                flo = sock.makefile('rb')
                class_info = pickle.load(flo)
                if class_info is False: 
                    print('No class with classid '+str(classid)+' exists',
                    file=sys.stderr)
                    return
                if class_info == 'Error': 
                    widget.QMessageBox.critical(window, 'Server Error', 
                    '''A server error occured.
                     Please contact the system administrator''')
                    return
                widget.QMessageBox.information(window, 'Class Details',
                class_info)
        except Exception as ex: 
            widget.QMessageBox.critical(window, 'Server Error',ex)

    result_list.itemActivated.connect(class_slot)         
        #----------------control frame-----------------
    control_frame = create_control_frame(dept, coursenum, area,
        title,submit)
        #---------------list frame --------------
    list_frame = create_list_frame(result_list)
        #---------------central frame layout-----------
    central_frame = create_central_frame(control_frame, list_frame)
        #-------------window----------------------------
    window.setCentralWidget(central_frame)
    screen_size = widget.QDesktopWidget().screenGeometry()
    window.resize (screen_size.width()//2,screen_size.height()//2)
    window.setWindowTitle('Princeton University Class Search')
    window.show()
    initialize_list(host,port,window,result_list)
    #-----------initial list-------------------------
    sys.exit(app.exec_())
#----------------------------------------------------------------------
if __name__ == '__main__':
    main()
