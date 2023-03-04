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
#----------------------------------------------------------------------
# format each row for list given raw sqlite result row
def createRow(row): 
        rowstring = ''
        for i in range(5 - len(str(row[0]))):
            rowstring += ' '
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
        rowstring += str(row[3])
        rowstring += str(' '+row[4])
        return rowstring
# compile sqlite result string into tuple for client 
def handle_client(search_list,sock):
    result_list = []
    search = ds.DatabaseSearch()
    rawresults = search.fullsearch(idept=search_list[0], 
    iarea=search_list[1],icoursenum=search_list[2],
    ititle=search_list[3])
    for irow in rawresults: 
        result_list.append(createRow(row=irow))
    flo = sock.makefile(mode='wb')
    pickle.dump(result_list,flo)
    print('Wrote to client')
# connect to client 
def main(): 
    #--------------------parser-------------------------------
    parser = ap.ArgumentParser(prog='regserver.py',
    usage='regserver.py [-h] port',
    description='Server for the registrar application')
    parser.add_argument('port',
    help='the port at which the server should listen')
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
                  input_string = isock.makefile(mode='rb')
                  search_input = pickle.load(input_string)
                  print('Recieved input')
                  handle_client(search_list=search_input, sock=isock)
                  print('Resolved search')
        except Exception as ex: 
             print(ex, file=sys.stderr)

if __name__ == '__main__': 
    main()
        
    