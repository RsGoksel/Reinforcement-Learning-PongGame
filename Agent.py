import pygame
import Constants

# Screen
WIDTH, HEIGHT =  Constants.WIDTH, Constants.HEIGHT


# Paddle 
P_WIDTH, P_HEIGHT = Constants.PADDLE_WIDTH, Constants.PADDLE_HEIGHT

MOVE_COEF = Constants.MOVE_COEF


class Paddle(pygame.sprite.Sprite):
    def __init__(self,color):
        pygame.sprite.Sprite.__init__(self)
        
        #Constant values for their ratio
        self.image = pygame.Surface([P_WIDTH, P_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
        
    def Move(self, action):
        
        """
        Action:
            0: Rise up
            1: Hold
            2: get down
        """
        
        if action == 0:
            self.rect.y -= MOVE_COEF

        if action == 1:
            #paddleY.rect.y = paddleY.rect.y
            pass
        
        if action == 2:
            self.rect.y += MOVE_COEF

        """
        w/numpy it could be 
        self.rect.y  = np.clip(self.rect.y, 0, HEIGHT - P_HEIGHT)
        """
        
        #Keep the paddle in boundries
        if self.rect.y < 0:  
            self.rect.y = 0

        if self.rect.y > HEIGHT - P_HEIGHT: 
            self.rect.y = HEIGHT - P_HEIGHT

        return self.rect.y
