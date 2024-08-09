import pandas as pd
import os

def load_user_data(username):
    filename = f"{username}_transactions.csv"
    if os.path.exists(filename):
        return pd.read_csv(filename)
    else:
        return pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount'])

def save_user_data(username, df):
    filename = f"{username}_transactions.csv"
    df.to_csv(filename, index=False)
