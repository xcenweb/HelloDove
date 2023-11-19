import sounddevice
import re
import sherpa_ncnn
import sys

def create_recognizer():
    """
    创建语音识别实例
    """
    model_dir = 'model'
    recognizer = sherpa_ncnn.Recognizer(
        tokens=sys.path[0]+"/"+model_dir+"/tokens.txt",
        encoder_param=sys.path[0]+"/"+model_dir+"/encoder_jit_trace-pnnx.ncnn.param",
        encoder_bin=sys.path[0]+"/"+model_dir+"/encoder_jit_trace-pnnx.ncnn.bin",
        decoder_param=sys.path[0]+"/"+model_dir+"/decoder_jit_trace-pnnx.ncnn.param",
        decoder_bin=sys.path[0]+"/"+model_dir+"/decoder_jit_trace-pnnx.ncnn.bin",
        joiner_param=sys.path[0]+"/"+model_dir+"/joiner_jit_trace-pnnx.ncnn.param",
        joiner_bin=sys.path[0]+"/"+model_dir+"/joiner_jit_trace-pnnx.ncnn.bin",
        num_threads=4,
    )
    return recognizer

def audio_capture(queue, sample_rate, duration):
    """
    抓取麦克风声音
    """
    samples_per_read = int(duration * sample_rate)
    with sounddevice.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
        while True:
            samples, _ = s.read(samples_per_read)
            samples = samples.reshape(-1)
            queue.put(samples)

def dict2str(recognizer_dict, this_time, period=2):
    """
    将一个 period(秒) 内的指令字典汇总成一段文字，并将过时内容删去
    """
    str_list = []
    new_dict = {}
    for timestamp,recognizers in recognizer_dict.items():
        if this_time-timestamp <= period:
            new_dict[timestamp] = recognizers
            for value in recognizers:
                str_list.append(value)
    return ''.join(str_list), new_dict


def wakeup_word(word):
    """
    唤醒词验证
    """
    if re.search(r'你好多维|你好多为|你好多喂', word):
        return True
    else:
        return False