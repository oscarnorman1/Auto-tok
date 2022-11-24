import moviepy.editor as mpy

clip = mpy.VideoFileClip("assets/basevideo.mp4")

txt_clip = mpy.TextClip("Sample text", fontsize = 70, color = 'white')
txt_clip = txt_clip.set_position('center').set_duration(10)

video = mpy.CompositeVideoClip([clip, txt_clip])

video.write_videofile("test.mp4")
