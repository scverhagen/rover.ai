#!/usr/bin/python3
import os
import rovercom
from flask import Flask, request, send_file
app = Flask(__name__)

thisfilepath = os.path.dirname(__file__)

status = rovercom.status_fifo()

start_html = '<html><head><script src="https://code.jquery.com/jquery-3.3.1.min.js" crossorigin="anonymous"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script><script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script></head><body>'

@app.route('/')
def wwwroot():
    hs = start_html
#    hs += """
#    <script>
#    function getPositions(ev) {
#    if (ev == null) { ev = window.event }
#        _mouseX = ev.clientX;
#        _mouseY = ev.clientY;
#        alert(_mouseY);
#    }
#    </script>
#    """
    hs += '<h2>Rover.ai</h2>'
    hs += '<img src="/stream?action=stream" onMouseMove="getPositions();>'
    hs += '<hr>'
    hs += '<div id="status">Loading...</div>'
    hs += '<script>'
    hs += 'function updateStatus() {'
    hs += '$.ajax({\n'
    hs += 'url : "/getstatus",\n'
    hs += 'success : function(result){\n'
    hs += 'document.getElementById("status").innerHTML = result;\n'
    hs += '}\n'
    hs += '});\n'
    hs += '}\n'
    hs += 'setInterval(updateStatus, 250);\n'
    hs += '</script>'
    hs += '</body></html>'
    return hs

@app.route('/sendcommand')
def wwwsendcommand():
    cmd = request.args.get('cmd')
    rovercom.sendcommand(cmd)
    return cmd

@app.route('/getstatus')
def wwwgetstatus():
    return status.getstatus()
    
#needs to be at end of file:
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8088, threaded=True)

