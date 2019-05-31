import sys
sys.path.append("..")

import easymap
import numpy as np
import random
import csv
import os.path
from network import neural_net, LossHistory

sensor_input = 5
GAMMA = 0.9  # Forgetting.
easymap.fps = 9999 # Simulation speed

def train_net(model, params):

    filename = params_to_filename(params)

    observe = 1000  # Number of frames to observe before training.
    epsilon = 0.5
    train_frames = 1000000  # Number of frames to play.
    batchSize = params['batchSize']
    buffer = params['buffer']

    # Initial states
    max_reward = 0
    reward = 0
    t = 0
    data_collect = []
    replay = []
    loss_log = []

    game_state = easymap.GameState(display_hidden=True) # Hide the game screen to improve performance

    # Get initial state by doing nothing and getting the state.
    _, state = game_state.frame_step((2))

    # Run the frames.
    while t < train_frames:
        t += 1

        # Choose an action.
        if random.random() < epsilon or t < observe:
            action = np.random.randint(0, 2)  # random
        else:
            # Get Q values for each action.
            qval = model.predict(state, batch_size=1)
            action = (np.argmax(qval))  # best

        # Take action, observe new state and get our treat.
        reward, new_state = game_state.frame_step(action)

        # Experience replay storage.
        replay.append((state, action, reward, new_state))

        # If we're done observing, start training.
        if t > observe:

            # If we've stored enough in our buffer, pop the oldest.
            if len(replay) > buffer:
                replay.pop(0)

            # Randomly sample our experience replay memory
            minibatch = random.sample(replay, batchSize)

            # Get training values.
            X_train, y_train = process_minibatch2(minibatch, model)

            # Train the model on this batch.
            history = LossHistory()
            model.fit(
                X_train, y_train, batch_size=batchSize,
                nb_epoch=1, verbose=0, callbacks=[history]
            )
            loss_log.append(history.losses)

        # Update the starting state with S'.
        state = new_state

        # Decrement epsilon to 0
        if epsilon > 0 and t > observe:
            epsilon -= (1.0/train_frames)

        # We died, so update stuff.
        if reward != -500:
            # Log the car's distance at this T.
            data_collect.append([t, reward])

            # Update max.
            if reward > max_reward:
                max_reward = reward

            # Output some stuff so we can watch.
            print("Max: %d at %d\tepsilon %f\t(%d)" %
                  (max_reward, t, epsilon, reward))

        # Save the model every 500,000 frames.
        if t % 500000 == 0:
            model.save_weights('easy_models/' + filename + '-' +
                               str(t) + '.h5',
                               overwrite=True)
            print("Saving model %s - %d" % (filename, t))

    # Log results after we're done all frames.
    log_results(filename, data_collect, loss_log)


def log_results(filename, data_collect, loss_log):
    # Save the results to a file so we can graph it later.
    with open('easy_results/learn_data-' + filename + '.csv', 'w', newline='') as data_dump:
        wr = csv.writer(data_dump)
        wr.writerows(data_collect)

    with open('easy_results/loss_data-' + filename + '.csv', 'w', newline='') as lf:
        wr = csv.writer(lf)
        for loss_item in loss_log:
            wr.writerow(loss_item)

def process_minibatch2(minibatch, model):
    # by Microos, improve this batch processing function 
    #   and gain 50~60x faster speed (tested on GTX 1080)
    #   significantly increase the training FPS
    
    # instead of feeding data to the model one by one, 
    #   feed the whole batch is much more efficient

    mb_len = len(minibatch)

    old_states = np.zeros(shape=(mb_len, 5))
    actions = np.zeros(shape=(mb_len,))
    rewards = np.zeros(shape=(mb_len,))
    new_states = np.zeros(shape=(mb_len, 5))

    for i, m in enumerate(minibatch):
        old_state_m, action_m, reward_m, new_state_m = m
        old_states[i, :] = old_state_m[...]
        actions[i] = action_m
        rewards[i] = reward_m
        new_states[i, :] = new_state_m[...]

    old_qvals = model.predict(old_states, batch_size=mb_len)
    new_qvals = model.predict(new_states, batch_size=mb_len)

    maxQs = np.max(new_qvals, axis=1)
    y = old_qvals
    non_term_inds = np.where(rewards != -500)[0]
    term_inds = np.where(rewards == -500)[0]

    y[non_term_inds, actions[non_term_inds].astype(int)] = rewards[non_term_inds] + (GAMMA * maxQs[non_term_inds])
    y[term_inds, actions[term_inds].astype(int)] = rewards[term_inds]

    X_train = old_states
    y_train = y
    return X_train, y_train

def process_minibatch(minibatch, model):
    """This does the heavy lifting, aka, the training. It's super jacked."""
    X_train = []
    y_train = []
    # Loop through our batch and create arrays for X and y
    # so that we can fit our model at every step.
    for memory in minibatch:
        # Get stored values.
        old_state_m, action_m, reward_m, new_state_m = memory
        # Get prediction on old state.
        old_qval = model.predict(old_state_m, batch_size=1)
        # Get prediction on new state.
        newQ = model.predict(new_state_m, batch_size=1)
        # Get our predicted best move.
        maxQ = np.max(newQ)
        y = np.zeros((1, 5))
        y[:] = old_qval[:]
        # Check for terminal state.
        if reward_m != -500:  # non-terminal state
            update = (reward_m + (GAMMA * maxQ))
        else:  # terminal state
            update = reward_m
        # Update the value for the action we took.
        y[0][action_m] = update
        X_train.append(old_state_m.reshape(sensor_input,))
        y_train.append(y.reshape(6,))

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    return X_train, y_train


def params_to_filename(params):
    return str(params['network'][0]) + '-' + str(params['network'][1]) + '-' + \
            str(params['batchSize']) + '-' + str(params['buffer'])


def launch_learn(params):
    filename = params_to_filename(params)
    print("Trying %s" % filename)
    # Make sure we haven't run this one.
    if not os.path.isfile('easy_results/loss_data-' + filename + '.csv'):
        # Create file so we don't double test when we run multiple
        # instances of the script at the same time.
        open('easy_results/loss_data-' + filename + '.csv', 'a').close()
        print("Starting test.")
        # Train.
        model = neural_net(sensor_input, params['network'])
        train_net(model, params)
    else:
        print("Already tested.")


if __name__ == "__main__":
    network_param = [256, 256]
    params = {"batchSize": 400, "buffer": 50000, "network": network_param}
    model = neural_net(sensor_input, network_param)
    train_net(model, params)
