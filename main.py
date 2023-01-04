import moviepy.editor as mpy
from selenium import webdriver
from pydub import AudioSegment
from gtts import gTTS
from PIL import Image
from mongo import Mongo
import reddit as r
import pyautogui
import json
import config
import subredditlist
import selenium_util
import os
import math
import time


def upload(subreddit):
    firefox_profile = webdriver.FirefoxProfile(config.getProperty('firefox_profile_path'))
    fox = webdriver.Firefox(firefox_profile=firefox_profile)
    fox.get("https://www.tiktok.com/upload?lang=sv-SE")

    time.sleep(2)

    pyautogui.click(800, 320)
    pyautogui.typewrite(get_tags(subreddit))

    time.sleep(1)

    pyautogui.click(613, 692)
    time.sleep(1)

    pyautogui.click(83, 359)
    time.sleep(1)

    pyautogui.click(241, 172)
    pyautogui.click(241, 172)
    time.sleep(20)

    pyautogui.click(1014, 963)
    time.sleep(10)
    fox.quit()


def get_tags(subreddit):
    return f"{subreddit} #python #reddit #automation #{subreddit} #foryou"

def selenium_printscreen_title_and_content(subreddit):
    firefox_profile = webdriver.FirefoxProfile(config.getProperty('firefox_profile_path'))
    fox = webdriver.Firefox(firefox_profile=firefox_profile)
    fox.get(subreddit)
    time.sleep(0.5)

    for index, x in enumerate(selenium_util.xpaths):
        element_post = fox.find_element('xpath', x)
        element_post.screenshot('results/img/postContent.png')
        image_path = "results/img/postContent.png"
        try:
            img = Image.open(image_path)
        except FileNotFoundError:
            print(f'Unable to open image in path: {image_path}')
            return None

        if img.height >= 150:
            print("length longer than 150")
            break
        if img.height < 150 and index == len(selenium_util.xpaths) - 1:
            fox.quit()
            raise Exception("None of the xpaths generated a image that passes the requirements")
        if img.height < 150:
            print("lenght shorter than 150, continuing with other xpath....")

    element_post = fox.find_element('xpath',
                                    '/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/div[1]/div[2]/div[1]/div')
    element_post.screenshot('results/img/postTitle.png')
    fox.quit()


def video_stuff(audio_durations_array):
    audio_title_duration = audio_durations_array[0]
    audio_content_duration = audio_durations_array[1]

    print(f'title dur: {audio_title_duration}')
    print(f'content dur: {audio_content_duration}')

    # Image to add to title video
    title_image = (mpy.ImageClip("results/img/postTitle.png")
                   .set_duration(audio_title_duration + 2)
                   .set_pos('center').resize(width=1000))

    # Audio to title video
    intro_title_audio = mpy.AudioFileClip('results/audio/test_title.mp3')

    # Intro title video
    intro_title_display = get_concatenated_background_video(3)
    final_intro_title_display = mpy.CompositeVideoClip([intro_title_display, title_image]) \
        .subclip(0, audio_title_duration).set_audio(intro_title_audio)
    print(f'intro vid duration: {final_intro_title_display.duration}')

    # Content title video
    content_image = (mpy.ImageClip('results/img/postContent.png')
                     .set_duration(audio_content_duration + 3)
                     .set_pos('center')
                     .resize(width=1000))

    content_audio = mpy.AudioFileClip('results/audio/test_content.mp3')

    content_display = get_concatenated_background_video(15)
    final_content_display = mpy.CompositeVideoClip([content_display, content_image]) \
        .subclip(0, audio_content_duration + 2) \
        .set_audio(content_audio)

    # Final video
    final = mpy.concatenate_videoclips([final_intro_title_display, final_content_display])

    # Resize to save some disk space
    final.resize((720, 1280))

    # Preview or write
    # final.show(15, interactive=True)
    final.write_videofile('results/vid/result.mp4', threads=12, fps=30)


def get_concatenated_background_video(n):
    tmp = []
    for x in range(n):
        tmp.append(mpy.VideoFileClip('assets/pexels-ekaterina-bolovtsova.mp4'))
    return mpy.concatenate_videoclips(tmp, method='compose')


def text_to_speech_stuff(text_array):
    # engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0])
    # engine.setProperty('rate', 150)
    # engine.save_to_file(text_array[0], 'results/audio/test_title.mp3')
    # engine.save_to_file(text_array[1], 'results/audio/test_content.mp3')
    # engine.runAndWait()
    speech = gTTS(text=text_array[0], lang='en', tld='ca')
    speech.save('results/audio/test_title.mp3')
    speech = gTTS(text=text_array[1], lang='en', tld='ca')
    speech.save('results/audio/test_content.mp3')

    audio_title = AudioSegment.from_file(os.getcwd() + "\\results\\audio\\test_title.mp3")
    audio_content = AudioSegment.from_file(os.getcwd() + "\\results\\audio\\test_content.mp3")

    return [math.ceil(audio_title.duration_seconds), math.ceil(audio_content.duration_seconds)]


def fetch_reddit_stuff(subreddit):
    reddit = r.return_instance()
    blob = json.loads(r.return_blob(subreddit, reddit))
    return blob


def save_to_db(dict):
    db = Mongo()
    tmp = {"title": dict["title"], "content": dict["content"], "ups": dict["ups"], "url": dict["url"]}
    db.save(tmp)


def main():
    # subreddit = subredditlist.getRandomSub()
    subreddit = 'tifu'
    reddit_json_blob = fetch_reddit_stuff(subreddit)
    selenium_printscreen_title_and_content(reddit_json_blob['url'])
    audio_durations = text_to_speech_stuff([reddit_json_blob['title'], reddit_json_blob['content']])
    save_to_db(reddit_json_blob)
    video_stuff(audio_durations)
    upload(subreddit)


if __name__ == "__main__":
    main()
