import pandas as pd
import numpy as np
import json
import nfl_data_py as nfl
from matplotlib import pyplot as plt

from simulation import Simulation

class Evaluation:
    def __init__(self, odds_filepath: str, params_filepath: str) -> None:
        self.odds = pd.read_csv(odds_filepath)

        with open(params_filepath) as f:
            self.params = json.load(f)

        self.games = self.get_games()

        self.rng = np.random.default_rng(self.params['random_seed'])

    def get_games(self):
        schedules = nfl.import_schedules(years=[self.params['prediction_year']])[['game_id', 'season', 'week', 'away_team', 'away_score', 'home_team', 'home_score']]
        games = schedules[(schedules['week'] >= self.params['prediction_gameweek_start']) & (schedules['week'] <= self.params['prediction_gameweek_end'])]
        return games

    def predict_games(self):
        predictions = []
        for game in self.games.itertuples():
            prediction = self.predict_game(game[6], game[4])
            prediction['game_id'] = game[1]
            predictions.append(prediction)

        predictions = pd.DataFrame(predictions)
        self.games = pd.merge(self.games, predictions, on='game_id')

    def predict_game(self, home_team, away_team):
        sim = Simulation(
            home_team=home_team,
            away_team=away_team,
            iterations=self.params['iterations'],
            rng = self.rng,
            playcaller_method=self.params['playcaller_method']
        )

        sim.run_simulations()

        results = pd.DataFrame(sim.results)

        if self.params['prediction_method'] == 'median':
            home_score_prediction = results['home_score'].median()
            away_score_prediction = results['away_score'].median()

        return {
            'home_score_prediction': home_score_prediction, 
            'away_score_prediction': away_score_prediction
        }
    
    def evaluate(self):
        self.games['home_residual'] = self.games['home_score'] - self.games['home_score_prediction']
        self.games['away_residual'] = self.games['away_score'] - self.games['away_score_prediction']

    def plot(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(self.games.index, self.games['home_residual'], color='blue', label='Home Residuals')

        # Plot residual for away team
        ax.scatter(self.games.index, self.games['away_residual'], color='red', label='Away Residuals')

        # Add horizontal line at y=0 for reference
        ax.axhline(y=0, color='black', linestyle='--', linewidth=1)

        # Add labels and title
        ax.set_xlabel('Game Index', fontsize=12)
        ax.set_ylabel('Residuals', fontsize=12)
        ax.set_title('Residual Plot: Actual vs Predicted Scores', fontsize=14)

        # Add legend
        ax.legend()

        # Show plot
        plt.tight_layout()
        plt.show()
