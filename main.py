import moviepy.editor as mpy
from selenium import webdriver
from gtts import gTTS
import reddit as r
import json
import config
import subredditlist


def seleniumstuff(subreddit):
    firefox_profile = webdriver.FirefoxProfile(config.getProperty('firefox_profile_path'))

    fox = webdriver.Firefox(firefox_profile=firefox_profile)
    fox.get(f'https://www.reddit.com/r/{subreddit}/')

    # element_cookie = fox.find_element('xpath', '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[3]/div[1]/section/div/section[2]/section[1]/form/button')
    # element_cookie.click()
    # time.sleep(1)

    element_post = fox.find_element('xpath',
                                    '//*[@id="AppRouter-main-content"]/div/div/div[2]/div[4]/div[1]/div[4]/div[2]/div')
    element_post.screenshot('results/img/postTitle.png')
    fox.quit()


def videostuff(json_blob, text_to_speech):
    sentance_list = json_blob['sentence_list']
    text_clips_list = []
    final_video = None

    background_clip = mpy.VideoFileClip('assets/pexels-ekaterina-bolovtsova.mp4')

    image = (mpy.ImageClip("results/img/postTitle.png").set_duration(5).set_pos('center'))
    final = mpy.CompositeVideoClip([background_clip, image])

    #    textclip_submission_title = mpy.TextClip(json_blob['title'], fontsize=40, color='white') \
    #        .set_position('center').set_duration(5)

    for sentence in sentance_list:
        text_clip = mpy.TextClip(sentence, fontsize=30, color='white').set_position('center').set_duration(2)
        text_clips_list.append(text_clip)

    final_text_clip = mpy.concatenate_videoclips(text_clips_list)
    final = mpy.CompositeVideoClip([final, final_text_clip])
    final.resize(height=1920, width=1080)
    final.write_videofile('result.mp4')



    # TODO: Add some for loops to iterate through len(json_blob['sentence_list']) and create
    # TODO: text to speech, VideoFileClip, TextClip and CompositeVideoClip and lastly concatenate them all


def text_to_speech_stuff(text):
    audio = gTTS(text=text, lang='en', tld='co.uk', slow=False)
    audio.save()


def fetch_reddit_stuff(subreddit):
    reddit = r.return_instance()
    blob = json.loads(r.return_blob(subreddit, reddit))
    # print(blob['title'])
    # print(blob['ups'])
    # print(blob['sentence_list'])
    return blob


def main():
    # subreddit = subredditlist.getRandomSub()
    subreddit = 'TalesFromRetail'
    # seleniumstuff(subreddit)
    reddit_json_blob = fetch_reddit_stuff(subreddit)
    text_to_speech_stuff(reddit_json_blob['sentence_list_full'])
    # print(reddit_json_blob['sentence_list'])
    videostuff(reddit_json_blob)


if __name__ == "__main__":
    main()
