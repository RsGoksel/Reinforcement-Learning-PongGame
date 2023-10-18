import gym
from gym import spaces

from pygame.locals import *

import pygame
import random
import numpy as np
import os
import Constants
from Agent import Paddle

WIDTH = Constants.WIDTH
HEIGHT = Constants.HEIGHT

MIDDLE = Constants.PADDLE_HEIGHT * 0.5 # Middle of paddle, or which area you want to focus and train for

black = (0,0,0)
red = (255,0,0)
blue = (50,0,200)

BALL_Xspeed = Constants.BALL_Xspeed
BALL_Yspeed = Constants.BALL_Yspeed

class PongEnv(gym.Env):
  
    class Ball(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([WIDTH*0.01,WIDTH*0.01])
            self.image.fill(red)
            self.rect = self.image.get_rect()
            self.Xspeed = BALL_Xspeed
            self.Yspeed = BALL_Yspeed
        
        #Restrict the Ball within screen boundries and reflect it 
        def clip(self):
            
                # WIDTH*0.01 is size of the ball. Checking if ball in boundries
            if self.rect.y > HEIGHT - WIDTH*0.01 or self.rect.y < WIDTH*0.01: 
                 self.Yspeed *= -1
        
            if self.rect.x <= WIDTH*0.01 or self.rect.x >= WIDTH - WIDTH*0.01:  #  self.rect.x >= WIDTH*0.99  
                return True
            
            
    def __init__(self):
         
        super(PongEnv, self).__init__()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.init()
        
        self.reward = 0
        self.done = False
        
        self.action_space = spaces.Discrete(3) # Up, hold, down
        self.observation_space = spaces.Box(low=-1, high=1,
                                            shape=(6,), dtype=np.float32)
        """
        observation_space:
            Euclidean_distance_Agent-bal
            Agent_Y_Coord
            Agent_X_Coord
            Ball_Y_Coord
            Ball_X_Coord
            Ball_Velocity 
        """
        self.Agent = Paddle("Blue")
        self.Bot = Paddle("Red")
        
        self.BALL = self.Ball() #fix this
        
        # Getting the current_distance Initially
        self.current_distance = self.Distance_Between_Paddle_Ball()
    
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.Agent, self.Bot, self.BALL)
        
        self.info = {}
        self.reset()
        
    def step(self, action):
        
        """
        Action:
            0: Rise up
            1: Hold
            2: get down
        """
        self.render()
        self.reward = 0
        
        self.Agent.Move(action)

            # Move the ball
        self.BALL.rect.x += self.BALL.Xspeed
        self.BALL.rect.y += self.BALL.Yspeed 

            # The bot will track the ball's exact position.
        self.Bot.rect.y = self.BALL.rect.y - WIDTH*0.02

            # Reflect the ball if touches to Bot paddle
        if self.Bot.rect.colliderect(self.BALL.rect):
            self.BALL.Xspeed *= -1
        
            # Check if the ball makes contact with any of the four flanks
        if self.BALL.clip():
            
            self.done = True
            self.reward -= 30
            return self.observation, self.reward, self.done, self.info

            # Reflecting the ball upon contact with the paddle
        if self.Agent.rect.colliderect(self.BALL.rect): 
            self.BALL.Xspeed *= -1
            self.reward += 30

            # Giving the Score if the distance between ball and paddle is less than Ball's size
        if self.Distance_Between_Paddle_Ball() < self.current_distance:
            self.reward += 0.1
       
            
            # +Score if Ball between middle of Agent paddle
        if self.Agent.rect.bottom > self.BALL.rect.y > self.Agent.rect.y:
            self.reward += 1
            #if self.BALL.rect.top - paddle_Y/2 >= self.Agent.rect.top 
        
        """
        #Agressive Learning
        # Giving No score and finish the round if the ball gets away
        if self.BALL.Xspeed < 0 and self.Distance_Between_Paddle_Ball() > self.current_distance:
            self.reward = 0
            self.done = True
            
        """

            #Update current distance between paddle and the ball
        self.current_distance = self.Distance_Between_Paddle_Ball()

            #Update observation 
        self.observation = self.get_observation()

        return self.observation, self.reward, self.done, self.info        
        
        
    def reset(self):
        
        self.done = False
        self.reward = 0
        
        self.Agent.rect.x = WIDTH*0.02
        self.Agent.rect.y = random.randint(0,HEIGHT/10)*10 
        
        self.Bot.rect.x = WIDTH*0.95 
        self.Bot.rect.y =  random.randint(0,HEIGHT/10)*10
        
        self.BALL.rect.x = WIDTH*0.5
        self.BALL.rect.y = HEIGHT*0.25 + random.randint(0, int(HEIGHT*0.4))
        
        self.BALL.Xspeed = random.sample([-self.BALL.Xspeed,self.BALL.Xspeed],1)[0]
        self.BALL.Yspeed = random.sample([-self.BALL.Yspeed,self.BALL.Yspeed],1)[0]
        
        self.current_distance = self.Distance_Between_Paddle_Ball()
        
        return self.get_observation()
       
    def render(self):
        
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            
        pygame.display.update()
        #pygame.time.delay(15)
        
    def get_observation(self):
        
        return np.array([
                      self.current_distance, 
                      self.Agent.rect.y, 
                      self.BALL.rect.x, 
                      self.BALL.rect.y, 
                      self.BALL.Xspeed, 
                      self.BALL.Yspeed])
    
        
    def Distance_Between_Paddle_Ball(self):
        return np.linalg.norm(np.array([self.Agent.rect.x, self.Agent.rect.y + MIDDLE]) - np.array([self.BALL.rect.x,self.BALL.rect.y]))
  
    def close (self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()

