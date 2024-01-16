# 语音输出
import pyttsx3
import random
import pygame

engine = pyttsx3.init()  # 初始化pyttsx3引擎

def speak(text=''):
    """
    根据文本输出语音
    """
    # print('[', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), ']', text)
    print('【Dove】:', text)
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 180)  # 语速
    engine.setProperty('volume', 1)  # 声音大小
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()

def wakeup_callback():
    """
    唤醒后语音
    """
    text = ['我在，请说', '您好，请说', '主人，有什么吩咐？']
    text = text[random.randint(0, len(text)-1)]

    music('source/music/wakeup.mp3')
    speak(text)

    return text

def sleep_callback():
    """
    关闭唤醒后语音
    """
    music('source/music/sleep.mp3')
    return

def music(path):
    """
    播放音乐
    """
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
       pygame.time.Clock().tick(10)
    
    return