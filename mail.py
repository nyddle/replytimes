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

from statistics import median

from filters import filter_address, filter_letters


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

        self.domains = domains

        self.mailboxes = defaultdict(int)
        self.sentfrom = defaultdict(int)
        self.received = defaultdict(int)
        self.receivedfrom = defaultdict(int)
        self.totalletters = 0
        self.totalsent = 0
        self.totalreceived = 0

        db = self.getdb()
        db.query("""SELECT fromaddr, toaddr, TIMESTAMP(datetime), is_question, msgid, replyto_msgid FROM message""")
        r=db.store_result()
        self.data = r.fetch_row(1000000)

        self.filter_data()

        for letter in self.data:
            #db.query("""SELECT fromaddr, toaddr, TIMESTAMP(datetime), is_question, msgid, replyto_msgid FROM message""")
            (fromaddr, toaddr, when, is_question, msgid, replyto_msgid) = letter
            self.sentfrom[fromaddr] += 1
            self.received[toaddr] += 1
            self.totalletters += 1

            if self.is_local(fromaddr):
                print fromaddr

    def filter_data(self):

        tmp_data = []

        return self.data

    def __repr__(self):
        return "Total letters: %s\n" % (self.totalletters) + \
               "Sent letters: %s\n" % (self.totalsent) + \
               "Received letters: %s\n" % (self.totalreceived)

    def is_local(self, addr):
        #(name, domain, junk) = addr.split('@')
        domain = None
        try:
            if addr.index('@'):
                name, domain  = addr.split('@')
        except:
            pass
            #print "ERRORR!!!" + addr

        for d in self.domains:
            if domain == d:
                return 1
        return 0

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
        sorted_data = sorted(data, key = lambda el: el[2])


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

    #mailbox = Mailbox(['tellur.com.ua'], filters=['inbound'])
    mailbox = Mailbox()
    print mailbox


#
