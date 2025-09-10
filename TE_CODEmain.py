import cv2
import pytesseract
import pyttsx3


# Try to import GPIO (only works on Raspberry Pi)
try:
import RPi.GPIO as GPIO
ON_PI = True
except:
ON_PI = False


# Camera index (0 = default camera)
CAMERA_INDEX = 0
# GPIO pin for button
BUTTON_GPIO = 18


# Setup TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)


def speak(text):
print("Speaking:", text)
engine.say(text)
engine.runAndWait()


def capture_and_read():
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
print("Camera not found!")
speak("Camera not found!")
return


ret, frame = cap.read()
cap.release()


if not ret:
print("Failed to capture image")
speak("Failed to capture image")
return


# Convert image to text
text = pytesseract.image_to_string(frame)
if text.strip():
print("Recognized text:\n", text)
speak(text)
else:
print("No text found")
speak("No text detected")


# GPIO setup for Raspberry Pi
if ON_PI:
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)


print("Press the button to capture and read text.")
try:
while True:
if GPIO.input(BUTTON_GPIO) == GPIO.LOW:
capture_and_read()
cv2.waitKey(500) # debounce delay
except KeyboardInterrupt:
GPIO.cleanup()
else:
# Test mode without GPIO
print("Press Enter to capture and read text (Ctrl+C to exit)")
try:
while True:
input()
capture_and_read()
except KeyboardInterrupt:
print("Exiting...")