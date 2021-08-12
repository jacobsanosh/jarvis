from gtts import gTTS
from playsound import playsound
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from wikipedia.wikipedia import search
from googlesearch import search as s
import smtplib
import pickle

# text to speech
def speak(audion):
   talk=gTTS(text=audion,lang='en')
   talk.save("adima.mp3")
   playsound('adima.mp3')

#to make wish based on time
def wish():
    C_hour=datetime.datetime.now().hour
    if C_hour>=0 and C_hour<12:
        wish_text="Good morning"    
    elif C_hour>=12 and C_hour<15:
        wish_text="Good afternoon"
    else:
        wish_text="Good evening"
    speak(f"{wish_text} sir i am Alexa . how can i help you")

def takeCommand():
    """used for taking commands using speech module"""
    #It takes microphone input from the user and returns string output
    listen_me=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listen_me.pause_threshold=1  #seconds for non speaking audio
                                    #by this it will incerase the time for speaking between words 
        audio=listen_me.listen(source)
        
        try:
            """recognizing using google it need an good net connection"""
            query=listen_me.recognize_google(audio,language='en-in')

        except Exception as e:
            # print(e)
            speak("sorry sir can you repeat the command one more")
            return "None" #it a string not None 
        #if there is no problem we will return query
        return query

def send_email(id,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    with open("account.pkl",'rb') as file:
        acc_details=pickle.load(file)
    server.login(acc_details['uname'],acc_details['password'])
    server.sendmail(acc_details['uname'],id,content)
    server.close()
    speak("Email sended")
if __name__=="__main__":
    # wish()
    while True:
        query=takeCommand().lower()
        print(query)
        if 'wikipedia' in query:
            speak("searching sir")
            query=query.replace("wikipedia","")#to remove qikipedia from query
            results=wikipedia.summary(query,sentences=2)
            speak(f"according to wikipedia {results}")

        elif 'youtube' in query:
            webbrowser.open("youtube.com")
        elif 'timer' in query:
            webbrowser.open("https://www.google.com/search?q=timer+&sxsrf=ALeKk02uumXjh7epTB_BcVF_rojayymf1Q%3A1628690895741&ei=z9kTYZLcLLCP4-EPzpWC8AQ&oq=timer+&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQkQIyBQgAEJECMggIABCABBCxAzILCAAQgAQQsQMQgwEyCAgAEIAEELEDMggIABCABBCxAzILCAAQgAQQsQMQgwEyCAgAEIAEELEDMggIABCABBCxAzIICAAQgAQQsQM6BwgjEOoCECc6BwguEOoCECc6BAgjECc6BAgAEEM6BQgAEIAEOgsIABCxAxCDARCRAjoICC4QgAQQsQM6CAguELEDEIMBOgUIABCxAzoKCAAQgAQQhwIQFEoECEEYAFCKJliMO2CZSWgBcAF4AIABhAGIAZ4GkgEDMS42mAEAoAEBsAEKwAEB&sclient=gws-wiz-serp&ved=0ahUKEwjS_6eykqnyAhWwxzgGHc6KAE4Q4dUDCA4&uact=5")
        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")
        elif 'search' in query:
            query=query.replace("search","")
            for i in s(query,tld='com', lang='en', num=1,stop=1):
                webbrowser.open(i)
        elif "time" in query:
            a=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"sir the time is {a}")
        elif "send email" in query:
            speak("sir please type the email address because there is a chance of failre in guessing")
            id=input("enter email id    ")
            contents=takeCommand()
            send_email(id,contents)

        elif 'exit' in query:
            exit()
