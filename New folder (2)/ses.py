import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
duration = 3  # kayıt saniyeleri
sample_rate = 44100
can = 4
seviyeye_göre_kelimeler = {
    "kolay": ["kedi", "köpek", "elma", "süt", "güneş", "araba", "ev", "masa", "kitap", "telefon"],
    "orta": ["muz", "okul", "arkadaş", "pencere", "sarı", "masa", "kitap", "telefon", "çanta", "bilgisayar"],
    "zor": ["teknoloji", "üniversite", "bilgi", "telaffuz", "hayal gücü", "yaratıcılık", "deneyim", "gelişim", "farkındalık", "sorumluluk"]
}
def konusma(kelime):
    global can,googletrans,sr,wav,sd,np
    print("Şimdi konuşun...")
    recording = sd.rec(
        int(duration * sample_rate), # kaydedilecek örnek sayısı
        samplerate=sample_rate,      # örnekleme hızı
        channels=1,                  # 1, mono kayıt anlamına gelir.
        dtype="int16")               # kayıtlı örnekler için veri türü
    sd.wait()  
    wav.write("output.wav", sample_rate, recording)
    print("Kayıt tamamlandı, şimdi tanıma işlemi devam ediyor...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="en")
        recognized = text.lower()
        print("Şunu söylediniz:", recognized)
        translator = Translator()
        translated = translator.translate(kelime, dest="en")
        ingilizce_ceviri = translated.text.lower()
        print(f"çeviri:", translated.text)
        if recognized == ingilizce_ceviri:
            print("Tebrikler! Doğru söylediniz.")
        else:
            can =  can - 1
            print(can)
            print("Maalesef, doğru söylemediniz. Doğru kelime:", kelime)
    except:
        can = can - 1
        print(can)
        print(kelime)
        print("Üzgünüm, sesi tanıyamadım. Lütfen tekrar deneyin.")


seviy = input("Lütfen bir seviye seçin kolay, orta, zor ").lower()
while can > 0: 
    kelime = random.choice(seviyeye_göre_kelimeler[seviy])
    konusma(kelime)
print("Oyun bitti")