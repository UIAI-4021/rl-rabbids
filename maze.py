import time
import gym
import gym_maze
import numpy as np


def get_reward(next_state):
    goal = 1
    step_penalty = -0.01

    if next_state == 99:
        return goal
    else:
        return step_penalty


def epsilon_greedy(state):
    if np.random.random() < epsilon:
        return np.argmax(Q[state])
    else:
        return np.random.randint(4)


def q_learning(curr_state, next_state, curr_action, Q):

    temporal_difference = get_reward(next_state) + (gamma * np.max(Q[next_state])) - Q[curr_state][curr_action]
    Q[curr_state][curr_action] = Q[curr_state][curr_action] + (alpha * temporal_difference)
    return Q


if __name__ == '__main__':

    # Create an environment
    env = gym.make("maze-random-10x10-plus-v0")
    observation = env.reset()

    # Define the maximum number of iterations
    NUM_EPISODES = 1000
    MAX_STEP = 100
    epsilon = 0.9
    gamma = 0.9
    alpha = 0.9
    done = False

    Q = np.zeros((100, 4))
    current_state = 0
    current_action = epsilon_greedy(0)

    finding_count = 0
    converged = False

    q_list = []

    for episode in range(NUM_EPISODES):
        print(f"episode: {episode}")
        old_q = np.copy(Q)
        for step in range(MAX_STEP):
            env.render()

            next_state, reward, done, truncated = env.step(current_action)

            # if episode > 300:
            #     time.sleep(0.1)

            next_state = int(next_state[1] * 10 + next_state[0])

            next_action = epsilon_greedy(next_state)

            Q = q_learning(current_state, next_state, current_action, Q)

            if episode == 30:
                epsilon = 0.3
            elif episode == 50:
                epsilon = 0.6
            elif episode == 70:
                epsilon = 0.9
            elif episode == 90:
                epsilon = 1

            current_state = next_state
            current_action = next_action

            if done or truncated:
                finding_count += 1
                print(f"Reached the goal for the {finding_count} time")
                observation = env.reset()
                current_state = 0
                current_action = epsilon_greedy(current_state)
                break

        observation = env.reset()
        current_state = 0
        current_action = epsilon_greedy(current_state)

        # if episode == 120:
        #     if np.max(np.abs(q_list[0], q_list[1])) < 1e-10 :
        #         print(f"in episode: {episode} converged")
        print(f"{abs(np.linalg.norm(old_q) - np.linalg.norm(Q))}")

        if abs(np.linalg.norm(old_q) - np.linalg.norm(Q)) < 1e-4:
            print(f"in episode: {episode} converged")
    # Close the environment
    env.close()
