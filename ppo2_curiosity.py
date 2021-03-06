#!/usr/bin/env python

"""
Train an agent on Sonic using PPO2 with curiosity-driven exploration (https://arxiv.org/abs/1705.05363)
"""

import os
import tensorflow as tf

from baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from baselines.common.vec_env.subproc_vec_env import SubprocVecEnv

# Code for curiosity-driven exploration can be found in baselines/ppo2_curiosity
import baselines.ppo2_curiosity.ppo2 as ppo2
import baselines.ppo2_curiosity.policies as policies

import gym_remote.exceptions as gre

from sonic_util import make_env

def main():
    """Run PPO until the environment throws an exception."""
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True # pylint: disable=E1101
    with tf.Session(config=config):
        # Take more timesteps than we need to be sure that
        # we stop due to an exception.
        ppo2.learn(policy=policies.CnnPolicy,
                   env=DummyVecEnv([make_env]),
                   nsteps=4096,
                   nminibatches=8, 
                   lam=0.95,
                   gamma=0.99,
                   noptepochs=3,
                   log_interval=1,
                   ent_coef=0.001, 
                   lr=lambda _: 2e-4,
                   cliprange=lambda _: 0.1,
                   total_timesteps=int(1e7),
                   load_path='./pretrain_model') # Set to None if no pretrained model

if __name__ == '__main__':
    try:
        main()
    except gre.GymRemoteError as exc:
        print('exception', exc)
