import os
from text2Speech import textToSpeech
from Slide import make_slide
from moviepy.editor import *
import json

# f = open('summaries.json')
# print(type(f))
with open('summaries.json') as file:
  data = json.load(file)
img = []

# a = "".join(slide_txts[0])
# voice_over = []

vidClips = []
for i, d in enumerate(data):
    for j, paragraph in enumerate(d['summary_data']):
        img.append(make_slide(str(j), paragraph['bullet points']))
        textToSpeech(paragraph["summary"], j)
        audio = AudioFileClip("audio/" + str(j) + ".mp3")
        clip = ImageClip(img[j]).set_duration(audio.duration)
        clip = clip.set_audio(audio)
        vidClips.append(clip)

video_slides = concatenate_videoclips(vidClips, method='compose')
video_slides.write_videofile("output_video.mp4", fps=12)
