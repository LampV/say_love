#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author: Jiawei Wu
@create time: 2022-01-03 23:46
@edit time: 2022-01-06 21:26
@file: /say_love/baidu_speech.py
@desc: 
"""
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus
import json
API_KEY = ""
SECRET_KEY = ""


TTS_URL = 'http://tsn.baidu.com/text2audio'

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'


def fetch_token():
    """获取token"""
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    result_str = result_str.decode()

    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'audio_tts_post' in result['scope'].split(' '):
            print('please ensure has check the tts ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


def tts_and_save(text, filename="resources/save.wav", **kwargs):
    token = fetch_token()

    tex = quote_plus(text)  # 此处TEXT需要两次urlencode

    params = {'tok': token, 'tex': tex, 'cuid': "quickstart",
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数
    params.update(kwargs)

    data = urlencode(params)

    req = Request(TTS_URL, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()

        headers = dict((name.lower(), value)
                       for name, value in f.headers.items())

        has_error = ('content-type' not in headers.keys()
                     or headers['content-type'].find('audio/') < 0)
    except URLError as err:
        print('http response http code : ' + str(err.code))
        result_str = err.read()
        has_error = True

    save_file = "error.txt" if has_error else filename

    with open(save_file, 'wb') as of:
        of.write(result_str)

    if has_error:
        result_str = str(result_str, 'utf-8')
        print("tts api  error:" + result_str)

    print("file saved as : " + save_file)


def play_sound(filename):
    import sounddevice as sd
    import soundfile as sf
    data, fs = sf.read(FNAME, dtype='float32')
    sd.play(data, fs, device=1)
    status = sd.wait()
    
def loop():
    # 大姚的订单信息内容文本
    # TEXT = "Hello荔荔，这个是我用百度在线版合成的语音，试试别的音色"
    while True:
        text = input("输入文本\n")
        # FNAME = "resources/test-5118.wav"
        FNAME = "resources/tmp.wav"
        tts_and_save(text, FNAME, aue=6)
        play_sound(FNAME)
    
if __name__ == '__main__':
    TEXT = "你好，这里是为荔荔编写的智能小黄鸭"

    FNAME = "resources/demo.wav"
    tts_and_save(TEXT, FNAME, aue=6, per=5118, spd=5) 