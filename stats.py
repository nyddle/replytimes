#! /usr/bin/python
#import sqlalchemy

import sys
import re
import imaplib
import pytz
import time
import MySQLdb
from datetime import datetime
from calendar import timegm

from statistics import median

DB_HOST = "95.85.22.116"
DB_USER = "replytimes"
DB_PASSWORD = "1Jx2VLSbi1TPE6rPIW"
DB_BASE = "replytimes"
DB_CHARSET = "utf8"

def getdb():
    return MySQLdb.connect( host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD, db = DB_BASE, charset = DB_CHARSET, connect_timeout = 10 )

def inbox():
    db = getdb()
    db.query("""SELECT fromaddr, toaddr, TIMESTAMP(datetime), is_question, msgid, replyto_msgid FROM message""")

    r=db.store_result()
    threads = {}
    heroes = {}


    data = r.fetch_row(100000)

    #print data

    sorted_data = sorted(data, key = lambda el: el[2])


    #print data

    for letter in sorted_data:

        #print letter[-1]
        #print letter[-2]

        heroes[ letter[0] ] = 1
        heroes[ letter[1] ] = 1

        #print letter
    #print data
    return data


def sent(sender, recipient):

    data = inbox()
    snt = filter(lambda x: x[0]  == sender and x[1] == recipient, data)
    return len(snt)

def received(sender, recipient):

    data = inbox()
    snt = filter(lambda x: x[0]  == recipient and x[1] == sender, data)
    return len(snt)

def threads():

    threads = {}
    data = list(inbox())

    for letter in data:

        #db.query("""SELECT fromaddr, toaddr, TIMESTAMP(datetime), is_question, msgid, replyto_msgid FROM message""")
        (fromaddr, toaddr, when, is_question, msgid, replyto_msgid) = letter

        if not replyto_msgid:
            #print letter
            threads[msgid] = []
            threads[msgid].append(letter)

        elif replyto_msgid in threads:

            if msgid in threads:
                raise "Msgid exists!!!11"

            threads[replyto_msgid].append(letter)
            threads[msgid] = threads[replyto_msgid]
            del threads[replyto_msgid]
        else:

            print "Smth. weird!\n"
            print letter

            threads[msgid] = []
            threads[msgid].append(letter)

    return threads

def reply_mean():
    return 0


if (__name__ == "__main__"):

    #inbox()

    #print len(threads())
    #print sent('nyddle@funtastiq.ru', 'eugenebolotin@gmail.com')
    #print received('nyddle@funtastiq.ru', 'eugenebolotin@gmail.com')


    all_data = inbox()
    #print all_data
    for datum in all_data:
        print datum


"""
for row in data:

    print row
    (fromaddr, to, time, smth, msgid, replyto_msgid) = row
    print fromaddr

    all[msgid] = row

    print time

    #print time.strptime(time)
    #timestamp = timegm( time.strptime( datetime(time), "%b %d %H:%M:%S %Z %Y" ) )
    #print datetime(2014, 5, 3, 18, 57, 13)
"""



"""
    datestr = " ".join( msg.get( "subject", "" ).split()[ -5: ] )
    timestamp = timegm( time.strptime( datestr, "%b %d %H:%M:%S %Z %Y" ) )
    dt = datetime.fromtimestamp( timestamp )
"""



