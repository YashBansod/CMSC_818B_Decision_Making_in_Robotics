# !/usr/bin/env python

# ******************************************    Libraries to be imported    ****************************************** #
import numpy as np
from matplotlib import pyplot as plt


# ******************************************        Function Definition     ****************************************** #
def moving_average(base_array, win_size=100):
    running_average = np.cumsum(base_array, dtype=np.float32)
    running_average[win_size:] = running_average[win_size:] - running_average[:-win_size]
    running_average[win_size - 1:] = running_average[win_size - 1:] / win_size

    for i in range(win_size - 1):
        running_average[i] = running_average[i] / (i+1)

    return running_average


# ******************************************        Main Program Start      ****************************************** #
def main():
    reward = np.loadtxt('./saved_reward/unmod_reward_p_2_1.txt')
    running_reward = moving_average(reward, win_size=100)

    flag_100, flag_150, flag_175 = False, False, False

    for i in range(running_reward.shape[0]):
        if running_reward[i] > -100:
            if not flag_100:
                print("Running average of -100 was seen at episode: ", i)
            flag_100 = True
        elif running_reward[i] > -150:
            if not flag_150:
                print("Running average of -150 was seen at episode: ", i)
            flag_150 = True
        elif running_reward[i] > -175:
            if not flag_175:
                print("Running average of -175 was seen at episode: ", i)
            flag_175 = True

    np.savetxt('running_reward.txt', running_reward, delimiter=',')

    fig = plt.figure(5, figsize=[15, 10])
    subplt = fig.subplots()
    plt.title("Q Learning")
    plt.xlabel("Episode")
    plt.ylabel("Running Reward")

    subplt.plot(np.arange(running_reward.shape[0]), running_reward, color='r')
    plt.grid()
    plt.tight_layout()
    fig.savefig('running_reward.png')
    plt.show(block=True)


# ******************************************        Main Program End        ****************************************** #

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print('\nProcess interrupted by user. Bye!')

"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""