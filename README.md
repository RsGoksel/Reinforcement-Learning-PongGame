# PPO_Optimization_PongGame
Reinforcement Learning - PPO (Proximal Policy Optimization) Implementation to Pong Game 



# Before the Training
![10k](https://github.com/RsGoksel/Train-PPO-Agent_PongGame/assets/80707238/efd096bc-f058-4e60-98b9-d71894aaedd6)
________________________________________________________________________________________________________________

## Problem
The Pong game was discussed for the PPO solution example as problem. A2C and DQN can also be used if requested. It can be switch from train.py file.

### _**Reward:**_
 Reward was the distance between the Ball and Agent. Reward mechanism was:
* Ball coming out - score, 
* Ball hitting the agent + score, 
* Agent coming closer to the ball + score

### _**Observation Space:**_
Observation array was:
* Euclidean distance between Agent and ball,
* Agent_Y_Coord
* Agent_X_Coord
* Ball_Y_Coord
* Ball_X_Coord
* Ball_Velocity
  
### _**Action Space:**_ 
Action space was discrete(3). It means there is certain 3 moves the Agent has to do. Rise Up, hold and get down.
________________________________________________________________________________________________________________

# Usage

* test.py   :  Testing for the environment. You can display how game screen is.
* train.py  :  Trains the Agent. You can change total_steps from Constants.py. Check it out
* Agent.py  :  Padlde & Agent class.
* evaluate.py  :  If you have any trained model, you can evaluate it with this file. Detailed usage is down below. 
* Env.py       :  Environment class. You can alter the game rules, Reward mechanism and what ever you want.
* Constants.py : Stable variables of the Game. Screen width, hyperparameters etc. 


Install required libraries initially:
``` 
$ pip install -r requirements.txt
```

## Test the environment and check everything is OK:
``` 
$ python test.py
```

## Let's begin to Train! 
Default step is 100k. You can alter it from Constants.py  
(Loading Libraries may take a time about 10 seconds)
``` 
$ python train.py
```

## Evalute your model
! After the training, your model will be saved in 'models' file. Evaluate it with: (Do not forget to add model path)
``` 
$ python evaluate.py --model models/yourmodel
```


# After the Training 
![200k](https://github.com/RsGoksel/Train-PPO-Agent_PongGame/assets/80707238/a4ee5f2f-bceb-433d-a6e7-003a5d6cd83f)
________________________________________________________________________________________________________________
