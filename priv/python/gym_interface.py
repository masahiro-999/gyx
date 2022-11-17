import gym
from erlport.erlang import set_encoder, set_decoder
from erlport.erlterms import List
import numpy as np

def make(envname):
    en = str(envname, encoding='ascii')
    env = gym.make(en)
    print("             < 🐍  >  Loaded Gym environment {0} from Python ✔".format(envname))
    initial_state = env.reset()
    if type(initial_state)==tuple and type(initial_state[0]) == np.ndarray:
        initial_state =(initial_state[0].tolist(),)
    action_space = str(env.action_space).strip()
    observation_space = str(env.observation_space).strip()
    return (env, initial_state, action_space, observation_space)


def step(env, _step):
    state, reward, terminated, truncated, info = env.step(_step)
    if type(state) == np.ndarray:
        state =state.tolist()
    return (env, (state, float(reward), terminated, truncated, info))


def render(env):
    #    env.env.ale.saveScreenPNG(b'test_image.png')
    #res = env.render(mode='rgb_array')
    env.render()


def reset(env):
    initial_state = env.reset()
    if type(initial_state) == np.ndarray:
        initial_state =initial_state.tolist()

    return (env,
            initial_state,
            str(env.action_space).strip(),
            str(env.observation_space).strip())


def action_space_sample(env):
    return env.action_space.sample()


def getScreenRGB(env):
    return List([List([List([j[0] for j in i])
                       for i in env.render(mode='rgb_array')]),
                 List([List([j[1] for j in i])
                       for i in env.render(mode='rgb_array')]),
                 List([List([j[2] for j in i])
                       for i in env.render(mode='rgb_array')])])


def getScreenRGB2(env):
    return List([List([int('#{:02x}{:02x}{:02x}'.
                           format(j[0], j[1], j[2])[1:], 16) for j in i])
                 for i in env.render(mode='rgb_array')])


def getScreenRGB3(env):
    rgb_array = env.render(mode='rgb_array')
    return List([List([List([j[0] for j in i])
                       for i in rgb_array]),
                 List([List([j[1] for j in i])
                       for i in rgb_array]),
                 List([List([j[2] for j in i])
                       for i in rgb_array])])