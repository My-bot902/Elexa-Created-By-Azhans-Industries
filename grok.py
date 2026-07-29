import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import time
import webbrowser
import videolibrary 
import datetime
import threading
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ============== SETUP ==============
recognizer = sr.Recognizer()
yes_boss_file = "yes_boss.mp3"
ai_active = False  # Check karne ke liye ke voice pehle se chal rahi hai ya nahi

if not os.path.exists(yes_boss_file):
    tts = gTTS(text="Yes Boss!", lang='en-uk', slow=False)
    tts.save(yes_boss_file)

def speak(text):
    try:
        print(f"Elexa: {text}")
        if text.lower() == "yes boss!":
            playsound.playsound(yes_boss_file)
        else:
            tts = gTTS(text=text, lang='en-uk', slow=False)
            temp_file = "temp_voice.mp3"
            tts.save(temp_file)
            playsound.playsound(temp_file)
            os.remove(temp_file)
    except Exception as e:
        print(f"Speak Error: {e}")

def wish_me():                                    
    hour = int(datetime.datetime.now().hour)      
    if hour < 12: speak("Good Morning!")                    
    elif hour < 18: speak("Good Afternoon!")                  
    else: speak("Good Evening!")

# ============== CORE AI LOGIC ==============
def process_command(command):
    command = command.lower().strip()
    response = ""

    if "elexa".lower() in command:
        response = "yes Boss!"
    elif "open youtube" in command or "youtube kholo" in command:
        response = "Opening YouTube"
        webbrowser.open("https://youtube.com")
    elif "google ai" in command or "google ai kholo" in command:
        response = "Opening Google AI"
        webbrowser.open("https://google.com")
    elif "open pixverse" in command or "pixverse kholo" in command:
        response = "Opening Pixverse"
        webbrowser.open("https://pixverse.com")
    elif any(x in command for x in ["capcut", "cap cut", "capcut kholo"]):
        response = "Opening CapCut"
        capcut_path = r"C:\Users\M AZHAN\AppData\Local\CapCut\Apps\CapCut.exe"
        try: os.startfile(capcut_path)
        except: response = "Sorry, I could not find CapCut on your PC."
    elif "chill" in command or "Chill" in command:
        response=" Openeing Youtube channel chilltone by Us-sud khan" 
        webbrowser.open("https://www.youtube.com/@Chilltoons-1hub")
    elif "Atif" in command or "atif" in command:
        response="Showing picture of Atif" 
        webbrowser.open("https://i.insider.com/5229449eecad04c3708b4570?width=1366&format=jpeg&auto=avif&quality=85%2C80")
    elif "Azhan" in command or "azhan" in command:
        response="Showing picture of Uh-ZAHN" 
        webbrowser.open("https://oyster.ignimgs.com/wordpress/stg.ign.com/2020/12/daredevil-1280jpg-782297_1280w.jpg")
    elif "Umair" in command or "umair" in command:
        response="Showing picture of Oo-MARE" 
        webbrowser.open("https://www.google.com/imgres?q=ugly%20mans%20in%20goodlook&imgurl=https%3A%2F%2Fthumbs.dreamstime.com%2Fb%2Fold-man-sad-face-30758277.jpg&imgrefurl=https%3A%2F%2Fwww.dreamstime.com%2Fphotos-images%2Fugly-man.html&docid=0V9YVaVuq0aGIM&tbnid=zgvcUcrOFwnOnM&vet=12ahUKEwj1hN-t6KOUAxUbMvsDHVfOCdIQnPAOegQIGRAB..i&w=800&h=621&hcb=2&ved=2ahUKEwj1hN-t6KOUAxUbMvsDHVfOCdIQnPAOegQIGRAB")
    elif "shah" in command or "shah" in command:
        response="Showing picture of Shah ji" 
        webbrowser.open("https://www.google.com/imgres?q=ugly%20animal%20that%20are%20so%20weak%20and%20thin&imgurl=https%3A%2F%2Fs.yimg.com%2Fny%2Fapi%2Fres%2F1.2%2F9BmTifND1tnX0ufXefujiw--%2FYXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTYxOTtjZj13ZWJw%2Fhttps%3A%2F%2Fmedia.zenfs.com%2Fen%2Floveexploring_uk_835%2Fd8d18632c951fe34c4fefef1732b4fb1&imgrefurl=https%3A%2F%2Fuk.style.yahoo.com%2Fhilarious-photos-reveal-worlds-ugliest-133100356.html&docid=QScRDx0xYUEtWM&tbnid=ZOccDRZptnvZ-M&vet=12ahUKEwjFy6mO6KOUAxXL0wIHHbwdEfE4ChCc8A56BAglEAE..i&w=959&h=619&hcb=2&ved=2ahUKEwjFy6mO6KOUAxXL0wIHHbwdEfE4ChCc8A56BAglEAE")
        
    elif "subhan" in command or "Subhan" in command:
        response="Showing picture of subhan" 
        webbrowser.open("https://www.google.com/imgres?q=ugly%20animal%20with%20half%20white%20hairs&imgurl=https%3A%2F%2Fimg.wattpad.com%2F6ccbaf24285de5c17d9c389ced2295bffa227109%2F68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f7551484a675143357758457559513d3d2d3531383137343131372e313530373136383165626537333236663530323436333037303530302e6a7067%3Fs%3Dfit%26w%3D720%26h%3D720&imgrefurl=https%3A%2F%2Fwww.wattpad.com%2F518174117-my-random-art-d-ugly-animals-lol&docid=wJWRR5T30QgVLM&tbnid=ycrK0YoEqeQh-M&vet=12ahUKEwjbq_TY5KOUAxURTaQEHZThDO4QnPAOegQIURAB..i&w=480&h=360&hcb=2&ved=2ahUKEwjbq_TY5KOUAxURTaQEHZThDO4QnPAOegQIURAB")
        
    elif 'naveed' in command:
        response = "Naveed is a cute person and a dangerous coder. He is a secret agent of NASA!"
    elif 'ali' in command:
        response = "Ali is a great person. He is very helpful and kind."
    elif 'asad' in command:
        response = "Us-sud eck paa-gull lur-kah hay, joe jub day-kho dee-maagh khuh-raab kur-tah hay!"
    elif "mausam" in command:
        response = "Aaj kah maw-sam baw-hot a-chah hai."
    elif "naam kya hai" in command:
        response = "Mera naam Elexa hai, aapki digital assistant!"
    elif command.startswith("play"):
        video_query = command.replace("play", "").strip()
        found = False
        for name, link in videolibrary.video.items():
            if name.lower() == video_query:
                webbrowser.open(link)
                response = f"Playing {name} from your library."
                found = True
                break
        if not found:
            response = f"Sorry I cannot play '{video_query}' at this momernt. ."
    elif "stop" in command:
        response = "Stopping the process. Goodbye!"
    else:
        response = f" {command}"

    threading.Thread(target=speak, args=(response,)).start()
    return response

# ============== FLASK ROUTES ==============
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ai')
def ai_page():
    global ai_active
    # Voice assistant sirf tab start hoga jab user pehli baar AI page open karega
    if not ai_active:
        threading.Thread(target=voice_loop, daemon=True).start()
        ai_active = True
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_msg = data.get("message")
    answer = process_command(user_msg)
    return jsonify({"reply": answer})

# ============== VOICE LOOP ==============
def voice_loop():
    speak("Initializing Elexa...")
    wish_me()
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                query = recognizer.recognize_google(audio, language='en-in').lower()
                if "alexa" in query or "elexa" in query:
                    speak("Yes Boss!")
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio, language='en-in')
                    process_command(command)
            except:
                continue

if __name__ == '__main__':
    # Threading yahan se hata di hai taake terminal par chalte hi na bole
    app.run(debug=True, use_reloader=False)
