"""Broadband dielectric coating design using TMM and Gymnasium.

Action: three layer thicknesses in nm. Observation: those thicknesses and R(lambda).
The example uses nondispersive, lossless indices; replace the model for materials
with wavelength-dependent complex optical constants.
"""
import gymnasium as gym
import numpy as np
from tmm import coh_tmm


class ThinFilm(gym.Env):
    metadata = {}

    def __init__(self):
        self.wavelengths = np.linspace(450, 700, 21)
        self.action_space = gym.spaces.Box(10.0, 250.0, shape=(3,), dtype=np.float64)
        self.observation_space = gym.spaces.Box(
            low=np.r_[np.full(3, 10.0), np.zeros(21)],
            high=np.r_[np.full(3, 250.0), np.ones(21)], dtype=np.float64)

    def evaluate(self, thickness):
        reflection, transmission = [], []
        for wavelength in self.wavelengths:
            result = coh_tmm('s', [1, 1.45, 2.1, 1.45, 1.52],
                             [np.inf, *thickness, np.inf], 0, wavelength)
            reflection.append(float(result['R']))
            transmission.append(float(result['T']))
        observation = np.r_[thickness, reflection]
        error = float(np.max(np.abs(np.array(reflection) + transmission - 1)))
        return observation, {'wavelength_nm': self.wavelengths.copy(),
                             'mean_reflectance': float(np.mean(reflection)),
                             'energy_balance_error': error}

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.steps = 0
        return self.evaluate(self.np_random.uniform(10, 250, 3))

    def step(self, action):
        action = np.asarray(action, dtype=np.float64)
        if not self.action_space.contains(action):
            raise ValueError('Supply three layer thicknesses between 10 and 250 nm')
        observation, info = self.evaluate(action)
        self.steps += 1
        # The search budget is an external stopping condition, not a terminal material state.
        return observation, -info['mean_reflectance'], False, self.steps >= 12, info


def make_env():
    return ThinFilm()


def make_policy(seed):
    rng = np.random.default_rng(seed)
    return lambda observation: rng.uniform(10, 250, 3)
