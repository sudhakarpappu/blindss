import cv2
import pytesseract
from gtts import gTTS
import pygame
import time

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TextReaderApp(App):
    def build(self):
        self.start_time = None
        self.cap = cv2.VideoCapture("http://172.18.225.9:4747/video")
        self.text_read = False

        layout = BoxLayout(orientation='vertical')
        self.image_widget = Image()
        layout.add_widget(self.image_widget)

        self.start_button = Button(text='Start Reading')
        self.start_button.bind(on_press=self.start_reading)
        layout.add_widget(self.start_button)

        Clock.schedule_interval(self.update, 1.0 / 30.0)

        return layout

    def start_reading(self, instance):
        self.start_time = time.time()
        self.text_read = False

    def update(self, dt):
        if self.start_time and not self.text_read:
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite('temp.jpg', frame)
                text = pytesseract.image_to_string('temp.jpg')
                if text:
                    self.say(text)
                    print(text)
                    self.text_read = True

            if time.time() - self.start_time > 20:
                self.start_time = None

    def say(self, words):
        tts = gTTS(text=words, lang='en-au', slow=False)
        tts.save("output.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()

if __name__ == '__main__':
    TextReaderApp().run()
