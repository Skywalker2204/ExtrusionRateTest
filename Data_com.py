#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 01:04:02 2021

@author: lukashentschel
"""

from hx711 import HX711
import RPi.GPIO as GPIO

class DataMaster():
    def __init__(self):
        
        self.startStream = b"M155 S1\r\n"
        self.msg =['']
        self.dataDict = {'temperature' : ['--']}
        self.RowMsg = ''
        
        self.referenceUnit=92
        self.scaleInit = False
        self.PINS = [5,6] #DT und SCK in GIPO PIN
        
    def DecodeMsg(self):
        temp = self.RowMsg
        if len(temp) > 0:
            if temp.startswith(' T:') or temp.startswith('ok T:'):
                print(temp, 'bin da')
                T = temp.split(':')[1].split(r'/')[0]
                self.dataDict['temperature'].append(T)
                print(T)
            else:
                self.msg.append(temp)
        return temp
    
    def initScale(self):
        if not self.scaleInit:
            self.hx = HX711(self.PINS[0], self.PINS[1])
            self.hx.set_reading_format("MSB", "MSB")
            self.hx.set_reference_unit(self.referenceUnit)
            self.hx.reset()
            self.hx.tare()
            self.scaleInit = True
        pass
    
    def setReferenceValue(self, value):
        self.referenceUnit=value
        self.hx.set_reference_unit(self.referenceUnit)
        pass
    
    def runScale(self):
        try:
            value = self.hx.get_weight(self.PINS[0])
            self.dataDict['Force'].append(value)
            print(value)
        except Exception as e:
            print("Scale Error: "+e)
        
            
