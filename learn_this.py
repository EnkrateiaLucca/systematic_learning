from datetime import datetime
import os
import time
import webbrowser

import numpy as np
import pandas as pd


def set_up_dataset(csv_file="dataset.csv", text_file='dataset.txt'):
    """Creates a CSV file with the attention_level, session_time, date, and
    session_score for each link within the given text file.

    The columns are:
        attention_level -> input a number representing how much attention the
                           user will give to that source
        session_time -> How long it took to finish studying that source
        date -> The date of this session
        session_score -> The subjective score the user gives to its own
                         performance on that content.

    Args:
        csv_file (str): Path to the CSV file to parse
        text_file (str): Path to the text file to remove

    Return:
        dataframe created from the CSV file
    """
    df = pd.read_csv(text_file, sep=" ", header=None)
    df.columns= ["links"]
    cols =  ["attention_level", "session_time", "date", "session_score"]
    for col in cols:
        df[col] = None
    df["last_index"] = 0
    df.to_csv(csv_file)
    os.remove(text_file)
    return df


def get_date(save_file=False):
    """Get the date formatted either for a filename or for a column in the"""
    today = datetime.now()
    year = today.year
    month = today.month
    day = today.day
    if save_file:
        return f"{year}_{month}_{day}"
    return f"{year}/{month}/{day}"


if __name__ == "__main__":
    # .txt with relevant links
    text_file = "./dataset.txt"
    # Check if the .txt file exists
    if os.path.isfile(text_file):
        # If so, set up the new dataset as a .csv file
        df = set_up_dataset()
    # Create a session directory if there isn't one already
    if not os.path.isdir(".\\sessions"):
        os.mkdir(".\\sessions")

    # Try to read in the CSV file
    try:
        df = pd.read_csv("dataset.csv")
    except:
        print("Make sure the csv is in the right folder")

    # Start looping through the links, beginning at the last index
    last_index = df["last_index"][0]
    for i, url in enumerate(df["links"][last_index:]):
        # Open the link in the default browser
        webbrowser.open(url)
        # Get the start time and date
        start_session = time.time()
        date = get_date()
        df["date"][i] = date

        # When the user is finished, get their attention level
        attention_prompt = "Input the attention level for this input (0-10):"
        att_level = float(input(attention_prompt))
        df["attention_level"][i] = att_level

        # See if they want to continue
        perf_prompt = "Score your performance in this session (0-10):"
        continue_prompt = "Press enter to go to next link or q to quit"
        next_inp = input()
        if next_inp == "q":
            # Save off the last index, so we can pick up where we left off
            df["last_index"] = i
            end_session = time.time()
            s_time = np.round(end_session - start_session, 2)
            df["session_time"][i] = s_time
            s_score = float(input(perf_prompt))
            df["session_score"][i] = s_score
            break
        end_session = time.time()
        s_time = np.round(end_session - start_session, 2)
        df["session_time"][i] = s_time
        s_score = float(input(perf_prompt))
        df["session_score"][i] = s_score

    session_df = df.copy()
    date_file = get_date(save_file=True)
    session_df.to_csv(".\\sessions\\session_{}.csv".format(date_file))

    duolingo_prompt = "Do you want to do a quick duolingo session? (y/n)"
    duolingo = input(duolingo_prompt)
    if duolingo == "y":
        webbrowser.open("www.duolingo.com")
