from django.shortcuts import render
from django.http import StreamingHttpResponse
from googletrans import Translator
import cv2
import pytesseract
from PIL import Image
from project1.camera import VideoCamera
from gtts import gTTS
import speech_recognition as sr
import os


def imagetotext(request):
    return render(request,'imagetotext.html')

def home(request):
    return render(request, 'home.html')

def gen(camera):
    while True:
        hello = VideoCamera()
        hello.frame()
		
def speechtospeech(request):
    return render(request,'speechtospeech.html')
    
def speech(request):

    flag = 0
    dic = ('afrikaans', 'af', 'albanian', 'sq', 
        'amharic', 'am', 'arabic', 'ar',
        'armenian', 'hy', 'azerbaijani', 'az', 
        'basque', 'eu', 'belarusian', 'be',
        'bengali', 'bn', 'bosnian', 'bs', 'bulgarian',
        'bg', 'catalan', 'ca', 'cebuano',
        'ceb', 'chichewa', 'ny', 'chinese (simplified)',
        'zh-cn', 'chinese (traditional)',
        'zh-tw', 'corsican', 'co', 'croatian', 'hr',
        'czech', 'cs', 'danish', 'da', 'dutch',
        'nl', 'english', 'en', 'esperanto', 'eo', 
        'estonian', 'et', 'filipino', 'tl', 'finnish',
        'fi', 'french', 'fr', 'frisian', 'fy', 'galician',
        'gl', 'georgian', 'ka', 'german',
        'de', 'greek', 'el', 'gujarati', 'gu',
        'haitian creole', 'ht', 'hausa', 'ha',
        'hawaiian', 'haw', 'hebrew', 'he', 'hindi',
        'hi', 'hmong', 'hmn', 'hungarian',
        'hu', 'icelandic', 'is', 'igbo', 'ig', 'indonesian', 
        'id', 'irish', 'ga', 'italian',
        'it', 'japanese', 'ja', 'javanese', 'jw',
        'kannada', 'kn', 'kazakh', 'kk', 'khmer',
        'km', 'korean', 'ko', 'kurdish (kurmanji)', 
        'ku', 'kyrgyz', 'ky', 'lao', 'lo',
        'latin', 'la', 'latvian', 'lv', 'lithuanian',
        'lt', 'luxembourgish', 'lb',
        'macedonian', 'mk', 'malagasy', 'mg', 'malay',
        'ms', 'malayalam', 'ml', 'maltese',
        'mt', 'maori', 'mi', 'marathi', 'mr', 'mongolian',
        'mn', 'myanmar (burmese)', 'my',
        'nepali', 'ne', 'norwegian', 'no', 'odia', 'or',
        'pashto', 'ps', 'persian', 'fa',
        'polish', 'pl', 'portuguese', 'pt', 'punjabi', 
        'pa', 'romanian', 'ro', 'russian',
        'ru', 'samoan', 'sm', 'scots gaelic', 'gd',
        'serbian', 'sr', 'sesotho', 'st',
        'shona', 'sn', 'sindhi', 'sd', 'sinhala', 'si',
        'slovak', 'sk', 'slovenian', 'sl',
        'somali', 'so', 'spanish', 'es', 'sundanese',
        'su', 'swahili', 'sw', 'swedish',
        'sv', 'tajik', 'tg', 'tamil', 'ta', 'telugu',
        'te', 'thai', 'th', 'turkish',
        'tr', 'ukrainian', 'uk', 'urdu', 'ur', 'uyghur',
        'ug', 'uzbek',  'uz',
        'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh',
        'yiddish', 'yi', 'yoruba',
        'yo', 'zulu', 'zu')
    

    def takecommand():  
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening.....")
            r.pause_threshold = 1
            audio = r.listen(source)
    
        try:
            print("Recognizing.....")
            query = r.recognize_google(audio, language='en-in')
            print(f"The User said {query}\n")
        except Exception as e:
            print("say that again please.....")
            return "None"
        return query
    
    
    # Input from user
    # Make input to lowercase
    query = takecommand()
    while (query == "None"):
        query = takecommand()
    
    
    def destination_language():
        print("Enter the language in which you\
        want to convert : Ex. Hindi , English , etc.")
        print()
        
        # Input destination language in
        # which the user wants to translate
        to_lang = takecommand()
        while (to_lang == "None"):
            to_lang = takecommand()
        to_lang = to_lang.lower()
        return to_lang
    
    to_lang = destination_language()
    
    # Mapping it with the code
    while (to_lang not in dic):
        print("Language in which you are trying\
        to convert is currently not available ,\
        please input some other language")
        print()
        to_lang = destination_language()
    
    to_lang = dic[dic.index(to_lang)+1]
    
    translator = Translator()
    

    text_to_translate = translator.translate(query, dest=to_lang)
    
    text = text_to_translate.text
    
   
    speak = gTTS(text=text, lang=to_lang, slow=False)
    
    speak.save("captured_voice2.mp3")

    return render (request,'answer2.html',{'speechy':text})

def videostart(request):
    return StreamingHttpResponse(videostart(VideoCamera()))
def translate(request):
    return render(request,'translate.html')

def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def trans(request):
    ti = request.GET["text"]
    translater = Translator()
    out=translater.translate(ti,dest="en")
    return render(request,'answer.html',{'texty': out.text })

def srans(request):
    ti = request.GET["text"]
    translater = Translator()
    out=translater.translate(ti,dest="en")

  

    return render(request,'answer2.html',{'speechy': out.text })