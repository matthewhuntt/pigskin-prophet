import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import joblib

class Playcaller:
    def __init__(self, game_state, rng, method) -> None:
        self.game_state = game_state
        self.rng = rng
        self.method = method

        self.nn = load_model('../Data/playcaller_nn.keras')
        self.preprocessor = joblib.load('../Data/playcaller_preprocessor.pkl')

    def call_play(self):
        """placeholder; we'll use this to determine, based on game state, what play is called
        """
        pass

    def get_outcome(self) -> int:
        """placeholder; we'll use this to determine, based on the play called, what the outcome should be

        Returns:
            int: yards gained
        """
        if self.method == 'random':
            play = self.call_play()
            yards_gained = int(self.rng.normal(loc=3.945493, scale=7.746565))
            return yards_gained
        
        if self.method == 'nn':
            return int(self.nn.predict(self.preprocesses()))

    def preprocesses(self):
        preprocessed_state = {}

        preprocessed_state['down'] = self.game_state['down']
        preprocessed_state['posteam'] = self.game_state['possession']
        preprocessed_state['defteam'] = self.game_state['home_team'] if self.game_state['possession'] == self.game_state['away_team'] else self.game_state['away_team']
        preprocessed_state['home_team'] = self.game_state['home_team']
        preprocessed_state['away_team'] = self.game_state['away_team']
        preprocessed_state['game_seconds_remaining'] = self.game_state['time_remaining']
        preprocessed_state['ydstogo'] = self.game_state['yards_to_go']
        preprocessed_state['yardline_100'] = self.game_state['field_position']
        preprocessed_state['posteam_score'] = self.game_state['home_score'] if self.game_state['possession'] == self.game_state['home_team'] else self.game_state['away_score']
        preprocessed_state['defteam_score'] = self.game_state['home_score'] if self.game_state['possession'] == self.game_state['away_team'] else self.game_state['away_score']
        
        return self.preprocessor.transform(pd.DataFrame(preprocessed_state, index=[0]))