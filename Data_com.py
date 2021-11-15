#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 01:04:02 2021

@author: lukashentschel
"""

class DataMaster():
    def __init__(self):
        self.startStream = b"M155 S1\r\n"
        self.msg =[]
        self.data = {'temperature' : ['--']}
        
    def DecodeMsg(self):
        temp = self.RowMsg
        if len(temp) > 0:
            if temp.stratswith('T'):
                self.data['temperature'].append(temp)
            else:
                self.msg.append(temp)
        return self.msg[-1]
            