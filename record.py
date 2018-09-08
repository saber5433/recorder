#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,shutil
import sys,threading
import numpy as np
from pyaudio import PyAudio, paInt16
from datetime import datetime
#from pydub import AudioSegment
import wave
import pylab
import time
from tkinter import *

# define of params
NUM_SAMPLES = 2000
framerate = 44100
channels = 2
sampwidth = 2

finish = 1
flag = 0
wavname = ''


def playerThread():
    global finish
    global flag
    if finish == 1 and flag == 0:
        flag = 1
        t = threading.Thread(target=player_wave, args=())
        t.setDaemon(True)
        t.start()

    else:
        flag = 0
        finish = 0
        return 0


def player_wave():
    global wavname
    global finish
    global flag
    path = r".\\audio\\"+wavname
    if finish == 1 and wavname != '' and os.path.exists(path):
        # open a wav format music
        f = wave.open(path, "rb")
        # instantiate PyAudio
        p = PyAudio()
        # open stream
        stream = p.open(format=paInt16, channels=2,
                        rate=framerate,
                        output=True)
        # read data
        data = f.readframes(NUM_SAMPLES)
        # paly stream
        print("播放中...")
        while len(data) and finish == 1:
            stream.write(data)
            data = f.readframes(NUM_SAMPLES)
            # stop stream
        print("播放结束")
        if finish == 0:
            finish = 1
        flag = 0
        stream.stop_stream()
        stream.close()
        # close PyAudio
        p.terminate()
    else:
        flag = 0
        finish = 1
        print("请先录音 !")
        return 0 


def upload_wave():
    global wavname
    path = r".\\audio\\" + wavname
    if os.path.exists(path) and wavname != '':
        newpath = r'.\\' + wavname
        shutil.move(path,newpath)
        print("Move File to" + newpath)
        wavname = ''
        return 0
    else:
        print("请先录音 !" )
        return 0 


def delete_wave():
    global wavname
    if wavname != '':
        path = r".\\audio\\"
        files = os.listdir(path)
        for name in files:
            if name == wavname:
                os.remove(path+name)
                print("Delete File: " + path + wavname)
                wavname = ''
                return 0
            
        print("no such file !:" + path + wavname)
        return 0
    else:
        print("请先录音 !" )
        return 0 


def recordThread():
    global finish
    global flag
    if finish == 1 and flag == 0:
        t = threading.Thread(target=record_wave, args=())
        t.setDaemon(True)
        t.start()
        flag = 1
    else:
        flag = 0
        finish = 0
        return 0
    
        
def record_wave():
    global finish
    global wavname
    # open the input of wave
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=2,
                     rate=framerate, input=True,
                     frames_per_buffer=NUM_SAMPLES)
    filename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav"
    wavname = filename
    path = ".\\audio\\"+filename
    wf = wave.open(path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    print("录制中...")
    while finish == 1:
        # read NUM_SAMPLES sampling data
        string_audio_data = stream.read(NUM_SAMPLES)
        wf.writeframes(string_audio_data)
        
    stream.stop_stream()
    stream.close()
    wf.close()
    
    print("录制结束")
    finish = 1

    pa.terminate()
    print (filename, "saved")


def record_button(root, label_text, button_text, button_func):
    '''function of creat label and button'''
    # label details
    label = Label(root)
    label['text'] = label_text
    label.pack()
    # label details
    button = Button(root)
    button['text'] = button_text
    button['command'] = button_func
    button.pack()


def player_button(root, button_text, button_func):
    '''function of creat label and button'''
    button = Button(root)
    button['text'] = button_text
    button['command'] = button_func
    button.pack()


def delete_button(root, button_text, button_func):
    '''function of creat label and button'''
    button = Button(root)
    button['text'] = button_text
    button['command'] = button_func
    button.pack()


def upload_button(root, button_text, button_func):
    '''function of creat label and button'''
    button = Button(root)
    button['text'] = button_text
    button['command'] = button_func
    button.pack()


def main():
    root = Tk()
    record_button(root, "录音程序", "录音", recordThread)
    player_button(root, "播放", playerThread)
    upload_button(root, "上传", upload_wave)
    delete_button(root, "删除", delete_wave)
    root.mainloop()


if __name__ == "__main__":
    main()
