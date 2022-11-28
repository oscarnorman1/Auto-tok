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


def seleniumstuff(subreddit):
    firefox_profile = webdriver.FirefoxProfile(config.getProperty('firefox_profile_path'))

    fox = webdriver.Firefox(firefox_profile=firefox_profile)
    fox.get(f'https://www.reddit.com/r/{subreddit}/top/?t=week')

    # element_cookie = fox.find_element('xpath', '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[3]/div[1]/section/div/section[2]/section[1]/form/button')
    # element_cookie.click()
    # time.sleep(1)

    element_post = fox.find_element('xpath',
                                    '/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[4]/div[1]/div[4]/div[2]/div')
    element_post.screenshot('results/img/postTitle.png')
    fox.quit()


def video_stuff(json_blob, audio_durations_array):
    sentence_list = json_blob['sentence_list']
    text_clips_list = []

    audio_title_duration = audio_durations_array[0]
    audio_content_duration = audio_durations_array[1]

    print(f'title dur: {audio_title_duration}')
    print(f'content dur: {audio_content_duration}')

    # Image to add to title video
    image_original = (mpy.ImageClip("results/img/postTitle.png").set_duration(7).set_pos('center'))

    # Audio to title video
    intro_title_audio = mpy.AudioFileClip('results/audio/test_title.mp3')

    # Intro title video
    intro_title_display = get_concatenated_background_video(3)
    final_intro_title_display = mpy.CompositeVideoClip([intro_title_display, image_original]) \
        .subclip(0, audio_title_duration + 2).set_audio(intro_title_audio)
    print(f'intro vid duration: {final_intro_title_display.duration}')

    final_intro_title_display.write_videofile('result.mp4', threads=12, fps=30)

    # Content title video
    comment_display = get_concatenated_background_video(15)
    for sentence in sentence_list:
        text_clip = mpy.TextClip(sentence, font="Arial", fontsize=45, color='white').set_position(
            'center').set_duration(3)
        text_clips_list.append(text_clip)
    final_text_clip = mpy.concatenate_videoclips(text_clips_list).set_position('center')
    final_comment_display = mpy.CompositeVideoClip([comment_display, final_text_clip])\
        .subclip(0, audio_content_duration)

    # Final video
    final = mpy.concatenate_videoclips([final_intro_title_display, final_comment_display])

    # Preview or write
    final.resize((720, 1280))
    # final.show(2, interactive=True)
    final.write_videofile('result.mp4', threads=12, fps=30)


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
    subreddit = 'TrueOffMyChest'
    reddit_json_blob = fetch_reddit_stuff(subreddit)
    seleniumstuff(subreddit)
    audio_durations = text_to_speech_stuff([reddit_json_blob['title'], reddit_json_blob['sentence_list_full']])
    video_stuff(reddit_json_blob, audio_durations)


if __name__ == "__main__":
    main()
