import os
import time
import datetime
import threading
from flask import Flask, render_template, request, jsonify

# Cloud platforms par microphone aur audio drivers crash hone se bachane ke liye safe imports
try:
    import speech_recognition as sr
    from gtts import gTTS
    import playsound
    import webbrowser
    import videolibrary  # Aapki apni banayi hui local file
    LOCAL_MODE = True
except Exception as e:
    # Agar cloud par deploy ho raha hai to errors skip ho jayenge
    LOCAL_MODE = False

app = Flask(__name__)

# ============== SETUP (Only for Local PC) ==============
yes_boss_file = "yes_boss.mp3"
ai_active = False  

if LOCAL_MODE:
    recognizer = sr.Recognizer()
    if not os.path.exists(yes_boss_file):
        try:
            tts = gTTS(text="Yes Boss!", lang='en-uk', slow=False)
            tts.save(yes_boss_file)
        except:
            pass

def speak(text):
    if not LOCAL_MODE:
        print(f"Cloud Log - Elexa: {text}")
        return
    try:
        print(f"Elexa: {text}")
        if text.lower() == "yes boss!":
            playsound.playsound(yes_boss_file)
        else:
            tts = gTTS(text=text, lang='en-uk', slow=False)
            temp_file = "temp_voice.mp3"
            tts.save(temp_file)
            playsound.playsound(temp_file)
            if os.path.exists(temp_file):
                os.remove(temp_file)
    except Exception as e:
        print(f"Speak Error: {e}")

def wish_me():                                    
    hour = int(datetime.datetime.now().hour)      
    if hour < 12: speak("Good Morning!")                    
    elif hour < 18: speak("Good Afternoon!")                  
    else: speak("Good Evening!")

# ============== CORE AI LOGIC (Smart Web Handling) ==============
def process_command(command):
    command = command.lower().strip()
    response = ""
    action = "none"
    url = ""

    if "elexa" in command:
        response = "Yes Boss!"
        
    elif "open youtube" in command or "youtube kholo" in command or "youtube" in command:
        response = "Opening YouTube"
        action = "open_url"
        url = "https://youtube.com"
        if LOCAL_MODE: webbrowser.open(url)


    elif "open instagram" in command or "instagram kholo" in command or "instagram" in command:
        response = "Opening Instagram"
        action = "open_url"
        url = "https://www.instagram.com/?hl=en"
        if LOCAL_MODE: webbrowser.open(url)

    elif "open tiktok" in command or "tiktok kholo" in command or "tiktok" in command:
        response = "Opening TikTok"
        action = "open_url"
        url = "https://www.tiktok.com/en/"
        if LOCAL_MODE: webbrowser.open(url)

    elif "open games" in command or "games kholo" in command or "games" in command:
        response = "Opening Gaming website for you!"
        action = "open_url"
        url = "hhttps://poki.com/"
        if LOCAL_MODE: webbrowser.open(url)

    elif "open playstore" in command or "playstore kholo" in command or "playstore" in command:
        response = "Opening Playstore"
        action = "open_url"
        url = "https://play.google.com/store/apps?hl=en&pli=1"
        if LOCAL_MODE: webbrowser.open(url)

    elif "google ai" in command or "google ai kholo" in command:
        response = "Opening Google AI"
        action = "open_url"
        url = "https://google.com"
        if LOCAL_MODE: webbrowser.open(url)
    elif "open pixverse" in command or "pixverse kholo" in command:
        response = "Opening Pixverse"
        action = "open_url"
        url = "https://pixverse.com"
        if LOCAL_MODE: webbrowser.open(url)
    elif any(x in command for x in ["capcut", "cap cut", "capcut kholo"]):
        if LOCAL_MODE:
            capcut_path = r"C:\Users\M AZHAN\AppData\Local\CapCut\Apps\CapCut.exe"
            try: 
                os.startfile(capcut_path)
                response = "Opening CapCut on your PC."
            except: 
                response = "Sorry, I could not find CapCut on your PC."
        else:
            response = "Opening CapCut Web Edition for you!"
            action = "open_url"
            url = "https://capcut.com"
    elif "chill" in command:
        response = "Opening Youtube channel chilltone by Us-sud khan" 
        action = "open_url"
        url = "https://www.youtube.com/@Chilltoons-1hub"
        if LOCAL_MODE: webbrowser.open(url)
    elif "atif" in command:
        response = "Showing picture of Atif" 
        action = "open_url"
        url = "https://i.insider.com/5229449eecad04c3708b4570?width=1366&format=jpeg&auto=avif&quality=85%2C80"
        if LOCAL_MODE: webbrowser.open(url)
    elif "azhan" in command:
        response = "Showing picture of Uh-ZAHN" 
        action = "open_url"
        url = "https://oyster.ignimgs.com/wordpress/stg.ign.com/2020/12/daredevil-1280jpg-782297_1280w.jpg"
        if LOCAL_MODE: webbrowser.open(url)
    elif "umair" in command:
        response = "Showing picture of Oo-MARE" 
        action = "open_url"
        url = "https://dreamstime.com"
        if LOCAL_MODE: webbrowser.open(url)
    elif "shah" in command:
        response = "Showing picture of Shah ji" 
        action = "open_url"
        url = "https://zenfs.com"
        if LOCAL_MODE: webbrowser.open(url)
    elif "subhan" in command:
        response = "Showing picture of Subhan" 
        action = "open_url"
        url = "https://wattpad.com"
        if LOCAL_MODE: webbrowser.open(url)
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
        if LOCAL_MODE:
            for name, link in videolibrary.video.items():
                if name.lower() == video_query:
                    webbrowser.open(link)
                    response = f"Playing {name} from your library."
                    action = "open_url"
                    url = link
                    found = True
                    break
        if not found:
            response = f"Sorry, I cannot play '{video_query}' right now."
    elif "stop" in command:
        response = "Stopping the process. Goodbye!"
    else:
        response = f"Mera pass iska jawab nahi hai: {command}"

    # Background safe speaking thread for local PC
    if LOCAL_MODE:
        threading.Thread(target=speak, args=(response,)).start()
        
    return {"reply": response, "action": action, "url": url}

# ============== FLASK ROUTES ==============
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/ai')
def ai_page():
    global ai_active
    # Threads sirf local machine par chalaein, cloud block nahi karega
    if LOCAL_MODE and not ai_active:
        threading.Thread(target=voice_loop, daemon=True).start()
        ai_active = True
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # Frontend json inputs handling
    data = request.get_json() or {}
    user_msg = data.get("message", "") or data.get("command", "")
    
    if not user_msg:
        return jsonify({"reply": "Kuch toh bolo, boss!", "action": "none", "url": ""})
        
    result = process_command(user_msg)
    return jsonify(result)

# ============== VOICE LOOP (Only runs locally) ==============
def voice_loop():
    if not LOCAL_MODE:
        return
    speak("Initializing Elexa...")
    wish_me()
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
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
    app.run(debug=True, use_reloader=False)
