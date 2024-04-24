import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from game import Game
from playcaller import Playcaller

class Simulation:
    def __init__(self, home_team, away_team, iterations: int, rng, playcaller_method: str) -> None:
        """creates a simulation object

        Args:
            home_team (str): home team
            away_team (str): away team
            iterations (int): number of games to simulate
            random_seed (int): seed for random generator
        """
        self.home_team = home_team
        self.away_team = away_team
        self.iterations = iterations
        self.rng = rng
        self.playcaller_method = playcaller_method
        self.results = []

    def run_simulations(self):
        """simulates i games and adds results to list
        """
        for i in range(self.iterations):
            game = Game(self.home_team, self.away_team, rng=self.rng)
            game.start_game()
            playcaller = Playcaller(game_state=game.get_game_state(), rng=self.rng, method=self.playcaller_method)
            while game.time_remaining > 0:
                playcaller.game_state = game.get_game_state()
                game.run_play(yards_gained=playcaller.get_outcome(), time=20)
            
            self.results.append({
                'home_score': game.home_score,
                'away_score': game.away_score
            })
            
