# 处理各类语音指令
import re
import subprocess
import util.voice as voice

def unpack(commond):
    """
    从文本信息分析操作信息
    """

    # 浏览器搜索
    if re.search(r'^打开浏览器', commond):
        subprocess.Popen(r'C:\\Program Files (x86)\\Microsoft\\Edge\Application\\msedge.exe')
        voice.speak('已经帮主人打开浏览器啦')
        return True

    voice.speak('主人，这个我不会')
    return False