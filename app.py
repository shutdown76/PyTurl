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


from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import flash
import lib

app = Flask(__name__)
app.secret_key = 'plop'

@app.route('/')
def index(msg=None):
    if msg:
        flash(msg, 'erreur')
    return render_template('index.html', title="PyTurl: Home")


@app.route('/<key>')
def redirection(key):
    """ P """
    #On cherche la clé dans la db

    i = lib.pyTurl()
    url = i.readentry(key)

    if url:
        return redirect(url[0][0])
    else:
        return index(msg=u"L'url demandé n'existe pas!")


@app.route('/submit', methods=['POST'])
def submit():
    url = request.form['url']

    i = lib.pyTurl()
    key = i.keygen(8)
    i.addentry(key,url)

    q = lib.pyTurl()
    fqr = q.qrgen(url)
    
    d = lib.pyTurl()
    qr = d.getqr(fqr)

    return render_template('submit.html', title="PyTurl: Record", url=url, key=request.url_root+key, qr=qr)

@app.route('/about')
def about():
    return render_template('about.html', title="PyTurl: About")

@app.route('/contact')
def contact():
    return render_template('contact.html', title="PyTurl: Contact")

if __name__ == '__main__':
    app.run(debug=True)

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79
