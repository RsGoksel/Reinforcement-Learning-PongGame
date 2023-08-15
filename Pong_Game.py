import gym
from gym import spaces

from pygame.locals import *

import pygame
import random
import numpy as np

import os
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy


HEIGHT = 450 
WIDTH = 600

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (50,0,200)

MOVE_COEF = 4

def updatePaddle(action, paddleY):
    
        if action == 0:
            paddleY.rect.y -= MOVE_COEF

        #if action == 1:
        #    paddleY.rect.y = paddleY.rect.y

        if action == 2:
            paddleY.rect.y += MOVE_COEF

        #Keep the paddle in boundries
        if paddleY.rect.y < 0:  
            paddleY.rect.y = 0

        if paddleY.rect.y > HEIGHT*0.8: #Paddle height is game_height/5. So we keepin' it in boundries
            paddleY.rect.y = HEIGHT*0.8 

        return paddleY.rect.y

class PongEnv(gym.Env):
  
    metadata = {'render.modes': ['human']}
    
    class paddle(pygame.sprite.Sprite):
        def __init__(self,color):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([WIDTH*0.02,HEIGHT*0.2]) #Constant values for their ratio
            self.image.fill(color)
            self.rect = self.image.get_rect()
           
    class ball(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([WIDTH*0.02,WIDTH*0.02])
            self.image.fill(red)
            self.rect = self.image.get_rect()
            self.Xspeed = 3
            self.Yspeed = 3
    
    def __init__(self):
         
        super(PongEnv, self).__init__()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.init()
        
        self.myfont = pygame.font.SysFont("monospace", 16)
        
        self.reward = 0
        self.done = False
        self.score = 0
        
        self.action_space = spaces.Discrete(3) # Up, hold, down
        #self.action_space.dtype = np.int8 
        
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                            shape=(6,), dtype=np.float32)
        #observation space will 
        # distance between paddle and ball, agnet's Y coordinate, Agent's X coordinate, Ball's Y coordinate, Ball's X coordinate, Ball's velocity] 
        
        self.maxSkor = 0
        self.rekor = 0
        
        self.scoretext = self.myfont.render("Score = "+str(self.rekor), 1, (0,0,0))
        
        self.pedal1 = self.paddle(blue)
        self.pedal2 = self.paddle(blue)
        
        self.BALL = self.ball()
        
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.pedal1, self.pedal2, self.BALL)
        
        self.pedal1.rect.x = WIDTH*0.02
        self.pedal1.rect.y = random.randint(0,HEIGHT/10)*10 #300
        
        self.pedal2.rect.x = 575
        self.pedal2.rect.y = random.randint(0,HEIGHT*0.1)*10
        
        self.BALL.rect.x = WIDTH/2
        self.BALL.rect.y = HEIGHT/5 + random.randint(0, int(3/4*HEIGHT))
        
        self.BALL.Xspeed = random.sample([-self.BALL.Xspeed,self.BALL.Xspeed],1)[0]
        self.BALL.Yspeed = random.sample([-self.BALL.Yspeed,self.BALL.Yspeed],1)[0]
        
        #First difference between ball and our agent
        self.fark = np.linalg.norm
        (np.array([self.pedal1.rect.x,self.pedal1.rect.y]) - np.array([self.BALL.rect.x,self.BALL.rect.y]))
        
    def step(self, action):
        
        # Ball has to move in every step   
        self.BALL.rect.x += self.BALL.Xspeed
        self.BALL.rect.y += self.BALL.Yspeed 
        
        self.pedal2.rect.y = self.BALL.rect.y - (WIDTH*0.025) #Our agent will train "bot paddle" which follow the ball automatically
        
        # if action = 0, up
        # if action = 1, hold paddle
        # if action = 2, pull down paddle
        
        if action==0:
            updatePaddle(0, self.pedal1)
        
        if action==1:
            updatePaddle(1, self.pedal1)
            
        if action==2:
            updatePaddle(2, self.pedal1)
        
        
        if self.BALL.rect.y > HEIGHT - (WIDTH*0.025) or self.BALL.rect.y < WIDTH*0.005: #keep ball within boundries and reflect it 
             self.BALL.Yspeed *= -1
                
        if self.pedal1.rect.colliderect(self.BALL.rect): #If the ball touch the our paddle, than score will increase and the ball will reflect  
            self.BALL.Xspeed *= -1
            self.rekor += 1
            
        if self.pedal2.rect.colliderect(self.BALL.rect):
            self.BALL.Xspeed *= -1 
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            
        pygame.display.update()

        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        
        if self.BALL.rect.x <= WIDTH*0.0083 and self.BALL.rect.x >= WIDTH*0.0083 - WIDTH*0.02:    
            self.done = True #If ball is not in boundries, than round is "Done"


        #If the distance between ball and paddle is less than 6, than +score
        if np.linalg.norm(np.array([self.pedal1.rect.x,self.pedal1.rect.y]) - np.array([self.BALL.rect.x,self.BALL.rect.y])) < 6:
            self.score += 10

        # If our agent and ball's distance is grater than difference of previous move's value and + 10, than  it's round over.
        if np.linalg.norm(np.array([self.pedal1.rect.x,self.pedal1.rect.y]) - np.array([self.BALL.rect.x,self.BALL.rect.y])) > self.fark + 10:
            self.done = True
            self.score = 0
        
        self.reward += self.score
        
        #Update the diffference
        self.fark = np.linalg.norm(np.array([self.pedal1.rect.x,self.pedal1.rect.y]) - np.array([self.BALL.rect.x,self.BALL.rect.y]))

        #Update observation
        self.observation = [self.fark, self.pedal1.rect.y, self.BALL.rect.x, self.BALL.rect.y, self.BALL.Xspeed, self.BALL.Yspeed] 
        self.observation = np.array(self.observation)
        
        
        pygame.time.delay(3)
        
        self.scoretext = self.myfont.render("Score = "+str(self.rekor), 1, (0,0,0))
        self.screen.blit(self.scoretext, (5, 10))
       
        info = {}
        return self.observation, self.reward, self.done, info        
        
        
    def reset(self):

        #Update all essential variables
        
        self.done = False
        self.score = 0
        self.reward = 0
        
        self.pedal1.rect.x = WIDTH*0.02
        self.pedal1.rect.y = random.randint(0,HEIGHT/10)*10 
        
        
        self.pedal2.rect.x = WIDTH*0.95 
        self.pedal2.rect.y =  random.randint(0,HEIGHT/10)*10
        
        
        self.BALL.rect.x = WIDTH*0.5
        self.BALL.rect.y = HEIGHT*0.25 + random.randint(0, int(HEIGHT*0.4))
        
        self.BALL.Xspeed = random.sample([-self.BALL.Xspeed,self.BALL.Xspeed],1)[0]
        self.BALL.Yspeed = random.sample([-self.BALL.Yspeed,self.BALL.Yspeed],1)[0]
        
        self.fark = np.linalg.norm(np.array([self.pedal1.rect.x,self.pedal1.rect.y]) - np.array([self.BALL.rect.x,self.BALL.rect.y]))
        
        self.observation = [self.fark, self.pedal1.rect.y, self.BALL.rect.x, self.BALL.rect.y, self.BALL.Xspeed, self.BALL.Yspeed]  
        self.observation = np.array(self.observation)
        
        return self.observation  
       
    def render(self):
        pass
  
    def close (self):
        if self.screen is not None:
            pygame.display.quit()
            pygame.quit()


env = PongEnv()
PPO_Path = os.path.join('Training/Beast') #or 'Training/Beast'
#log_path = os.path.join('Training','Logs')

model = PPO.load(PPO_Path,env=env)#,tensorboard_log=log_path)

try:
    evaluate_policy(model,env,n_eval_episodes=100,render = True)
except:
    env.close()
    