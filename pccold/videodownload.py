import re
import os
import logging
from .config import conf

room_obj_list=[]

from .tools import read,saveStream,ReturnCodeObserverThread,SleepKillerThread
from .bypyrm import doBypy

isinit=False

def getRoomObjList():
    global room_obj_list
    global isinit
    global conf
    files=os.listdir(conf.download_path)
    if isinit:
        return room_obj_list
    logging.info('init room obj list')
    md=read(conf.videolist_path)
    lines=md.split('\n')
    for l in lines:
        match=re.match(r'\[(.*)\]\((.*)\)',l)
        if l and match:
            room_obj={'file_name':match.group(1)+'.mp4','url':match.group(2)}
            if room_obj.get('file_name','') in files:
                logging.info(room_obj.get('file_name','')+' is exist')
            else:
                room_obj_list.append(room_obj)
    isinit=True
    return room_obj_list
    

def downloadVideo():
    global conf
    print('videodownload main')
    room_obj_list=getRoomObjList()
    if len(room_obj_list)>0:
        room_obj=room_obj_list.pop()
        saveStream('source',room_obj.get('file_name','default.mp4'),url=room_obj.get('url',''))
    elif conf.is_bypy:
        doBypy()

ReturnCodeObserverThread.main=downloadVideo
SleepKillerThread.main=downloadVideo


if __name__ == '__main__':
    downloadVideo()
