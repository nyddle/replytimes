#! /usr/bin/python

import datetime


#TODO: add EXCLUDE option
def filter_letters(slist, rlist, data):

    res = []
    for letter in data:
        (s, r) = letter[0], letter[1]

        if filter_address(s, slist) and filter_address(r, rlist):
            res.append(letter)

    return res


def filter_address(address, filters):

    addresses = [ l for l in filters if l.find('@') > -1 ]
    regexes = [ l for l in filters if l.find('@') == -1 ]

    if len(filters) == 0:
        return 1

    if address in addresses:
        return 1

    for r in regexes:
        if address.find('@' + r) > -1:
            return 1

    return 0


if (__name__ == "__main__"):


    data = [(u'203641@loveloft.ru.ru', u'killer7087@rambler.ru', datetime.datetime(2014, 6, 20, 8, 26, 20), 0, u'<7174C2919A4E60B36F6A239DC9326F41@geme>', u''), \
    (u'soenko_ud@tellur.dp.ua', u'its@tellur.com.ua', datetime.datetime(2014, 6, 20, 9, 12, 48), 0, u'<CAG2TwjF1TTHEi9w-O4d3g9eNbWOLOZN6R=cbs4AMRvgL28iHrA@mail.gmail.com>', u''), \
    (u'info@1c.ru', u'infomail1c@tellur.dp.ua', datetime.datetime(2014, 6, 20, 10, 16, 58), 0, u'<53a44258.a292700a.4af8.ffffc3a5SMTPIN_ADDED_MISSING@mx.google.com>', u''), \
    (u'info@1c.ru', u'infomail1c@tellur.dp.ua', datetime.datetime(2014, 6, 20, 10, 16, 59), 0, u'<53a44258.a292700a.4af8.ffffc3a5SMTPIN_ADDED_MISSING@mx.google.com>', u''), \
    (u'info@1c.ru', u'infomail1c@tellur.dp.ua', datetime.datetime(2014, 6, 20, 10, 17), 0, u'<53a44258.a292700a.4af8.ffffc3a5SMTPIN_ADDED_MISSING@mx.google.com>', u''), \
    (u'info@1c.ru', u'infomail1c@tellur.dp.ua', datetime.datetime(2014, 6, 20, 10, 16, 58), 0, u'<53a44258.a292700a.4af8.ffffc3a5SMTPIN_ADDED_MISSING@mx.google.com>', u'')]


    #filters = [ 'inbound', 'outbound', recipients_list  ]

    sender = [  ]
    receiver = [ 'infomail1c@tellur.dp.ua', 'tellur.com.ua', 'rambler.ru' ]

    for s in filter_letters(sender, receiver, data):
        print s

    print filter_address('nyddle@gmail.com', [ 'gmail.com' ])

