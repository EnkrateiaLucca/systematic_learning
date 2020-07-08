import webbrowser
import pandas as pd
import numpy as np
import os
import pathlib
from googlesearch import search
import webbrowser
import pytube
from utils import clip_video
import time
from datetime import datetime


# def google_search_show(query, num_links=5):
#     # Perhaps later will be a return instead of print
#     useful_results = list(search(query, tld="co.in", num=10, stop=num_links, pause=2))
#     return useful_results


def clip_video(video_path, clipped_output_path):
    list_clips = literal_eval(input("Give the time stamps for the clips. ([[begin_1,end_1],[begin_2,end_2]]; format of begin and end -> [min,secs])"))
    clip_video(video_path,clipped_output_path, list_clips)


# def youtube_download(vid_url,download_path=r"C:\Users\lucas\Downloads",test=False):
#     if test:
#         video_url = 'https://www.youtube.com/watch?v=tXOIvjbNhts' # paste here your Youube videos' url
#         youtube = pytube.YouTube(video_url)
#         video = youtube.streams.first()
#         video.download(download_path)
#     else:
#         youtube = pytube.YouTube(vid_url)
#         video = youtube.streams.first()
#         video.download(download_path)

def generate_dataset():
    youtube_search = literal_eval(YoutubeSearch(learn_query, max_results=10).to_json())
    results = ["youtube.com" + item["link"] for item in youtube_search["videos"]]
    google_searche_results = google_search_show(learn_query, num_links=10)

    return results


def set_up_dataset(csv_file="dataset.csv",text_file='dataset.txt'):
    df = pd.read_csv(text_file, sep=" ", header=None)
    df.columns= ["links"]
    cols =  ["attention_level", "session_time","date","session_score"]
    for col in cols:
        df[col] = None
    df["last_index"] = 0
    df.to_csv(csv_file)
    os.remove(text_file)

    return df


def get_date(save_file=False):
    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day
    if save_file:
        return f"{year}_{month}_{day}"
    return f"{year}/{month}/{day}"


if __name__=="__main__":
    #youtube_download(vid_url)
    text_file = r"C:\Users\lucas\Desktop\projects\medium_posts\learning_post\dataset.txt"
    if os.path.isfile(text_file):
        df = set_up_dataset()
    if not os.path.isdir(".\\sessions"):
        os.mkdir(".\\sessions")
    try:
        df = pd.read_csv("dataset.csv")
    except:
        print("Make sure the csv is in the right folder")
    last_index = df["last_index"][0]
    for i,url in enumerate(df["links"][last_index:]):
        webbrowser.open(url)
        start_session = time.time()
        date = get_date()
        df["date"][i] = date
        att_level = input("Input the attention level for this input (b,s-f,f):")
        df["attention_level"][i] = att_level
        next_inp = input("Press enter to go to next link or q to quit training for now")
        if next_inp == "q":
            df["last_index"] = i
            end_session = time.time()
            s_time = np.round(end_session - start_session,2)
            df["session_time"][i] = s_time
            s_score = float(input("Give a score to your performance in this session (0-10):"))
            df["session_score"][i] = s_score
            break
        end_session = time.time()
        s_time = np.round(end_session - start_session,2)
        df["session_time"][i] = s_time
        s_score = float(input("Give a score to your performance in this session (0-10):"))
        df["session_score"][i] = s_score

    session_df = df.copy()
    date_file = get_date(save_file=True)
    session_df.to_csv(".\\sessions\\session_{}.csv".format(date_file))

    duolingo = input("Do you want to do a quick duolingo session to finish things off? (y/n)")
    if duolingo=="y":
        webbrowser.open("www.duolingo.com")
    



    




