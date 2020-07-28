import speech_recognition as sr
import re

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Start talking...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        stt = r.recognize_google(audio, language='zh-TW')
    except sr.UnknownValueError:
        stt = "N/A"
    except sr.RequestError as e:
        stt = "N/A".format(e)

    return stt


def convert_cndigit(xxx):
    cn_num = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    }

    regex = re.compile(r'[一二三四五六七八九123456789]+')
    xxx = regex.search(xxx)
    if xxx:
        xxx = xxx.group()
    else:
        return None
    result = 0
    result_list = []
    for i, d in enumerate(xxx):

        if d in cn_num:
            result += cn_num[d]

    return sum(result_list) + result

def speech():

    text = speech_to_text()
    print(text)

    res = convert_cndigit(text)
    print(res)
