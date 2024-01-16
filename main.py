import time
import queue
import threading

from util import voice
from util import listen
from util import processor

# 启动
recognizer = listen.create_recognizer()
sample_rate = recognizer.sample_rate
duration = 0.8
audio_queue = queue.Queue()
audio_thread = threading.Thread(target=listen.audio_capture, args=(audio_queue, sample_rate, duration))
audio_thread.start()

# 初始化变量
wakeup_status = False
wakeup_time = 0
callback_ststus = False
callback_time = 0
recognizer_dict = {}
commond_list = []

while True:
    if not audio_queue.empty():
        
        ### 初始化识别 ###
        samples = audio_queue.get()
        recognizer.accept_waveform(sample_rate, samples)
        this_time = round(time.time())
        
        ### 监听 ###
        if len(recognizer.text) != 0 and wakeup_status == False:

            if this_time in recognizer_dict.keys():
                old_list = recognizer_dict[this_time]
                old_list.append(recognizer.text)
                recognizer_dict[this_time] = old_list
            else:
                recognizer_dict[this_time] = [recognizer.text]
                
            commond, recognizer_dict = listen.dict2str(recognizer_dict, this_time)
                
            print('[input]', commond)

            if listen.wakeup_word(commond):
                print('---- 唤醒 ----')
                voice.wakeup_callback()

                wakeup_time = this_time
                wakeup_status = True

            recognizer.reset()
            
        ### 受令 ###
        if wakeup_status and callback_ststus == False:
            if (this_time - wakeup_time) >= 6 or len(recognizer.text) > 20:
                # 6 秒不说话，或字符数量超 20 后直接进入反馈模式
                if commond_list != []:
                    print('接受命令 ->', commond_list)
                    wakeup_status = False
                    callback_ststus = True
                else:
                    wakeup_status = False
                    voice.sleep_callback()
            else:
                if len(recognizer.text) != 0:
                    commond_list.append(recognizer.text)
                    print('受令中 ->', commond_list)
                    wakeup_time = this_time
                    recognizer.reset()
                else:
                    pass

        ### 反馈 ###
        if callback_ststus:

            # voice.speak(''.join(commond_list))
            processor.unpack(''.join(commond_list))
 
            callback_ststus = False
            wakeup_status = False

            commond_list = []
            recognizer.reset()

            print('---- 退出 ----')