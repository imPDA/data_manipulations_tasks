import math
import sqlite3
import pandas as pd
import os
# import datetime as dt

pd.set_option('display.max_column', None)
db = sqlite3.connect(os.environ.get("DB_PATH") or 'database.sqlite')
player_data = pd.read_sql("SELECT * FROM Player;", db)
match_data = pd.read_sql("SELECT * FROM Match;", db)
league_data = pd.read_sql("SELECT * FROM League;", db)
player_attributes_data = pd.read_sql("SELECT * FROM Player_Attributes;", db)
team_data = pd.read_sql("SELECT * FROM Team;", db)


# Country	11	2
# League	11	3
# Match	25979	115
# Player	11060	7
# Player_Attributes	183978	42
# Team	299	5
# Team_Attributes	1458	25


class Tasks:
    def __init__(self):
        self.dict_of_tasks = {num_of_task: f'task_{num_of_task}' for num_of_task in range(1, 16)}

    def run_tasks(self, list_of_tasks: list):
        for task in list_of_tasks:
            try:
                answer = getattr(self, self.dict_of_tasks[task])()
            except AttributeError:
                print(f'Task {task} not implemented yet.')
            else:
                try:
                    if answer:
                        print(f'Answer on Task {task} is {answer}')
                    else:
                        print(f'There is no answer for Task {task}')
                finally:
                    pass
                # except ValueError:
                #     print(f'Answer on Task {task} is {answer.all()}')
                #     pass

    def run_all_tasks(self):
        self.run_tasks(list(range(1, 16)))

    @staticmethod
    def task_1():
        """Task 1 (0.25 point). Calculate the number of players with a height between 180 and 190 inclusive."""

        return len(player_data.query('height >= 180 & height <= 190'))

    @staticmethod
    def task_2():
        """Task 2 (0.25 point). Calculate the number of players born in 1980."""

        return len(player_data[player_data['birthday'].dt.year == 1980])

    @staticmethod
    def task_3():
        """Task 3 (0.25 point). Make a list of the top 10 players with the highest weight sorted in descending order.
        If there are several players with the same weight put them in the lexicographic order by name."""

        return list(player_data.sort_values(by=['weight', 'player_name'], ascending=[False, True])
                    .head(10)
                    .get('player_name')
                    .to_dict().values()
                    )

    @staticmethod
    def task_4():
        """Task 4 (0.5 point). Make a list of tuples containing years along with the number of players born in that year
        from 1980 up to 1990. Structure example: [(1980, 123), (1981, 140) ..., (1990, 83)] -> There were born 123
        players in 1980, there were born 140 players in 1981 etc."""

        return sorted([(k, v) for k, v in player_data.query('birthday.dt.year >= 1980 & birthday.dt.year <= 1990')
                      .sort_values(by='birthday')['birthday']
                      .dt.year
                      .value_counts()
                      .to_dict().items()],
                      key=lambda x: x[0]
                      )

    @staticmethod
    def task_5():
        """Task 5 (0.5 point). Calculate the mean and the standard deviation of the players' height with the name
        Adriano.

        Note: Name is represented by the first part of player_name."""

        return {'Mean': player_data[player_data['player_name'].str.contains("Adriano")].get('height').mean(),
                'STD': player_data[player_data['player_name'].str.contains("Adriano")].get('height').std(),
                }

    @staticmethod
    def task_6():
        """Task 6 (0.75 point). How many players were born on each day of the week? Find the day of the week with the
        minimum number of players born."""

        return min(player_data['birthday'].dt.weekday.value_counts().to_dict().items(), key=lambda x: x[1])

    @staticmethod
    def task_7():
        """Task 7 (0.75 point). Find a league with the most matches in total. If there are several leagues with the
        same amount of matches, take the first in the lexical order."""

        return sorted([(league_data.loc[league_data['id'] == k]['name'].to_string(index=False), v) for
                       k, v in match_data['league_id'].value_counts().to_dict().items()],
                      key=lambda x: (-x[1], x[0])
                      )[0]

    @staticmethod
    def task_8():
        """Task 8 (1.25 point). Find a player who participated in the largest number of matches during the whole match
        history. Assign a player_name to the given variable."""

        return max(pd.melt(match_data,  # TODO: Could I use smth instead of 'melt'?
                           id_vars=['id'],
                           value_vars=['home_player_1', 'home_player_2', 'home_player_3', 'home_player_4',
                                       'home_player_5', 'home_player_6', 'home_player_7', 'home_player_8',
                                       'home_player_9', 'home_player_10', 'home_player_11',
                                       'away_player_1', 'away_player_2', 'away_player_3', 'away_player_4',
                                       'away_player_5', 'away_player_6', 'away_player_7', 'away_player_8',
                                       'away_player_9', 'away_player_10', 'away_player_11',
                                       ]
                           ).get('value').value_counts().to_dict().items(),
                   key=lambda x: x[1]
                   )

    @staticmethod
    def task_9():
        """Task 9 (1.5 point). List top-5 tuples of most correlated player's characteristics in the descending order
        of the absolute Pearson's coefficient value.

        Note 1: Players characteristics are all the columns in Player_Attributes table except [id, player_fifa_api_id,
        player_api_id, date, preferred_foot, attacking_work_rate, defensive_work_rate].
        Note 2: Exclude duplicated pairs from the list. E.g. ('gk_handling', 'gk_reflexes') and
        ('gk_reflexes', 'gk_handling') are duplicates, leave just one of them in the resulting list.

        Hint: You may use dataframe.corr() for calculating pairwise Pearson correlation."""

        return [(tuple(a), b) for a, b in sorted(list({frozenset(k): v for k, v in player_attributes_data
                                                      .drop(labels=['id', 'player_fifa_api_id', 'player_api_id', 'date',
                                                                    'preferred_foot', 'attacking_work_rate',
                                                                    'defensive_work_rate'
                                                                    ],
                                                            axis='columns'
                                                            )
                                                      .corr()
                                                      .unstack()
                                                      .to_dict().items() if len(frozenset(k)) > 1
                                                       }.items()
                                                      ),
                                                 key=lambda x: -x[1]
                                                 )[:5]
                ]

    @staticmethod
    def task_10():
        """Task 10 (2 points). Find top-5 most similar players to Neymar whose names are given. The similarity is
        measured as Euclidean distance between vectors of players' characteristics (described in the task above).
        Put their names in a vector in ascending order by Euclidean distance and sorted by player_name if the distance
        is the same.

        Note 1: There are many records for some players in the Player_Attributes table. You need to take the freshest
        data (characteristics with the most recent date).
        Note 2: Use pure values of the characteristics even if you are aware of such preprocessing technics as
        normalization.
        Note 3: Please avoid using any built-in methods for calculating the Euclidean distance between vectors, think
        about implementing your own."""

        #  TODO: Are there other solutions?

        def calculate_euclidean_distance_between_players(a, b):
            return math.sqrt(sum([(float(a) - float(b)) * (float(a) - float(b)) for a, b in zip(a, b)]))

        player_attributes_fresh_data = player_attributes_data.groupby(['player_api_id'])\
            .apply(lambda x: x.sort_values(by='date', ascending=False).head(1))

        neymar_id = int(player_data.loc[player_data['player_name'] == 'Neymar']['player_api_id'].to_string(index=False))
        neymar_attributes = player_attributes_fresh_data\
            .loc[player_attributes_fresh_data['player_api_id'] == neymar_id]\
            .drop(labels=['id', 'player_fifa_api_id', 'player_api_id', 'date',
                          'preferred_foot', 'attacking_work_rate',
                          'defensive_work_rate'],
                  axis='columns') \
            .squeeze()

        for index, row in player_attributes_fresh_data.drop(labels=['id', 'player_fifa_api_id', 'player_api_id', 'date',
                                                                    'preferred_foot', 'attacking_work_rate',
                                                                    'defensive_work_rate'],
                                                            axis='columns').iterrows():
            player_attributes_fresh_data.at[index, 'neymar_difference'] = \
                calculate_euclidean_distance_between_players(neymar_attributes, row)

        #  TODO: Rewrite whole Task.
        return player_attributes_fresh_data.sort_values(by='neymar_difference', ascending=True)\
            .head(6).tail(5)['neymar_difference'].to_dict()

    @staticmethod
    def task_11():
        """Task 11 (1 point). Calculate the number of home matches played by the Borussia Dortmund team in Germany 1.
        Bundesliga in season 2008/2009"""

        home_team_api_id = int(team_data.loc[team_data['team_long_name'] == "Borussia Dortmund"]['team_api_id']
                               .to_string(index=False))
        league_id = int(league_data.loc[league_data['name'] == "Germany 1. Bundesliga"]['id'].to_string(index=False))
        season = "2008/2009"

        return len(match_data.query(f'home_team_api_id == {home_team_api_id} & '
                                    f'league_id == {league_id} & '
                                    f'season == "{season}"'
                                    ).index
                   )


if __name__ == '__main__':
    player_data['birthday'] = pd.to_datetime(player_data['birthday'])

    my_tasks = Tasks()
    my_tasks.run_all_tasks()
