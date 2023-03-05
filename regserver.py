#----------------------------------------------------------------------
# Author: Lois I. Omotara
# regserver.py
#----------------------------------------------------------------------
import databasesearch as ds
import socket 
import sys 
import argparse as ap 
import pickle
import os
import textwrap as tw
import classsearch as cs
#----------------------------------------------------------------------
# format each row for list given raw sqlite result row
def createRow(row): 
        rowstring = ''
        for i in range(5 - len(str(row[0]))):
            rowstring += 'space'
        rowstring += str(row[0])
        rowstring += '  '
        rowstring += str(row[1])
        for i in range (6 - len(str(row[2]))):
            rowstring+=' '
        rowstring += ' '
        rowstring += str(row[2])
        rowstring += ' '
        for i in range(4-len(str(row[3]))):
            rowstring += ' '
            print('NUM SPACE=',i)
        rowstring += str(row[3])
        if len(str(row[3])) == 0: 
            rowstring+= ' '
        rowstring += str(' '+row[4])
        return rowstring
# compile sqlite result string into tuple for client 
def handle_tuple(search_list,sock):
    result_list = []
    search = ds.DatabaseSearch()
    rawresults = search.fullsearch(idept=search_list[0], 
    iarea=search_list[1],icoursenum=search_list[2],
    ititle=search_list[3])
    for irow in rawresults: 
        result_list.append(createRow(row=irow))
    flo = sock.makefile(mode='wb')
    pickle.dump(result_list,flo)
    flo.flush()
    print('Wrote to client')

def format_string(generaltable, dept_and_num, prof_table):
    formatstring = ''
    general = generaltable[0]
    wrapper = tw.TextWrapper(width = 72, break_long_words=True)
    formatstring+='Course Id: '+str(general[0])+'\n'
    formatstring+='\n'
    formatstring+='Days: '+str(general[1])+'\n'
    formatstring+='Start time: '+str(general[2])+'\n'
    formatstring+='End time: '+str(general[3])+'\n'
    formatstring+='Building: '+str(general[4])+'\n'
    formatstring+='Room: '+str(general[5])+ '\n'
    formatstring+='\n'
    for row in dept_and_num:
        formatstring+='Dept and Number: '
        formatstring+=str(row[0])+' '+str(row[1])+'\n'
    formatstring+='\n'
    formatstring+= 'Area: '+str(general[6])+'\n'
    formatstring+='\n'
    titlestring = wrapper.wrap('Title: '+general[7])
    for line in titlestring:
        formatstring+=line+'\n'
    formatstring+='\n'
    descripstring = wrapper.wrap('Description: '+general[8])
    for line in descripstring:
        formatstring+=line+'\n'
    formatstring+='\n'
    prereqstring = wrapper.wrap('Prerequisites: '+general[9])
    for line in prereqstring:
        formatstring+=line+'\n'
    formatstring+='\n'
    for name in prof_table:
        formatstring+='Professor: '+name[0]+'\n'
    return formatstring

def handle_int(classid, sock): 
    searchresult = ''
    classstring = str(classid)
    search = cs.ClassSearch(classstring)
    gen = search.get_general()
    d_and_n = search.get_deptandnum()
    profs = search.get_prof()
    searchresult = format_string(generaltable = gen, 
    dept_and_num=d_and_n,
    prof_table=profs)
    flo = sock.makefile(mode='wb')
    pickle.dump(searchresult,flo)
    flo.flush()
    print('Wrote to client')

# connect to client 
def main(): 
    #--------------------parser-------------------------------
    parser = ap.ArgumentParser(prog='regserver.py',
    usage='regserver.py [-h] port',
    description='Server for the registrar application')
    parser.add_argument('port',
                        help='the port at which the server should listen',
                        type=int)
    args = parser.parse_args()
    #---------------listen---------------------------------
    port = args.port
    server_sock = socket.socket()
    print('Opened socket server')
    if os.name != 'nt': 
         server_sock.setsockopt(
              socket.SOL_SOCKET, socket.SO_REUSEADDR,1
         )
    server_sock.bind(('',port))
    server_sock.listen()

    while True: 
        try: 
             #------------connect to client----------------
             isock, client_addr = server_sock.accept()
             with isock: 
                  print('Accepted connection at:', client_addr)
                  inputflo = isock.makefile(mode ='rb')
                  print('GOT TO MAKEFILE')
                  search_input = pickle.load(inputflo)
                  print(type(search_input))
                  print('Recieved input')
                  if(type(search_input) == int): 
                    handle_int(classid=search_input,sock=isock)
                  else: 
                    handle_tuple(search_list=search_input, sock=isock)
                  print('Resolved search')
        except Exception as ex: 
             print(ex, file=sys.stderr)

if __name__ == '__main__': 
    main()
        
    
