import sqlite3
import pandas as pd
import os
import datetime as dt

pd.set_option('display.max_column', None)
db = sqlite3.connect(os.environ.get("DB_PATH") or 'database.sqlite')
player_data = pd.read_sql("SELECT * FROM Player;", db)


if __name__ == '__main__':
    print(player_data)
    pattern = 'Task {task}, answer: {answer}'

    # Task 1 (0.25 point). Calculate the number of players with a height between 180 and 190 inclusive
    print(pattern.format(
        task=1,
        answer=len(player_data.query('height >= 180 & height <= 190')),
    ))

    # Task 2 (0.25 point). Calculate the number of players born in 1980
    player_data['birthday'] = pd.to_datetime(player_data['birthday'])
    print(pattern.format(
        task=2,
        answer=player_data[player_data['birthday'].dt.year == 1980],
    ))

    # Task 3
    # print(pattern.format(
    #     task=1,
    #     answer=len(player_data.query('height >= 180 & height <= 190'))
    # ))
