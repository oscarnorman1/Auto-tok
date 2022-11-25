import moviepy.editor as mpy
from moviepy.video.compositing.concatenate import concatenate_videoclips
from selenium import webdriver
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
    element_post.screenshot('results/postTitle.png')
    fox.quit()


def videostuff(json_blob):
    intro = mpy.VideoFileClip("assets/basevideo.mp4").subclip(0, 5)
    comment = mpy.VideoFileClip("assets/basevideo.mp4").subclip(0, 5)

    intro_txt = mpy.TextClip(json_blob['title'], fontsize=40, color='white')
    intro_txt = intro_txt.set_position('center').set_duration(5)

    comment_txt = mpy.TextClip(json_blob['content'], fontsize=10, color='white')
    comment_txt = comment_txt.set_position('center').set_duration(5)

    intro_vid = mpy.CompositeVideoClip([intro, intro_txt])
    comment_vid = mpy.CompositeVideoClip([comment, comment_txt])

    final_clip = concatenate_videoclips([intro_vid, comment_vid])

    # final_clip.preview()
    final_clip.show(7, interactive=True)
    # final_clip.write_videofile("test.mp4")


def fetch_reddit_stuff(subreddit):
    reddit = r.return_instance()
    blob = json.loads(r.return_blob(subreddit, reddit))
    #print(blob['title'])
    #print(blob['ups'])
    #print(blob['sentance_list'])
    return blob


def main():
    # subreddit = subredditlist.getRandomSub()
    subreddit = 'TalesFromRetail'
    #seleniumstuff(subreddit)
    reddit_json_blob = fetch_reddit_stuff(subreddit)
    print(len(reddit_json_blob['sentance_list']))
    #videostuff(reddit_json_blob)


if __name__ == "__main__":
    main()
