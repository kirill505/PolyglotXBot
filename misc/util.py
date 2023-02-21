import json
from googletrans import Translator
from tqdm import tqdm
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

translator = Translator()


def get_youtube_id(youtube_url: str):
    return youtube_url.split("v=")[-1]


def get_subtitles_list(youtube_id: str):
    srt = YouTubeTranscriptApi.get_transcript(youtube_id, languages=['en'])
    return srt


def preparate_subtitles_list(subtitles):
    word_list = set()
    for sub in subtitles:
        if sub["text"] != '[Music]':
            for word in sub["text"].split():
                if word not in word_list:
                    word_list.add(word)
    return word_list


def get_translated_word_list(youtube_link):
    youtube_id = get_youtube_id(youtube_link)
    srt_lst = get_subtitles_list(youtube_id)
    if srt_lst:
        all_words = list(preparate_subtitles_list(srt_lst))
        word_list = dict()
        yt = YouTube(youtube_link)
        for lang in tqdm(all_words[:20], desc="Translated word list"):
            translated = translator.translate(lang, dest='ru')

            word_list[translated.origin] = translated.text
        return yt.streams[0].title, youtube_id, word_list
