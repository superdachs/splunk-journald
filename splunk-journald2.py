#!/usr/bin/env python3

from threading import Thread
from flask import Flask
import daemonize
from time import sleep
import json
import sys
import os
from systemd import journal

class FlaskDaemon:

    def __init__(self, listen='0.0.0.0', port=5000):
        self.data = ["Hallo Welt", "Feld 2"]
        self.listen = listen
        self.port = port
        self.journal_reader = journal.Reader()

    def main(self):

        app = Flask(__name__)
        app.debug = False
        app.use_reloader=False

        @app.route("/last")
        def get_last_data():
            self.journal_reader.get_previous()
            data = []
            while self.journal_reader.get_next():
                for element in self.journal_reader:
                    for k in element:
                        try:
                            element[k] = str(element[k])
                        except:
                            element.pop[k]
                    data.append(element)
            return(json.dumps(data))

        Thread(target=app.run, kwargs={'host': self.listen, 'port': self.port}).start()

        self.loop()

    def loop(self):
        i = 0
        while True:

            self.data.append(i)
            i += 1
            sleep(1)

if __name__ == "__main__":

    def start():
        daemonize.Daemonize(app="flaskdaemon", pid="/tmp/flaskdaemon.pid", action=FlaskDaemon().main).start()

    def stop():
        if not os.path.exists("/tmp/flaskdaemon.pid"):
            sys.exit(0)
        with open("/tmp/flaskdaemon.pid", "r") as pidfile:
            pid = pidfile.read()
        os.system('kill -9 %s' % pid)

    def foreground():
        FlaskDaemon().main()

    def usage():
        print("usage: start|stop|restart|foreground")
        sys.exit(1)

    if not sys.argv[1]:
        usage()

    if sys.argv[1] == "start":
        start()
    elif sys.argv[1] == "stop":
        stop()
    elif sys.argv[1] == "restart":
        stop()
        start()
    elif sys.argv[1] == "foreground":
        foreground()
    else:
        sys.exit(1)