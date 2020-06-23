import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import threading
import time

API_KEY = 'tETTfJJc_AAw'
PROJECT_TOKEN = 'tYkSktVp4FWG'
RUN_TOKEN = 'tDquu4jsRasV'

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',
                                params=self.params)
        data = json.loads(response.text)
        return data

    def get_total_recovered(self):
        return self.data['total_recovered']

    def get_total_active_cases(self):
        return self.data['total_active_cases']

    def get_country_data(self, country):
        data = self.data["Country"]

        for content in data:
            if content['name'].lower() == country.lower():
                return content
        return "0"

    def list_of_countries(self):
        countries = []
        data = self.data['Country']
        for content in data:
            countries.append(content['name'].lower())
        return countries

    def update_data(self): # updating the data via threading, polling
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run',
                                 params=self.params)

        def poll():
            time.sleep(0.1)
            old_data = self.data
            while True:
                new_data = self.get_data()
                if new_data != old_data:
                    self.data = new_data
                    print("Data updated")
                    break
                time.sleep(5)

        t = threading.Thread(target=poll)
        t.start()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print("Exception:", str(e))

    return said.lower()

def main():
    print("Started Program")
    speak('Hi sir! What stats would you like to know about Coronavirus today?')
    data = Data(API_KEY, PROJECT_TOKEN)
    END_PHRASE = "stop"
    country_list = data.list_of_countries()

    # for total recovered or active cases in the world
    TOTAL_PATTERNS = {
        re.compile("[\w\s]+ total number of [\w\s]+ recovered cases"): data.get_total_recovered,
        re.compile("[\w\s]+ total recovered"): data.get_total_recovered,
        re.compile("[\w\s]+ total number of [\w\s]+ active"): data.get_total_active_cases,
        re.compile("[\w\s]+ total active"): data.get_total_active_cases
    }
    
    # get data for specific country
    COUNTRY_PATTERNS = {
        re.compile("[\w\s]+ recovered [\w\s]+"): lambda country: data.get_country_data(country)['recovered'],
        re.compile("[\w\s]+ active cases [\w\s]+"): lambda country: data.get_country_data(country)['active_cases'],
    }

    update_command = 'update'
    while True:
        print("Listening...")
        text = get_audio()
        print(text) # print what the user says on the screen
        result = None

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text): # if whatever the user says matches the pattern we created
                words = set(text.split(" ")) # get a list of the words the user says
                for country in country_list: # search for that particular country that user wants
                    if country in words:
                        result = func(country)
                        break

        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break

        if text == update_command:
            result = "Data is being updated. This may take a moment!"
            speak("Data is being updated. This may take a moment!")
            data.update_data()

        if result:
            speak(result) # return the result via microphone

        if text.find(END_PHRASE) != -1:  # stop loop
            speak('Terminating program')
            print("Exit")
            break

main()
