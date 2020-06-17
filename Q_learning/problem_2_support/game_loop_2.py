# !/usr/bin/env python

# ******************************************    Libraries to be imported    ****************************************** #
import numpy as np
from data_store import DataStore
from problem_2_support.nn_model_2 import NNModel
from gym.wrappers.time_limit import TimeLimit


# ******************************************    Class Declaration Start     ****************************************** #
class GameLoop(object):

    def __init__(self, data_store, nn_model, env):
        """

        :param DataStore data_store:
        :param NNModel nn_model:
        :param TimeLimit env:
        """
        self._ep_num = 0
        self._steps = 0
        self._lambda = 0.00001
        self._gamma = 0.99
        self._max_epsil = 1
        self._min_epsil = 0.01
        self._epsil = self._min_epsil + (self._max_epsil - self._min_epsil) * np.exp(-self._lambda * self._steps)
        self._max_pos_thresh = 0.45
        self._min_cost = 100000
        self._max_steps_per_ep = 500

        self.reward_history = []
        # self.max_pos_history = []

        self._data_store = data_store
        self._nn_model = nn_model
        self._env = env

        self._train_size = self._nn_model.batch_size * 1

    # ******************************        Class Method Declaration        ****************************************** #
    def train_episode(self, render=False):
        episode_reward = 0
        max_pos = -10
        curr_state = self._env.reset()
        cost_list = []

        for index in range(self._max_steps_per_ep):

            if render:
                self._env.render()

            action = self._choose_action(curr_state)
            next_state, reward, done, _ = self._env.step([action])
            max_pos = next_state[0] if next_state[0] > max_pos else max_pos

            if done or index == self._max_steps_per_ep - 1:
                done = True
                next_state[0] = -10

            data_array = np.array((curr_state[0], curr_state[1], action, reward, next_state[0], next_state[1]),
                                  dtype=np.float32)
            self._data_store.add_sample(data_array)

            episode_reward += reward
            curr_state = next_state

            cost_list.append(self._replay())

            if done:
                self.reward_history.append(episode_reward)
                break

        ep_cost = sum(cost_list) / len(cost_list)

        if self._ep_num == 0:
            self._nn_model.model.save('.\\saved_models\\unmod_reward_p_2_ep_0.h5', save_format='h5')
        elif self._ep_num == 300:
            self._nn_model.model.save('.\\saved_models\\unmod_reward_p_2_ep_300.h5', save_format='h5')

        if ep_cost < self._min_cost:
            if max_pos > self._max_pos_thresh:
                self._min_cost = ep_cost
                self._max_pos_thresh = max_pos
                self._nn_model.model.save('.\\saved_models\\unmod_reward_p_2.h5', save_format='h5')

        self._ep_num += 1

        return episode_reward, max_pos, ep_cost

    # ******************************        Class Method Declaration        ****************************************** #
    def test_episode(self, render=False):
        episode_reward = 0
        max_pos = -10
        curr_state = self._env.reset()

        for index in range(self._max_steps_per_ep):

            if render:
                self._env.render()

            action = self._choose_action(curr_state, epsilon=0)
            next_state, reward, done, _ = self._env.step([action])
            max_pos = next_state[0] if next_state[0] > max_pos else max_pos

            curr_state = next_state
            episode_reward += reward

            if done:
                break

        return episode_reward

    # ******************************        Class Method Declaration        ****************************************** #
    def _choose_action(self, curr_state, epsilon=None):

        if epsilon is None:
            epsilon = self._epsil
            self._steps += 1
            self._epsil = self._min_epsil + (self._max_epsil - self._min_epsil) * np.exp(-self._lambda * self._steps)

        if np.random.random() < epsilon:
            index = np.random.randint(0, 21)
        else:
            [prediction] = self._nn_model.model.predict_on_batch(np.array([curr_state])).numpy()
            index = np.argmax(prediction)
        action = (index / 10) - 1
        return action

    # ******************************        Class Method Declaration        ****************************************** #
    def _replay(self):

        batch = self._data_store.sample(self._train_size)

        curr_state_arr = batch[:, 0:2]
        action_arr, reward_arr = batch[:, 2], batch[:, 3]
        next_state_arr = batch[:, 4:6]

        action_arr = ((action_arr + 1) * 10).astype(np.int32)

        # predict Q(s,a) given the batch of states
        q_s_a = self._nn_model.model.predict_on_batch(curr_state_arr).numpy()
        # predict Q(s',a') - so that we can do gamma * max(Q(s'a')) below
        q_s_a_d = self._nn_model.model.predict_on_batch(next_state_arr).numpy()
        q_s_a_d[next_state_arr[:, 0] == -10, :] = 0

        # setup training arrays
        labels = q_s_a
        labels[range(labels.shape[0]), action_arr] = reward_arr + self._gamma * q_s_a_d.max(axis=1)

        cost = self._nn_model.model.train_on_batch(curr_state_arr, labels)

        return cost


# ******************************************    Class Declaration End       ****************************************** #

"""
Author: Yash Bansod
UID: 116776547
E-mail: yashb@umd.edu
Organisation: University of Maryland, College Park
"""
