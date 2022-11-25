import moviepy.editor as mpy
from moviepy.video.compositing.concatenate import concatenate_videoclips

intro = mpy.VideoFileClip("assets/basevideo.mp4").subclip(0, 10)
comment = mpy.VideoFileClip("assets/basevideo.mp4").subclip(0, 10)

intro_txt = mpy.TextClip("Reddit post title", fontsize=40, color='white')
intro_txt = intro_txt.set_position('center').set_duration(5)

comment_txt = mpy.TextClip("Reddit post comments", fontsize=40, color='white')
comment_txt = comment_txt.set_position('center').set_duration(5)

intro_vid = mpy.CompositeVideoClip([intro, intro_txt])
comment_vid = mpy.CompositeVideoClip([comment, comment_txt])

final_clip = concatenate_videoclips([intro_vid, comment_vid])

#final_clip.preview()
final_clip.show(11, interactive=True)

# video.write_videofile("test.mp4")
