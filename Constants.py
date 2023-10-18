
# Window Configure
WIDTH, HEIGHT = 900, 650

# Agent Configure
MOVE_COEF     = 4       # Speed of the Paddle 
PADDLE_HEIGHT = 60
PADDLE_WIDTH  = 10

# Ball Configure
BALL_Xspeed = 3
BALL_Yspeed = 3

# Hyperparameter Configure
learning_rate  = 0.0004 
ent_coef       = 0.01 
gamma          = 0.95 
gae_lambda     = 0.95
max_grad_norm  = 0.5

total_timesteps = 50000

# Model Configure 
Model_Save_Path = "./Models/" + str(int(total_timesteps/1000)) + "k.zip"  
# Indicates the model path which will save after the training, 

tensorboard_log = "./Pong_Log/"
tensorboard_sub_folder = 'PA_' + str(total_timesteps/1000) + "k"
