import moviepy.editor as mpy
from selenium import webdriver
from pydub import AudioSegment
import reddit as r
import json
import config
import subredditlist
import pyttsx3
import os
import math
import time


def selenium_printscreen_title_and_content(subreddit):
    firefox_profile = webdriver.FirefoxProfile(config.getProperty('firefox_profile_path'))
    fox = webdriver.Firefox(firefox_profile=firefox_profile)
    fox.get(subreddit)
    time.sleep(0.5)

    element_post = fox.find_element('xpath',
                                    '/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/div[1]/div[2]/div[1]/div/div[4]/div')
    element_post.screenshot('results/img/postContent.png')

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
        .subclip(0, audio_content_duration + 2)\
        .set_audio(content_audio)

    # Final video
    final = mpy.concatenate_videoclips([final_intro_title_display, final_content_display])

    # Resize to save some disk space
    final.resize((720, 1280))

    # Preview or write
    #final.show(15, interactive=True)
    final.write_videofile('results/vid/result.mp4', threads=12, fps=30)


def get_concatenated_background_video(n):
    tmp = []
    for x in range(n):
        tmp.append(mpy.VideoFileClip('assets/pexels-ekaterina-bolovtsova.mp4'))
    return mpy.concatenate_videoclips(tmp, method='compose')


def text_to_speech_stuff(text_array):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0])
    engine.setProperty('rate', 150)
    engine.save_to_file(text_array[0], 'results/audio/test_title.mp3')
    engine.save_to_file(text_array[1], 'results/audio/test_content.mp3')
    engine.runAndWait()

    audio_title = AudioSegment.from_file(os.getcwd() + "\\results\\audio\\test_title.mp3")
    audio_content = AudioSegment.from_file(os.getcwd() + "\\results\\audio\\test_content.mp3")

    return [math.ceil(audio_title.duration_seconds), math.ceil(audio_content.duration_seconds)]


def fetch_reddit_stuff(subreddit):
    reddit = r.return_instance()
    blob = json.loads(r.return_blob(subreddit, reddit))
    return blob


def main():
    # subreddit = subredditlist.getRandomSub()
    subreddit = 'relationship_advice'
    reddit_json_blob = fetch_reddit_stuff(subreddit)
    selenium_printscreen_title_and_content(reddit_json_blob['url'])
    audio_durations = text_to_speech_stuff([reddit_json_blob['title'], reddit_json_blob['content']])
    video_stuff(audio_durations)


if __name__ == "__main__":
    main()
