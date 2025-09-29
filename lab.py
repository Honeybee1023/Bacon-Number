"""
6.101 Lab:
Snekoban Game
"""

# import json # optional import for loading test_levels
# import typing # optional import
# import pprint # optional import

# NO ADDITIONAL IMPORTS!


DIRECTION_VECTOR = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def make_new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The returned description is a dictionary of 4 keys ("wall", "player", "computer", "target") with
    each key's value being a set of coordinates (row, col) that the key is on. Additionally, we include
    the height and width values of the board for easy conversion back to the original representation

    This function should not mutate the level_description.
    """
    new_rep = {"wall": set(), "computer": set(), "target": set()}
    
    height = len(level_description)
    width = len(level_description[0])

    new_rep["height"] = height
    new_rep["width"] = width
    
    for col in range(width):
        for row in range(height):
            for item in level_description[row][col]:
                if item == "player":
                    new_rep[item] = (row, col)
                else:
                    new_rep[item].add((row, col))
                
    return new_rep


def victory_check(game):
    """
    Given a game representation (of the form returned from make_new_game), where
    there are the same number of computers and targets, return a Boolean:
    True if all the computers are placed on targets, and False otherwise.

    A game with no computers or targets is unwinnable. This function should not mutate
    the input game.
    """
    if len(game["computer"]) == 0 or len(game["target"]) == 0 or len(game["computer"]) != len(game["target"]):
        return False

    return game["computer"] == game["target"]


def step_game(game, direction):
    """
    Given a game representation (of the form returned from make_new_game),
    return a game representation (of that same form), representing the
    updated game after running one step of the game.  The user's input is given
    by direction, which is one of the following:
        {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    Hint: you may want to use the DIRECTION_VECTOR
    """
    new_game = {
        "wall": set(game["wall"]),
        "computer": set(game["computer"]),
        "target": set(game["target"]),
        "player": game["player"],
        "height": game["height"],
        "width": game["width"]
        }
    
    #Set a goal spot that the player is trying to move into
    current_player = new_game["player"]
    goal_player = tuple(x+y for (x, y) in zip(current_player, DIRECTION_VECTOR[direction]))
    #If there is wall there, player will not move
    if goal_player in new_game["wall"]:
        return new_game
    #If there is computer there:
    elif goal_player in new_game["computer"]:
        #Set that goal spot that the computer is trying to move to, one step in direction of player's move
        current_computer = goal_player
        goal_computer = tuple(x+y for (x, y) in zip(current_computer, DIRECTION_VECTOR[direction]))
        #If there is solid object (either wall or computer) there, neither player nor computer moves
        if goal_computer in new_game["computer"] or goal_computer in new_game["wall"]:
            return new_game
        #Otherwise, both player and computer move to their goal spot
        else:
            new_game["computer"].remove(current_computer)
            new_game["computer"].add(goal_computer)
            new_game["player"] = goal_player
            return new_game
    #Otherwise there is no solid object there so the player just moves there
    else:
        new_game["player"] = goal_player
        return new_game


def dump_game(game):
    """
    Given a game representation (of the form returned from make_new_game),
    convert it back into a level description that would be a suitable input to
    make_new_game (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own. This function should not mutate the game.
    """
    level_description = [[[] for _ in range(game["width"])] for _ in range(game["height"])]
    
    for item in ["wall", "computer", "target"]:
        for (row, col) in game[item]:
            level_description[row][col].append(item)

    level_description[game["player"][0]][game["player"][1]].append("player")

    return level_description

def get_neighbor(game):
    """
    Given a game state in the internal representation of the board, return a list of game states reachable
    in one move from the current game state
    """
    return [board for board in [
        step_game(game, "up"),
        step_game(game, "down"),
        step_game(game, "left"),
        step_game(game, "right")
        ] if board != game]

def state_path_to_move_path(state_path):
    """
    Given a tuple of n states, return a list of strings which are n-1 moves connecting the states
    """
    move_path = []

    vect_to_dir = {
            (-1, 0): "up",
            (1, 0): "down",
            (0, -1): "left",
            (0, 1): "right"
            }
    
    for index in range(len(state_path)-1):
        move_vector = tuple(x-y for (x, y) in zip(state_path[index+1]["player"], state_path[index]["player"]))
        move_path.append(vect_to_dir[move_vector])

    return move_path

def solve_puzzle(game):
    """
    Given a game representation (of the form returned from make_new_game), find
    a solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None. This function should not mutate
    the input game.
    """
    if victory_check(game):
        return []
    
    visited = {(game["player"], frozenset(game["target"]), frozenset(game["computer"]))}
    agenda = [(game, )]

    while agenda:
        current_path = agenda.pop(0)
        last_state = current_path[-1]

        for neighbor in get_neighbor(last_state):
            if (neighbor["player"], frozenset(neighbor["target"]), frozenset(neighbor["computer"])) not in visited:
                new_path = current_path + (neighbor,)
                if victory_check(neighbor):
                    return state_path_to_move_path(new_path)
                else:
                    agenda.append(new_path)
                    visited.add((neighbor["player"], frozenset(neighbor["target"]), frozenset(neighbor["computer"])))

    return None


if __name__ == "__main__":
    pass
