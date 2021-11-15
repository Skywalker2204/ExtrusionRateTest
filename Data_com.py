#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 01:04:02 2021

@author: lukashentschel
"""

class DataMaster():
    def __init__(self):
        
        self.startStream = b"M155 S1\r\n"
        self.msg =['']
        self.dataDict = {'temperature' : ['--']}
        self.RowMsg = ''
        
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
            
