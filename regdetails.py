#----------------------------------------------------------------------
# regdetails.py
# Author: Lois I Omotara
#----------------------------------------------------------------------
import argparse as ap
import sys
import sqlite3
import textwrap as tw
import classsearch as cS
#----------------------------------------------------------------------
def format_print(generaltable, dept_and_num, prof_table):
    general = generaltable[0]
    wrapper = tw.TextWrapper(width = 72, break_long_words=True)
    print('Course Id:',general[0])
    print()
    print('Days:',general[1])
    print('Start time:',general[2])
    print('End time:', general[3])
    print('Building:',general[4])
    print('Room:', general[5])
    print()
    for row in dept_and_num:
        print('Dept and Number: ', end='')
        print(row[0]+' '+row[1])
    print()
    print('Area:',general[6])
    print()
    titlestring = wrapper.wrap('Title: '+general[7])
    for line in titlestring:
        print(line)
    print()
    descripstring = wrapper.wrap('Description: '+general[8])
    for line in descripstring:
        print(line)
    print()
    prereqstring = wrapper.wrap('Prerequisites: '+general[9])
    for line in prereqstring:
        print(line)
    print()
    for name in prof_table:
        print('Professor:', name[0])
def main():
    try:
        parser = ap.ArgumentParser(prog = "regdetails.py",
        usage="regdetails.py [-h] classid",
        description="Registrar application: "+
        "show details about a class",
        allow_abbrev=False )
        parser.add_argument('classid',
        help='the id of the class whose details should be shown',
        type=int)
        args =  parser.parse_args()
        search = cS.ClassSearch(args.classid)
        gen = search.get_general()
        d_and_n = search.get_deptandnum()
        profs = search.get_prof()
        if bool(gen) is False:
            raise Exception("no class with classid "+
            str(args.classid)+" exists")
        format_print(generaltable = gen, dept_and_num=d_and_n,
        prof_table=profs)
    except ap.ArgumentError as ex:
        print("regdetails.py:",ex,file=sys.stderr)
        sys.exit(2)
    except sqlite3.Error as ex:
        print("regdetails.py:",ex,file=sys.stderr)
        sys.exit(1)
    except Exception as ex:
        print("regdetails.py:",ex,file=sys.stderr)
        sys.exit(1)
if __name__ == '__main__' :
    main()
