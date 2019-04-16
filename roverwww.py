#!/usr/bin/python3
import os
import rovercom
from flask import Flask, request, send_file
app = Flask(__name__)

thisfilepath = os.path.dirname(__file__)

@app.route('/')
def wwwroot():
    hs = ''
    hs += '<html><body>'
    hs += '<h2>Rover.ai</h2>'
    hs += '<img src="/stream?action=stream">'
    hs += '</body></html>'
    return hs

@app.route('/sendcommand')
def wwwsendcommand():
    cmd = request.args.get('cmd')
    rovercom.sendcommand(cmd)
    return cmd

#needs to be at end of file:
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8088, threaded=True)
