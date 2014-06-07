#! /usr/bin/python

import sys
import re
import imaplib
import pytz
import time
import MySQLdb
from datetime import datetime
from calendar import timegm
from collections import defaultdict

DB_HOST = "95.85.22.116"
DB_USER = "replytimes"
DB_PASSWORD = "1Jx2VLSbi1TPE6rPIW"
DB_BASE = "replytimes"
DB_CHARSET = "utf8"

class Letter():
    """Represents a letter from corporate mailbox."""

    def __init__(self):
        self.letter= {}


class Mailbox():
    """Represents all emails in a corporate mailbox."""

    def __init__(self,domains=[]):

        self.mailboxes = defaultdict(int)
        self.sentfrom = defaultdict(int)
        self.received = defaultdict(int)
        self.receivedfrom = defaultdict(int)
        self.totalletters = 0

        db = self.getdb()
        db.query("""SELECT fromaddr, toaddr, TIMESTAMP(datetime), is_question, msgid, replyto_msgid FROM message""")
        r=db.store_result()
        self.data = r.fetch_row(1000000)

        for letter in self.data:
            #db.query("""SELECT fromaddr, toaddr, TIMESTAMP(datetime), is_question, msgid, replyto_msgid FROM message""")
            (fromaddr, toaddr, when, is_question, msgid, replyto_msgid) = letter
            self.sentfrom[fromaddr] += 1
            self.received[toaddr] += 1
            self.totalletters += 1

    def __repr__(self):
        return "Total letters: %s\n" % (self.totalletters)


    def threads(self):

        threads = {}

        for letter in self.data:

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


    def getdb(self):
        return MySQLdb.connect( host = DB_HOST, user = DB_USER, passwd = DB_PASSWORD, db = DB_BASE, charset = DB_CHARSET, connect_timeout = 10 )

    def inbox(self):
        db = self.getdb()
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


    def sent(self, sender, recipient):

        data = inbox()
        snt = filter(lambda x: x[0]  == sender and x[1] == recipient, data)
        return len(snt)

    def received(self, sender, recipient):

        data = inbox()
        snt = filter(lambda x: x[0]  == recipient and x[1] == sender, data)
        return len(snt)

    def reply_mean(self):
        return 0


if (__name__ == "__main__"):

    mailbox = Mailbox(['tellur.com.ua'])
    print mailbox


