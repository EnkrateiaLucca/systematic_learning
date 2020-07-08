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



def generate_dataset():
    youtube_search = literal_eval(YoutubeSearch(learn_query, max_results=10).to_json())
    results = ["youtube.com" + item["link"] for item in youtube_search["videos"]]
    google_searche_results = google_search_show(learn_query, num_links=10)

    return results, google_searche_results


def set_up_dataset(csv_file="dataset.csv",text_file='dataset.txt'):
    """
    Creates a Dataframe from a text file with urls. 
    The columns are: 
    attention_level -> input a number representing how much attention the user will give to that source
    session_time -> How long it took to finish studying that source
    date -> The date of this session
    session_score -> The subjective score the user gives to its own performance on that content.
    """
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
    text_file = "./dataset.txt" # This is the .txt file with the relevant links (should be adapted to each user).
    if os.path.isfile(text_file): # Checking if the txt files exists
        df = set_up_dataset() # If there is a text file it will set up the new dataset as a .csv file
    if not os.path.isdir(".\\sessions"):
        os.mkdir(".\\sessions") # Creates a directory to store the data for each session
    try:
        df = pd.read_csv("dataset.csv")
    except:
        print("Make sure the csv is in the right folder")
    last_index = df["last_index"][0]
    for i,url in enumerate(df["links"][last_index:]): # Looping over the links
        webbrowser.open(url) # Opens each link on the default browser 
        start_session = time.time() 
        date = get_date()
        df["date"][i] = date # Stores the date
        att_level = float(input("Input the attention level for this input (0-10):")) # Requests a score of attention 
        df["attention_level"][i] = att_level
        next_inp = input("Press enter to go to next link or q to quit training for now") # To go to the next link
        if next_inp == "q":
            df["last_index"] = i
            end_session = time.time()
            s_time = np.round(end_session - start_session,2)
            df["session_time"][i] = s_time
            s_score = float(input("Give a score to your performance in this session (0-10):"))
            df["session_score"][i] = s_score
            break
        end_session = time.time()
        s_time = np.round(end_session - start_session,2) # Records the time of that session
        df["session_time"][i] = s_time
        s_score = float(input("Give a score to your performance in this session (0-10):")) # Requests the score for performance
        df["session_score"][i] = s_score

    session_df = df.copy()
    date_file = get_date(save_file=True)
    session_df.to_csv(".\\sessions\\session_{}.csv".format(date_file)) # Stores the .csv for that session on the sessions directory

    duolingo = input("Do you want to do a quick duolingo session to finish things off? (y/n)") # Finishes prompting the user to do a quick duolingo session to wrap things up  
    if duolingo=="y":
        webbrowser.open("www.duolingo.com")
    



    




