# PPO_Optimization_PongGame
Reinforcement Learning - PPO (Proximal Policy Optimization) Implementation to Pong Game 
___________________________________________________________________________________________
What is PPO

 * Proximal Policy Optimization (PPO) is presently considered state-of-the-art in Reinforcement Learning.  
PPO strikes a balance between ease of implementation, sample complexity, and ease of tuning, trying to compute an update at each step that minimizes the cost function while ensuring the deviation from the previous policy is relatively small.
____________________________________________________________
![image](https://github.com/RsGoksel/PPO_Optimization_PongGame/assets/80707238/0fb88ba1-3463-4bdf-86d3-4e7993e5e505)
  


  In this repository, the agent is being trained as if the current state is closer to the ball than the previous state, and the reward mechanism scores and reinforces the agent accordingly.


This model "Beast" trained by this approach. 

https://github.com/RsGoksel/PPO_Optimization_PongGame/assets/80707238/bd752882-3c93-4859-bb2f-18c769714ad0


On the other hand, this "Apoclaypse" model is trained to make minimal movements and approach the ball closely. It got penalized every move same time.

https://github.com/RsGoksel/PPO_Optimization_PongGame/assets/80707238/1e7076fc-4bf6-4459-813b-ee63c740ebec





____________________________________________________________________________________________________________


It took 50 iteration for train Beast Model.

![image](https://github.com/RsGoksel/PPO_Optimization_PongGame/assets/80707238/f36fc527-2a75-42c6-9d23-e1bfc91e036d)

In conclusion, this project serves as a valuable resource for anyone looking to dive into reinforcement learning, PPO, and game AI. 

For use the model and analyze it, install required libraries 

```bash
 pip install -r requirements.txt
```
