import sys
sys.path.append("..")

import easymap
import numpy as np
from network import neural_net

NUM_SENSORS = 5
easymap.fps = 120

def play(model):
    game_state = easymap.GameState(display_hidden=False)

    # Do nothing to get initial.
    _, state = game_state.frame_step((2))

    # Move.
    while True:
        # Choose action.
        action = (np.argmax(model.predict(state, batch_size=1)))
        # Take action.
        _, state = game_state.frame_step(action)

if __name__ == "__main__":
    # Change this according to file that should be loaded
    saved_model = 'easy_models/256-256-400-50000-500000.h5'
    # Change this as well to match network of loaded file
    model = neural_net(NUM_SENSORS, [256, 256], saved_model)
    play(model)
