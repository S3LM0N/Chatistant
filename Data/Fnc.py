
'''
    Aiden Funcion List

    - TTS
    - STT
    - Analysis


'''

# LPD --------------------------------------------------------------------------------------------------
# Loaing Personal Data
import csv
def LPD(Dir):
    File = open(Dir, 'r', encoding='utf-8')

    Ls = csv.reader(File)
    LineCount = 0
    for L in Ls:
        if LineCount == 0 : PersonalData = {'Bookmarks':L}
        if LineCount == 1 : PersonalData['Exe_Work'] = L
        LineCount =+ 1
        
    File.close()  
    return PersonalData


# TTS --------------------------------------------------------------------------------------------------
# TTS("안녕하세요. Aiden 입니다.", 'ko')
from gtts import gTTS    
from playsound import playsound
import os
def TTS(Text, Language):
    if os.path.isfile('Data/TTS.mp3'): os.remove('Data/TTS.mp3')  
    TTS = gTTS(text=Text, lang=Language)
    TTS.save("Data/TTS.mp3")
    while True :
        try:
            playsound("Data/TTS.mp3", block=True) 
        except : #PlaysoundException
            playsound("Data/TTS.mp3", block=True)
        else: break
    os.remove('Data/TTS.mp3')  



# STT --------------------------------------------------------------------------------------------------
# STT('ko-KR')
import speech_recognition as sr
def STT(Language):
    
    while(True):
        # Record Audio
        Record = sr.Recognizer()
        with sr.Microphone() as source:
            Audio = Record.listen(source)

        try:
            Input_Text = Record.recognize_google(Audio, language=Language)
            return Input_Text
        
        except sr.UnknownValueError: continue
        except sr.RequestError: continue



# Analysis ---------------------------------------------------------------------------------------------
from konlpy.tag import Okt
def KoNLpy(Text):
    Text_Km = '"{}"'.format(Text)
    okt = Okt()
    Input_Text_Normalize = okt.normalize(Text_Km)
    Input_Text_Pos_Array = okt.pos(Input_Text_Normalize)
    Input_Text_Pos_Array_Lenth = len(Input_Text_Pos_Array)

    Analysis_Verb_List = []
    Analysis_Noun_List = []
    Analysis_Adjective_List = []

    while(Input_Text_Pos_Array_Lenth > 0):
        Input_Text_Pos_Array_Lenth = Input_Text_Pos_Array_Lenth - 1
        
        if (Input_Text_Pos_Array[Input_Text_Pos_Array_Lenth][1] == "Verb") :
            Analysis_Verb_List.append(Input_Text_Pos_Array[Input_Text_Pos_Array_Lenth][0])
        if (Input_Text_Pos_Array[Input_Text_Pos_Array_Lenth][1] == "Noun") :
            Analysis_Noun_List.append(Input_Text_Pos_Array[Input_Text_Pos_Array_Lenth][0])
        if (Input_Text_Pos_Array[Input_Text_Pos_Array_Lenth][1] == "Adjective") :
            Analysis_Adjective_List.append(Input_Text_Pos_Array[Input_Text_Pos_Array_Lenth][0])

    
    Analysis_Output = [Input_Text_Normalize, Input_Text_Pos_Array, Analysis_Verb_List, Analysis_Noun_List, Analysis_Adjective_List, len(Input_Text_Pos_Array)]

    return Analysis_Output
    '''
    Analysis_Output [0] - 정규화된 문장
    Analysis_Output [1] - 정렬되지 않은 요소들
    Analysis_Output [2] - 동사 리스트
    Analysis_Output [3] - 명사 리스트
    Analysis_Output [4] - 형용사 리스트
    Analysis_Output [5] - 요소 개수
    '''


# RULE -------------------------------------------------------------------------------------------------
def RULE(Text, PersonalData):

    # 시간 
    if  (
        ("시간" in Text[3] and "알려" in Text[2] and "줘" in Text[2]) or 
        ("시야" in Text[3] and "몇" in Text[3] and "지금" in Text[3]) or 
        ("되지" in Text[2] and "시간" in Text[3] and "지금" in Text[3] and "어떻게" in Text[4])
        ):
        #['"시간 알려 줘"', [###], ['줘', '알려'], ['시간'], [], 5]
        #['"지금 몇 시야"', [###], [], ['시야', '몇', '지금'], [], 5]
        #['"지금 시간이 어떻게 되지"', [###], ['되지'], ['시간', '지금'], ['어떻게'], 7]
        import datetime
        now = datetime.datetime.now()

        Return = "지금 시간은 "+ str(now.month)+ "월 "+ str(now.day)+ "일 "+ str(now.hour)+ "시 "+ str(now.minute)+ "분 "+ str(now.second)+ "초 입니다"
        return Return
        
    # 인터넷 실행
    elif(
        ("인터넷" in Text[3] and "열어" in Text[2] and "줘" in Text[2]) or
        ("인터넷" in Text[3] and "작업" in Text[3] and "열어" in Text[2] and "줘" in Text[2])
        ):
        #['"인터넷 열어 줘"', [###], ['줘', '열어'], ['인터넷'], [], 5]
        import webbrowser
        TTS("인터넷을 실행합니다. 작업환경 브라우저를 구성하시겠습니까?", 'ko')
        PERSONALDATA        = LPD('Data/PersonalData.csv')
        TEXT_INPUT_RAW      = STT('ko-KR')
        TEXT_INPUT_KoNLpy   = KoNLpy(TEXT_INPUT_RAW)
        if  (
            ("해" in TEXT_INPUT_KoNLpy[3]) or
            ("응" in TEXT_INPUT_KoNLpy[3]) or
            ("그래" in TEXT_INPUT_KoNLpy[4]) or
            ("그래요" in TEXT_INPUT_KoNLpy[4])
            ):
            #['"응"', [###], [], ['응'], [], 3]
            #['"그렇게 해"', [###], [], ['해'], [], 4]
            #['"그래"', [###], [], [], ['그래'], 3]
            #['"그래요"', [###], [], [], ['그래요'], 3]
            for URL in PersonalData['Bookmarks']:
                try : webbrowser.open(URL)
                except : pass
            Return = "작업환경 브라우저를 실행했습니다."
        else:
            try : webbrowser.open("https://www.google.com/")
            except : pass
            Return = "인터넷을 실행했습니다."
        return Return

    # 작업환경 구성
    elif(
        ("구성" in Text[3] and "환경" in Text[3] and "작업" in Text[3] )
        ):
        #['"작업 환경 구성 해 줘"', [###], ['줘'], ['해', '구성', '환경', '작업'], [], 7]
        import webbrowser
        for URL in PersonalData['Bookmarks']:
            try : webbrowser.open(URL)
            except : pass
        import subprocess
        for EXE in PersonalData['Exe_Work']:
            try : subprocess.run([EXE])
            except : pass
        Return = "작업환경을 구성했습니다."
        return Return

    else: return False


# TRANSFORMER ------------------------------------------------------------------------------------------
import tensorflow as tf
import re
def TRANSFORMER(Text):
    model = tf.keras.models.load_model('Aiden.h5')



