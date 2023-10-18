from Env import PongEnv
import pygame

env = PongEnv()

episode = 10
level = 0

for i in range(1, episode):
    state = env.reset()
    done = False
    score = 0
    
    while not done:
    
        env.render()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
        
    print('Episode: {} Score:{:.2f}'.format(i, score))

pygame.display.quit()
pygame.quit()