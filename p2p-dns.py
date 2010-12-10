#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import readline
import sys
from optparse import OptionParser
import threading
import os
import re
from config import *
from server import *
from database import *

class App(object):
    def __init__(self):
        self.parser = OptionParser(version="%prog 0.1")

    def parse_commandline(self):

        self.parser.add_option("-d",
                          "--daemon",
                          action="store_true",
                          dest="daemon_mode",
                          default=False,
                          help="Starts this server in daemon mode" )

        (options, args) = self.parser.parse_args()

        if options.daemon_mode:
            print("in daemon mode")
            os.spawnl(os.P_NOWAIT, "touch", "touch", "./daemon")
            return True
        return False

    def print_help(self):
        commands = {
            "help":     "print this help",
            "daemon":   "detaches the server and exits this process",
            "connect":  "connect to another node",
            "nodes":    "print all known nodes",
            "domains":  "print all known domains",
            "register": "register a domain with all known nodes",
            "quit":     "exit this process"
            }
        self.parser.print_help()
        print("\n\tCLI commands:")
        for (command, explanaiton) in sorted( commands.items() ):
            print( "%-10s %s" % (command, explanaiton) )

    def start_daemon(self):
        proc_id = os.spawnl(os.P_NOWAIT, sys.executable + " " + sys.argv[0], "-d")
        print("process id: %s" % proc_id)
        self.quit()

    def start_server(self):
        self.db = Database()
        self.srv = Server(db)
        self.srv.start()

    def stop(self):
        self.srv.stop()
        self.srv.join()
        sys.exit()

    def run(self):
        daemon_mode = self.parse_commandline()
        self.start_server()
        if not daemon_mode:
            print( """Welcome to this p2p-dns client.
    To run in daemon mode, use '-d' to start or type 'daemon'.
    To find out what other commands exist, type 'help'""" )

            while True:
                try:
                    io = raw_input("~> ")
                    if io == "help":
                        self.print_help()
                    elif io == "daemon":
                        self.start_daemon()
                    elif io == "connect":
                        server = raw_input("server:")
                        port = raw_input("port[%s]:" % default_port)

                        try:
                            port = int(port)
                        except:
                            port = default_port
                        
                        self.srv.add_node(server, port)
                    elif io == "nodes":
                        self.db.print_nodes()
                    elif io == "quit":
                        self.stop()
                    else:
                        print("Didn't recognize command. Please retry or type 'help'")
                except EOFError:
                    self.stop()
            
if __name__ == "__main__":
    app = App()
    app.run()
