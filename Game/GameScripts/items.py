import pygame
import random


class Items:
    def __init__(self):
        self.random_choices = ["ammo", "x2", "life", "x4", "empty", "x1"] 
        self.reward = None
        
    
    def box_reward(self, player, reward):
        if reward == "ammo":
            player.ammo += 10
        elif reward == "life":
            player.lifeline.gain()
        elif reward == "x2":
            player.multiplier = 2
        elif reward == "x4":
            player.multiplier = 4
        elif reward == "x1":
            player.multiplier = 1

    def box_opened(self, player):
        self.reward = random.choice(self.random_choices)
        self.box_reward(player, self.reward)
        print(f"Reward: {self.reward}, lives: {player.lifeline.lives}")
    
    
