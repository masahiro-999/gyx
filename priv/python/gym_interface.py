import gym
from erlport.erlang import set_encoder, set_decoder
from erlport.erlterms import List
import numpy as np


# When render_mode="human", env contains data that cannot be converted to Elixir data,
# so the value is saved on the Python side. 
env_list = []

def make(envname, opt):
    opt = {str(key, encoding='ascii'): str(value, encoding='ascii') for key,value in opt.items()}
    en = str(envname, encoding='ascii')
    env = gym.make(en, **opt)
    print(env)
    print("             < 🐍  >  Loaded Gym environment {0} from Python ✔".format(envname))
    initial_state = env.reset()
    try:
        if len(initial_state) == 2 and type(initial_state[0]) == np.ndarray:
            initial_state =(initial_state[0].tolist(),initial_state[1])
    except:
        pass
    action_space = str(env.action_space).strip()
    observation_space = str(env.observation_space).strip()
    env_list.append(env)
    index = len(env_list)-1
    return (index, initial_state, action_space, observation_space)


def step(_env, _step):
    env = env_list[_env]
    state, reward, terminated, truncated, info = env.step(_step)
    if type(state) == np.ndarray:
        state =state.tolist()
    return (_env, (state, float(reward), terminated, truncated, info))


def render(_env):
    #    env.env.ale.saveScreenPNG(b'test_image.png')
    #res = env.render(mode='rgb_array')
    env = env_list[_env]
    env.render()


def reset(_env):
    env = env_list[_env]
    initial_state = env.reset()
    try:
        if len(initial_state) == 2 and type(initial_state[0]) == np.ndarray:
            initial_state =(initial_state[0].tolist(),initial_state[1])
    except:
        pass

    return (_env,
            initial_state,
            str(env.action_space).strip(),
            str(env.observation_space).strip())


def action_space_sample(_env):
    env = env_list[_env]
    return env.action_space.sample()


def getScreenRGB(_env):
    env = env_list[_env]
    return List([List([List([j[0] for j in i])
                       for i in env.render(mode='rgb_array')]),
                 List([List([j[1] for j in i])
                       for i in env.render(mode='rgb_array')]),
                 List([List([j[2] for j in i])
                       for i in env.render(mode='rgb_array')])])


def getScreenRGB2(_env):
    env = env_list[_env]
    return List([List([int('#{:02x}{:02x}{:02x}'.
                           format(j[0], j[1], j[2])[1:], 16) for j in i])
                 for i in env.render(mode='rgb_array')])


def getScreenRGB3(_env):
    env = env_list[_env]
    rgb_array = env.render(mode='rgb_array')
    return List([List([List([j[0] for j in i])
                       for i in rgb_array]),
                 List([List([j[1] for j in i])
                       for i in rgb_array]),
                 List([List([j[2] for j in i])
                       for i in rgb_array])])