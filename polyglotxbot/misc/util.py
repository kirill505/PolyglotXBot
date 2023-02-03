import json
from googletrans import Translator
from tqdm import tqdm
from youtube_transcript_api import YouTubeTranscriptApi

translator = Translator()


def get_youtube_id(youtube_url: str):
    return youtube_url.split("v=")[-1]


def get_subtitles_list(yt_url: str):
    # assigning srt variable with the list
    # of dictonaries obtained by the get_transcript() function
    youtube_id = get_youtube_id(yt_url)
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
    srt_lst = get_subtitles_list(youtube_link)
    all_words = list(preparate_subtitles_list(srt_lst))
    print(all_words)
    word_list = dict()
    words_i_know = json.load(open(''))
    for lang in tqdm(all_words, desc="Translated word list"):
        if lang not in words_i_know:
            translated = translator.translate(lang, dest='ru')
            print(translated)
            word_list[translated.origin] = translated.text

    save_word_list(word_list, "")


def save_word_list(word_dict, output_file):
    with open(output_file, 'w', encoding='utf8') as outfile:
        json.dump(word_dict, outfile, ensure_ascii=False)
