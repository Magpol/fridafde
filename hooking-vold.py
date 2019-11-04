#!/usr/bin/env python

import frida
import sys
import time
import os


procname = "vold"

voldScript = """
var startTime = Date.now();
var currentApplication = "vold";
var targetFunction = "footer_put";

var baseAddr = Module.findBaseAddress(currentApplication);
var processAddr = Module.findExportByName(currentApplication, targetFunction); 

send(":: Intercepting - "+ currentApplication +" @ "+ baseAddr +"::");
send(":: Replacing function - "+ targetFunction +" @ "+ processAddr +"::");

Interceptor.replace(processAddr,  new NativeCallback(function() {send(":: " + Date(startTime).toString() + " - Replacing :: VOLD :: put_footer -")}, 'void', []));
"""

print(":: Starting..")
print(":: Attaching to process:" + procname)

def print_result(message):
            print(":: Running %s" %(message))

def on_message(message, data):
            print_result(message['payload'])

device = frida.get_usb_device()
session = device.attach(procname) 

script = session.create_script(voldScript)

script.on('message', on_message)
script.load()
sys.stdin.read()
