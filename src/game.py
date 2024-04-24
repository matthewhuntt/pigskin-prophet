import pandas as pd
import numpy as np

class Game:
    def __init__(self, home_team, away_team, rng, time_remaining=3600, home_score=0, away_score=0):
        """creates a Game object

        Args:
            home_team (str): home team
            away_team (str): away team
            time_remaining (int, optional): time remaining in seconds. Defaults to 3600.
            home_score (int, optional): starting home score. Defaults to 0.
            away_score (int, optional): starting away score. Defaults to 0.
        """
        self.home_team = home_team
        self.away_team = away_team
        self.rng = rng
        self.time_remaining = time_remaining
        self.home_score = home_score
        self.away_score = away_score
        self.pos_team = None
        self.down = None
        self.yards_to_go = None
        self.field_position = None

    def start_game(self):
        """sets game state to typical starting conditions
        """
        self.pos_team = self.home_team
        self.down = 1
        self.yards_to_go = 10
        self.field_position = 25

    def run_play(self, yards_gained: int, time: int):
        """updates game state based on play result

        Args:
            yards_gained (int): yards gained on the play
            time (int): time taken by the play
        """
        # Update down and ydstogo
        if self.down == 4 and self.yards_to_go > yards_gained:
            self.turnover()
        elif self.yards_to_go <= yards_gained:
            self.down = 1
            self.yards_to_go = 10
        else:
            self.down += 1
            self.yards_to_go -= yards_gained
        
        # Update field position
        self.field_position += yards_gained
        
        if self.field_position >= 100:
            self.score_touchdown(self.pos_team)
        elif self.field_position <= 0:
            self.turnover()

        # decrement time remaining
        self.time_remaining -= time
        
    def turnover(self):
        """changes game state to record a change in posession
        """
        if self.pos_team == self.home_team:
            self.pos_team = self.away_team
        else:
            self.pos_team = self.home_team
        
        self.down = 1
        self.yards_to_go = 10
        self.field_position = 100 - self.field_position

    def score_touchdown(self, team):
        """changes game state to record a touchdown

        Args:
            team (str): scoring team
        """
        pat = self.rng.random() < .95
        if team == self.home_team:
            self.home_score += (6 + pat)
        elif team == self.away_team:
            self.away_score += (6 + pat)
        self.kickoff()

    def score_field_goal(self, team):
        """changes game state to record a field goal

        Args:
            team (str): scoring team
        """
        if team == self.home_team:
            self.home_score += 3
        elif team == self.away_team:
            self.away_score += 3

    def kickoff(self):
        """changes game state to reset conditions after a score
        """
        if self.pos_team == self.home_team:
            self.pos_team = self.away_team
        else:
            self.pos_team = self.home_team
        self.down = 1
        self.yards_to_go = 10
        self.field_position = 25

    def get_game_state(self):
        """returns all game attributes as a dictionary

        Returns:
            dict: dictionary containing all game attributes
        """
        return {
            "time_remaining": self.time_remaining,
            "home_team": self.home_team,
            "home_score": self.home_score,
            "away_team": self.away_team,
            "away_score": self.away_score,
            "possession": self.pos_team,
            "down": self.down,
            "yards_to_go": self.yards_to_go,
            "field_position": self.field_position
        }

    def print_game_state(self):
        print("Time Remaining:", self.time_remaining)
        print("Home Team:", self.home_team, "Score:", self.home_score)
        print("Away Team:", self.away_team, "Score:", self.away_score)
        print("Possession:", self.pos_team)
        print("Down:", self.down)
        print("Yards to Go:", self.yards_to_go)
        print("Field Position:", self.field_position)
