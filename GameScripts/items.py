import pygame
import random


class Items:
    def __init__(self):
        self.random_choices = ["ammo", "health_potion", "life", "spider", "empty"] 
        self.reward = None
    
    def box_reward(self, player, reward):
        if reward == "ammo":
            player.ammo += 10
        elif reward == "life":
            player.life += 1
        elif reward == "health_potion":
            pass
        elif reward == "spider":
            pass


    def box_opened(self, player):
        self.reward = random.choice(self.random_choices)
        self.box_reward(player, self.reward)
