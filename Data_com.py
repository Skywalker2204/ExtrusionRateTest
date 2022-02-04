#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 01:04:02 2021

@author: lukashentschel
"""
DEBUG = True
if not DEBUG:
    from hx711 import HX711
    import RPi.GPIO as GPIO

class DataMaster():
    def __init__(self):
        
        self.dataDict = {'temperature' : [[0.0, 0.0]],
                         'force' : [[0.0, 0.0]]}
        self.RowMsgPrinter = ''
        self.RowMsgScale = ''
        
        self.referenceUnit=92
        self.scaleInit = False
        self.PINS = [5,6] #DT und SCK in GIPO PIN
        
    def DecodeMsgPrinter(self, time):
        temp = self.RowMsgPrinter
        msg = ''
        if len(temp) > 0:
            if temp.startswith(' T:') or temp.startswith('ok T:'):
                T = temp.split(':')[1].split(r'/')[0]
                self.dataDict['temperature'].append([time, T])
                print(T)
            else:
                msg = temp
        return msg
    
    def DecodeMsgScale(self, time):
        temp = self.RowMsgScale
        msg = ''
        if len(temp) > 0:
            print(temp)
            if temp.startswith(' T:') or temp.startswith('ok T:'):
                T = temp.split(':')[1].split(r'/')[0]
                self.dataDict['temperature'].append([time, T])
                print(T)
            else:
                msg = temp
        return msg
    
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
    
    def runScale(self, time):
        try:
            value = self.hx.get_weight(self.PINS[0])
            self.dataDict['force'].append([time, value])
            print(value)
        except Exception as e:
            print(f"Scale Error: {e}")

    def cleanAndExit(self):
        if not DEBUG:
            GPIO.cleanup()
        print('GPIO cleanup performed')
        
        
        
            
