# Coronavirus-recovered-and-active-cases-live-update-via-speech-recognition-
This program allows the user to speak directly into the microphone to ask for live updates on the number of recovered cases or active cases of a specific country. Total recovered and active cases in the world are also available if the user wants to know that. The program will answer the user back with a value scrape from worldometers.com, a website that gives live updates on Coronavirus. Should the user want to know about the latest, updated version of the stats ('refreshed version'), he/she could simply say 'update' and the program will take a short while to process the request and give back the output. This is done via threading. 

The libraries needed for this project are:
1. requests
2. pywin32
3. SpeechRecognition
4. pyttsx3
