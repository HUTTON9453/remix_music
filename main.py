# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 01:06:46 2020

@author: hutton
"""

import time
import pygame
# The below imports are required by the patch
import json
import os
from urllib.parse import parse_qs, parse_qsl, unquote
import numpy as np
from moviepy.editor import *
# This function is based off on the changes made in
# https://github.com/nficano/pytube/pull/643

def apply_descrambler(stream_data, key):
    """Apply various in-place transforms to YouTube's media stream data.
    Creates a ``list`` of dictionaries by string splitting on commas, then
    taking each list item, parsing it as a query string, converting it to a
    ``dict`` and unquoting the value.
    :param dict stream_data:
        Dictionary containing query string encoded values.
    :param str key:
        Name of the key in dictionary.
    **Example**:
    >>> d = {'foo': 'bar=1&var=test,em=5&t=url%20encoded'}
    >>> apply_descrambler(d, 'foo')
    >>> print(d)
    {'foo': [{'bar': '1', 'var': 'test'}, {'em': '5', 't': 'url encoded'}]}
    """
    otf_type = "FORMAT_STREAM_TYPE_OTF"

    if key == "url_encoded_fmt_stream_map" and not stream_data.get(
        "url_encoded_fmt_stream_map"
    ):
        formats = json.loads(stream_data["player_response"])["streamingData"]["formats"]
        formats.extend(
            json.loads(stream_data["player_response"])["streamingData"][
                "adaptiveFormats"
            ]
        )
        try:
            stream_data[key] = [
                {
                    "url": format_item["url"],
                    "type": format_item["mimeType"],
                    "quality": format_item["quality"],
                    "itag": format_item["itag"],
                    "bitrate": format_item.get("bitrate"),
                    "is_otf": (format_item.get("type") == otf_type),
                }
                for format_item in formats
            ]
        except KeyError:
            cipher_url = []
            for data in formats:
                cipher = data.get("cipher") or data["signatureCipher"]
                cipher_url.append(parse_qs(cipher))
            stream_data[key] = [
                {
                    "url": cipher_url[i]["url"][0],
                    "s": cipher_url[i]["s"][0],
                    "type": format_item["mimeType"],
                    "quality": format_item["quality"],
                    "itag": format_item["itag"],
                    "bitrate": format_item.get("bitrate"),
                    "is_otf": (format_item.get("type") == otf_type),
                }
                for i, format_item in enumerate(formats)
            ]
    else:
        stream_data[key] = [
            {k: unquote(v) for k, v in parse_qsl(i)}
            for i in stream_data[key].split(",")
        ]


import pytube
pytube.__main__.apply_descrambler = apply_descrambler

name_setting = []
i=0
with open('list.txt') as file:
    for line in file:
        print(line)
        yt = pytube.YouTube(line.rstrip())
        name_setting.append(yt.title)
        yt.streams.first().download('./youtube/mp4', filename=str(i))
        video = VideoFileClip(os.path.join('./youtube/mp4/'+str(i) + ".mp4"))
        video.audio.write_audiofile(os.path.join('./youtube/wav/'+str(i) + ".wav"))
        video.reader.close()
        video.audio.reader.close_proc()
        i+=1


name_setting_arr = np.array(name_setting)
np.save('ans',name_setting_arr)

name_setting_arr = np.load('ans.npy')
for j,name in enumerate(name_setting_arr):
    print(j+1,name)
#print(name_setting_arr)

i=0
queue = []
volume = []
pygame.init()

DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Memes.')

pygame.mixer.init()

for root, dir, files in os.walk("youtube/wav/"):
    for file in files:
        queue.append(pygame.mixer.Sound(os.path.join('youtube/wav/'+str(i)+'.wav')))
        volume.append(1.0)
        i+=1
time.sleep(20)
print("播放音樂1")
for j in range(i):
    pygame.mixer.Channel(j).play(queue[j])
#pygame.mixer.music.play()


    
while True: # Main Loop

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.unicode == ' ':
                pygame.quit()
                sys.exit()
            if event.unicode == 'z':
                for j in range(i):
                    pygame.mixer.Channel(j).pause()
            if event.unicode == 'x':
                for j in range(i):
                    pygame.mixer.Channel(j).unpause()
            if event.unicode == 'c':
                for j in range(i):
                    pygame.mixer.Channel(j).play(queue[j])
            if event.unicode == 'v':
                for j in range(i):
                    pygame.mixer.Channel(j).stop()
            if event.unicode == '1':
                volume[0]+=0.1
                print('0: '+str(volume[0]))
                pygame.mixer.Channel(0).set_volume(volume[0])
            if event.unicode == 'q':
                volume[0]-=0.1
                print('0: '+str(volume[0]))
                pygame.mixer.Channel(0).set_volume(volume[0])
            if event.unicode == 'a':
                pygame.mixer.Channel(0).stop()
            if event.unicode == '2':
                volume[1]+=0.1
                print('1: '+str(volume[1]))
                pygame.mixer.Channel(1).set_volume(volume[1])
            if event.unicode == 'w':
                volume[1]-=0.1
                print('1: '+str(volume[1]))
                pygame.mixer.Channel(1).set_volume(volume[1])
            if event.unicode == 's':
                pygame.mixer.Channel(1).stop()
            if event.unicode == '3':
                volume[2]+=0.1
                print('2: '+str(volume[2]))
                pygame.mixer.Channel(2).set_volume(volume[2])
            if event.unicode == 'e':
                volume[2]-=0.1
                print('2: '+str(volume[2]))
                pygame.mixer.Channel(2).set_volume(volume[2])
            if event.unicode == 'd':
                pygame.mixer.Channel(2).stop()
            if event.unicode == '4':
                volume[3]+=0.1
                print('3: '+str(volume[3]))
                pygame.mixer.Channel(3).set_volume(volume[3])
            if event.unicode == 'r':
                volume[3]-=0.1
                print('3: '+str(volume[3]))
                pygame.mixer.Channel(3).set_volume(volume[3])
            if event.unicode == 'f':
                pygame.mixer.Channel(3).stop()
            if event.unicode == '5':
                volume[4]+=0.1
                print('4: '+str(volume[4]))
                pygame.mixer.Channel(4).set_volume(volume[4])
            if event.unicode == 't':
                volume[4]-=0.1
                print('4: '+str(volume[4]))
                pygame.mixer.Channel(4).set_volume(volume[4])
            if event.unicode == 'g':
                pygame.mixer.Channel(4).stop()
            if event.unicode == '6':
                volume[5]+=0.1
                print('5: '+str(volume[5]))
                pygame.mixer.Channel(5).set_volume(volume[5])
            if event.unicode == 'y':
                volume[5]-=0.1
                print('5: '+str(volume[5]))
                pygame.mixer.Channel(5).set_volume(volume[5])
            if event.unicode == 'h':
                pygame.mixer.Channel(5).stop()
            if event.unicode == '7':
                volume[6]+=0.1
                print('6: '+str(volume[6]))
                pygame.mixer.Channel(6).set_volume(volume[6])
            if event.unicode == 'u':
                volume[6]-=0.1
                print('6: '+str(volume[6]))
                pygame.mixer.Channel(6).set_volume(volume[6])
            if event.unicode == 'j':
                pygame.mixer.Channel(6).stop()
            if event.unicode == '8':
                volume[7]+=0.1
                print('7: '+str(volume[7]))
                pygame.mixer.Channel(7).set_volume(volume[7])
            if event.unicode == 'i':
                volume[7]-=0.1
                print('7: '+str(volume[7]))
                pygame.mixer.Channel(7).set_volume(volume[7])
            if event.unicode == 'k':
                pygame.mixer.Channel(7).stop()
            
    pygame.display.update()
'''
說愛你
帶我走
愛你
我們的愛
心牆
後來
piano man
'''
