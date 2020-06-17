import matplotlib.pyplot as plt
import gym          # Tested on version gym v. 0.14.0 and python v. 3.17

env = gym.make('MountainCar-v0')
env.seed(42)

# Print some info about the environment
print("State space (gym calls it observation space)")
print(env.observation_space)
print("\nAction space")
print(env.action_space)

# Parameters
NUM_STEPS = 200
NUM_EPISODES = 1000
LEN_EPISODE = 200
reward_history = []

# Run for NUM_EPISODES
for episode in range(NUM_EPISODES):
    episode_reward = 0
    curr_state = env.reset()

    for step in range(LEN_EPISODE):
        # Comment to stop rendering the environment
        # If you don't render, you can speed things up
        env.render()

        # Randomly sample an action from the action space
        # Should really be your exploration/exploitation policy
        action = env.action_space.sample()

        # Step forward and receive next state and reward
        # done flag is set when the episode ends: either goal is reached or
        #       200 steps are done
        next_state, reward, done, _ = env.step(action)

        # This is where your NN/GP code should go
        # Create target vector
        # Train the network/GP
        # Update the policy

        # Record history
        episode_reward += reward

        # Current state for next step
        curr_state = next_state

        if done:
            # Record history
            reward_history.append(episode_reward)

            # You may want to plot periodically instead of after every episode
            # Otherwise, things will slow down
            fig = plt.figure(1)
            plt.clf()
            plt.xlim([0, NUM_EPISODES])
            plt.plot(reward_history,'ro')
            plt.xlabel('Episode')
            plt.ylabel('Reward')
            plt.title('Reward Per Episode')
            plt.pause(0.01)
            fig.canvas.draw()

            break
