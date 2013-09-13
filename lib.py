#/bin/env python
# -*- coding: utf-8 -*-


#          DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                   Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#          DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
# 0. You just DO WHAT THE FUCK YOU WANT TO.


import random
import string
import sqlite3
import qrcode
import base64

class pyTurl():
    """ Class dédier à pyTurl """

    def keygen(self, length):
        """Generateur de clé """

        dico = string.printable[:62]
        key = ''.join([dico[random.randrange(0, len(dico))] for loop in range(length)])
            
        print self.readentry(key)

        #while True:
            #if key in self.readentry(key):
                #key = self.keygen(8)
            #else:
                #break

        return key


    def dbinit(self):
        """ Initialiser la DB si elle n'existe pas """
        db = sqlite3.connect('pyTurl.db')
        db.row_factory = sqlite3.Row
        c = db.cursor()
        c.execute(""" 
            CREATE TABLE pyturl(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key varchar(8),
            url varchar(255)
            );
                  """)
        db.commit()
        c.close()


    def dbcon(self, query, *args):
        """ Connexion à la DB """
        try:
            with open('pyTurl.db'): pass
        except IOError:
            self.dbinit()

        db = sqlite3.connect('pyTurl.db')
        db.row_factory = sqlite3.Row
        c = db.cursor()
        c.execute(query, args)
        db.commit()
        r = []
        for i in c:
            r.append(i)
        c.close()
        db.close()

        return r



    def addentry(self, key, url):
        """ Ajout une nouvelle entré à la DB"""
        self.dbcon("INSERT INTO pyturl (key, url) VALUES (?, ?);", key, url)


    def readentry(self, key):
        """ Lis une entré en DB"""
        r = self.dbcon("SELECT url FROM pyturl where key=?;", key)
        return r


    def qrgen(self, url):
        """Generation du qrcode pour l'url"""
        qrc = qrcode.make(url, version = 5, error_correction = qrcode.constants.ERROR_CORRECT_H)
        file_name = self.keygen(12)
        qrc.save('tmp/' + file_name + '.png')

        return file_name

    def getqr(self, name):
        """Renvoi le qrcode en base64"""
        img = open('tmp/'+name+'.png')
        data = base64.encodestring(img.read())

        return data







# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79
