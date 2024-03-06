import speech_recognition as sr
import pyaudio
import wave
import random
from gtts import gTTS
import os
import pygame
import webbrowser
# import urllib.request
# from urllib import request


# ФУНКЦИЯ ДЛЯ ЗАПИСИ И РАСПОЗНАВАНИЯ РЕЧИ
def speech_rec():
    CHUNK = 1024
    FRT = pyaudio.paInt16
    CHAN = 1
    RT = 44100
    REC_SEC = 5  #ДЛИТЕЛЬНОСТИ ЗАПИСИ АУДИО
    OUTPUT = "output.wav"
    p = pyaudio.PyAudio()
    print("Пожалуйста, говорите")
    stream = p.open(format=FRT, channels=CHAN, rate=RT, input=True, frames_per_buffer=CHUNK)
    frames = []
    for i in range(0, int(RT / CHUNK * REC_SEC)):
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    w = wave.open(OUTPUT, 'wb')
    w.setnchannels(CHAN)
    w.setsampwidth(p.get_sample_size(FRT))
    w.setframerate(RT)
    w.writeframes(b''.join(frames))
    w.close()
    r = sr.Recognizer()
    harvard = sr.AudioFile('output.wav')
    with harvard as source:
        audio = r.record(source)
    return r.recognize_google(audio, language="ru-RU")


# ФУНКЦИЯ ДЛЯ ВОСПРОИЗВЕДЕНИЯ ОТВЕТА
def answer():
    # os.system("start example.mp3")
    pygame.init()
    pygame.mixer.music.load("example.mp3")
    pygame.mixer.music.play()

    clock = pygame.time.Clock()
    while pygame.mixer.music.get_busy():
        clock.tick(60)
        pygame.event.poll()
    pygame.quit()


# ВОЗМОЖНЫЕ ФРАЗЫ
bye = ['пока', 'до свидания']
bye1 = ['Приятно было пообщаться', 'Рада была помочь']
sps = ['спасибо']
yaw = ['Рада помочь', 'Всегда пожалуйста', 'Обращайтесь']
hello = ['привет', 'здравствуйте', 'здравствуй']
site = {}
site['дневник'] = 'https://dnevnik.ru/feed'
site['яндекс'] = 'https://ya.ru/?utm_referrer=https%3A%2F%2Fyandex.ru%2F'

frase = speech_rec().lower()
# print(frase)
while frase not in bye:
    if frase in sps:
        mytext = random.choice(yaw)
        audio = gTTS(text=mytext, lang="ru", slow=False)
        audio.save("example.mp3")
        answer()
        os.remove("example.mp3")
    elif 'открой' in frase:
        a = frase.index('й')
        frase = frase[a + 2:]
        print('открываю')
        webbrowser.open(site[frase]) # ОТКРЫТИЕ САЙТА
        # webUrl = request.urlopen('https://sochisirius.ru/obuchenie/nauka/smena1783/8255')
    elif frase in hello:
        mytext = random.choice(hello)
        audio = gTTS(text=mytext, lang="ru", slow=False)
        audio.save("example.mp3")
        answer()
        os.remove("example.mp3")
    else:
        print('Извините, я вас не понимаю')
        mytext = 'Извините, я вас не понимаю'
        audio = gTTS(text=mytext, lang="ru", slow=False)
        audio.save("example.mp3")
        answer()
        os.remove("example.mp3")
    frase = speech_rec().lower()


mytext = random.choice(bye1)
aud = gTTS(text=mytext, lang="ru", slow=False)
aud.save("end.mp3")
pygame.init()
pygame.mixer.music.load("end.mp3")
pygame.mixer.music.play()

clock = pygame.time.Clock()
while pygame.mixer.music.get_busy():
    clock.tick(60)
    pygame.event.poll()
pygame.quit()
# ЗАВЕРШЕНИЕ ПРОГРАММЫ