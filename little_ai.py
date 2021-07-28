
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia as wiki
import webbrowser as wb
import psutil
import pyjokes
import os
import random 
import wolframalpha
import pyautogui
import cv2
import time
import numpy as np
import autopy
import numpy as np
import hand_detction as htm
import time
import cv2

engine = pyttsx3.init()
engine.runAndWait()
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def Time():
    tim=datetime.datetime.now().strftime("%I:%M:%S")
    speak('the current time is')
    speak(tim)
    
def Date():
    date=datetime.date.today()
    speak('today is')
    speak(date)
    
def command():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.2)
        print('listing......')
        audio=r.listen(source)
        
    try:
        print('recognizing....')
        query = r.recognize_google(audio,language='en-US').lower()
        print('your query:'+query)
        return query
        
    except Exception as e:
        print(e)
        print('i didnt listen anything')
        return "None"
    
def google():
    speak('what should i search in google')
    query = command()
    url = "https://www.google.com.tr/search?q={}".format(query)
    wb.open_new_tab(url)
        
if __name__ == '__main__':
    clear = lambda: os.system('cls')
    clear()
    now=datetime.datetime.now().hour
    if(6<=now<12):
        speak('good morning pani')
    elif(12<=now<15):
        speak('good afternoon pani')
    elif(15<=now<19):
        speak('good evening pani')
    elif(19<=now<23):
        speak('good night pani')
    else:
        speak('what time is it go and sleep')
        
    Time()
    Date()
    speak('im always at your service!! tell me what to do')
    while(1):
        query = command()
        if 'time' in query:
            Time()
        elif 'date' in query:
            Date()
        elif 'wikipedia' in query:
            speak('what should i search in wikipedia')
            query = command()
            result=wiki.summary(query,sentences=3)
            print(result)
            speak(result)
#may generate ambious error 
        elif 'open google' in query:
           google()
    
        elif 'open youtube' in query:
            speak('what should i search in youtube')
            query = command()
            wb.open('https://www.youtube.com/results?search_query='+query)
        
        elif 'system status' in query:
            usage = str(psutil.cpu_percent())
            speak('cpu usage percentage is at'+usage)
            battery = psutil.sensors_battery()
            speak('battery is at a percentage of')
            speak(battery.percent)
    
        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'mouse' in query:
            cTime = 0
            pTime = 0
            x1 = 0
            x2 = 0
            y1 = 0
            y2 = 0
            plocx, plocy = 0, 0
            clocx, clocy = 0, 0
            smooth = 7
            wcam, hcam = 640, 480
            frame_red = 50
            wscr, hscr = autopy.screen.size()
            camera = cv2.VideoCapture(0)
            detector = htm.handDetector(maxHands=1)
            while True:

                success, img = camera.read()
                img = detector.findHands(img)
                lmlist, bbox = detector.findPosition(img)

                if len(lmlist) != 0:
                    x1, y1 = lmlist[8][1:]
                    x2, y2 = lmlist[12][1:]
                    # print(x1,x2,y1,y2 )
                    fingers = detector.fingersUp()
                    cv2.rectangle(img, (frame_red, frame_red), (wcam - frame_red, hcam - frame_red), (255, 0, 255))
                    if fingers[1] == 1 and fingers[2] == 0:
                        x3 = np.interp(x1, (frame_red, wcam - frame_red), (0, wscr))
                        y3 = np.interp(y1, (frame_red, hcam - frame_red), (0, hscr))
                        clocx = plocx + (x3 - plocx) / smooth
                        clocy = plocy + (y3 - plocy) / smooth

                        autopy.mouse.move(wscr - clocx, clocy)
                        cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)
                        plocx, plocy = clocx, clocy
                    if fingers[1] == 1 and fingers[2] == 1:
                        leng, img, lineinfo = detector.findDistance(8, 12, img)
                        if leng < 40:
                            cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
                            autopy.mouse.click()

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime

                cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 255), 3)
                cv2.imshow('main', img)
                k = cv2.waitKey(1)
                if k == ord('q'):
                    break
            cv2.destroyAllWindows()
            camera.release()

        elif 'yourself' in query:
            speak("iam just a python application,"
                 "im created by pani to make your life easy,"
                 "im always at your service and i will always help you at my level")
        
        elif 'log out' in query:
            os.system("shutdown -l")
        elif 'restart' in query:
            os.system("shutdown /r /t 1")
        elif 'shutdown' in query:
            os.system("shutdown /s /t 1")
        elif 'songs' in query:
            path = r"C:\Users\91967\Music\Songs"
            files=os.listdir(path)
            d=random.choice(files)
            print(d)
            speak('playing'+d)
            os.startfile(os.path.join(path,d))
        elif 'offline' in query or 'bye' in query or 'exit' in query:
            speak('going offline byeee pani!')
            break
        elif 'stop listening' in query or 'sleep' in query or 'wait' in query:
            speak('could you specify time in seconds to stop listening')
            a = float(command())
            time.sleep(a)
        elif 'calculate' in query or 'who' in query or 'what' in query:
            app_id = "TGQK5X-9569RA4GHT"
            client = wolframalpha.Client(app_id)
            res = client.query(query)
            answer = next(res.results).text
            print(answer)
            speak(answer)
        elif 'where is' in query:
            query = query.replace('where is',"")
            speak('opening'+query+'in maps')
            wb.open("https://www.google.com/maps/place/"+ query + "")
            
        elif 'screenshot' in query:
            img = pyautogui.screenshot()
            img.save(r'C:\Users\91967\Pictures\Screenshots\img from python\sc.png')
            speak('done pani')
            cv2.imshow('pic',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite('test.jpg',frame)
                break
            
        elif 'open camera' in query or 'take picture' in query:
            camera = cv2.VideoCapture(0)
            while(1):
                ret,frame = camera.read()
                if ret == True:
                    cv2.imshow('pic',frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.imwrite('test.jpg',frame)
                        break
                else:
                    break
            camera.release()
            cv2.destroyAllWindows()
        elif 'None' in query:
            pass

        else:
            speak('sorry i didnt get that can i search in google')
            query = command()
            if 'yes' in query or 'yeah' in query:
                google()
            else:
                speak('say command again')
                pass

camera.release()
cv2.destroyAllWindows()



