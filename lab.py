"""
6.101 Lab:
Bacon Number
"""

#!/usr/bin/env python3

import pickle
# import typing # optional import
# import pprint # optional import

# NO ADDITIONAL IMPORTS ALLOWED!

#HELPER FUNCTIONS
def name_to_ID(name):
    """
    Takes in name as string, return ID number of actor with that name as int
    """
    with open("resources/names.pickle", "rb") as f:
        namesdb = pickle.load(f)

    return namesdb[name]

def ID_to_name(ID):
    """
    Takes in ID of actor as int, return name of actor with that ID as string
    """
    with open("resources/names.pickle", "rb") as f:
        namesdb = pickle.load(f)

    for key, val in namesdb.items():
        if val == ID:
            return(key)
    

#LAB FUNCTIONS

def transform_data_old(raw_data):
    """
    Assume input is list of tuples (Actor ID 1, Actor ID 2, Movie ID)

    We will return data structure of a dictionary where key is a tuple (Actor 1 ID, Actor 2 ID) and value is movie ID

    Reasoning:
        We will often need to check if two actors are in movie together. So we will often call "if (actor 1, actor 2) in database"
        This means either set or dict work well, because they are the only 2 data structures we hace learned so far that have
        constant time access of some form.

        Between these, dict seems better because we may need to access values at some point.

        We must have the two actor IDs as keys of the dictionary for constant time access. Then we will have movie ID as value.
    """
    transformed_data = {}

    for data in raw_data:
        transformed_data[(data[0], data[1])] = data[2]
    
    return transformed_data

def transform_data(raw_data):
    """
    Assume input is list of tuples (Actor ID 1, Actor ID 2, Movie ID)

    We will return data structure of a dictionary where key is each actor ID, value is set of actors who have directly
    acted with that actor

    This makes it easy to access neighbors, which is an operation we use a lot later
    """
    transformed_data = {}

    #initializing empty set for all actors
    for data in raw_data:
        transformed_data[data[0]] = set()
        transformed_data[data[1]] = set()

    #creating enighbor mapping
    for data in raw_data:
        transformed_data[data[0]].add(data[1])
        transformed_data[data[1]].add(data[0])
    
    return transformed_data


def acted_together(neighbor_map, actor_id_1, actor_id_2):
    if actor_id_1 not in neighbor_map.keys() or actor_id_2 not in neighbor_map.keys():
        return False
    
    return (actor_id_2 in neighbor_map[actor_id_1])

def acted_with(neighbor_map, actor_1):
    """
    Return a set of all actors who have acted with the given actor
    """
    return (neighbor_map[actor_1])

def actors_with_bacon_number(neighbor_map, num):
    """
    We will loop through past nums and go layer by layer, and use dict to store past results
    Note: Do NOT use recursion here because it will lead to repeated calls and O(2^n) time complexity
    """
    if num == 0:
        return {4724}

    else:
        past_recursions = {0: {4724}}
        
        #Make a set of all actors who have lower bacon number already
        visited = {4724}
        for n in range(1, num+1):
            past_recursions[n] = set()
            for last_actor in past_recursions[n-1]:
                for actor in acted_with(neighbor_map, last_actor) - visited:
                    past_recursions[n].add(actor)
                    visited.add(actor)
            if len(past_recursions[n]) == 0:
                return set()

        return past_recursions[num]

def bacon_path(transformed_data, actor_id):
    if actor_id == 4724:
        return [4724]

    elif actor_id not in transformed_data.keys():
        return None

    else:
        #BFS , start by setting up visited and agenda
        visited = {4724}
            #^We only need to visit each node once, not each path once.
            #This is because with bfs, everytime we visit a node we reach there through the shortest path already
            #So we don't need to try to visit this node through another path, we just keep going from there
                # ! - This will not hold when we have edge weights involved!
        agenda = [[4724,]]
            #pop(0) for a list takes O(n) time because we need to shift everything after
            #So technically a FIFO like queue (or deck in python) is better
            #But here it doesn't matter too much (like by 2 secs), plus we cannot import

        #Keep looping, with empty agenda as exit condition (we've tried our best but found no path)
        while not agenda == []:
            #Take out the first item in our queue and visit it
            current_path = agenda.pop(0)

            #Explore all its neighbors
            for neighbor in acted_with(transformed_data, current_path[-1]):
                #If we've reached our goal already then just return this good path
                if neighbor == actor_id:
                    path = current_path + [neighbor]
                    return path
                #Otherwise add new path with this neighbor if we haven't tried visiting this neighbor yet
                else:
                    if neighbor not in visited:
                        new_path = current_path + [neighbor]
                        agenda.append(new_path)
                        visited.add(neighbor)
                            #Better to mark as visited right after adding to queue rather after popping from queue
                            #because we mark as visited sooner, thus avoid repetition within looping over neighbors

        return None


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Copy of bacon_path, except set all instances of 4724 to actor_id_1 instead
    """
    return actor_path(transformed_data, actor_id_1, lambda p: p == actor_id_2)



def actor_path(transformed_data, actor_id_1, goal_test_function):
    """
    Copy of actor_to_actor_path, but replace neighbor==actor_id_2 goal check with our given goal test function
    """
    if goal_test_function(actor_id_1):
        return [actor_id_1]

    elif actor_id_1 not in transformed_data.keys():
        return None

    else:
        visited = {actor_id_1}
        agenda = [[actor_id_1,]]

        while not agenda == []:
            current_path = agenda.pop(0)

            for neighbor in acted_with(transformed_data, current_path[-1]):
                if goal_test_function(neighbor):
                    path = current_path + [neighbor]
                    return path
                else:
                    if neighbor not in visited:
                        new_path = current_path + [neighbor]
                        agenda.append(new_path)
                        visited.add(neighbor)
        return None


def actors_connecting_films(transformed_data, film1, film2):
    raise NotImplementedError("Implement me!")


if __name__ == "__main__":
    with open("resources/small.pickle", "rb") as f:
        smalldb = pickle.load(f)

    with open("resources/names.pickle", "rb") as f:
        namesdb = pickle.load(f)

    transformed_smalldb = transform_data(smalldb)

    with open("resources/tiny.pickle", "rb") as f:
        tinydb = pickle.load(f)

    transformed_tinydb = transform_data(tinydb)

    with open("resources/large.pickle", "rb") as f:
        largedb = pickle.load(f)

    transformed_largedb = transform_data(largedb)

    print(tinydb)

    #print(bacon_path(transformed_tinydb, 1640))
    
    #output = bacon_path(transformed_largedb, name_to_ID("Cecile Arnold"))

    #output = actor_to_actor_path(transformed_largedb, name_to_ID("Marcella Daly"), name_to_ID("Sandra Bullock"))

    #for actor in output:
    #    print("\"", ID_to_name(actor), "\"")

    #print(actors_with_bacon_number(transformed_largedb, 6))

    #{1367972, 1338716, 1345461, 1345462}
    
    #print(ID_to_name(1367972), ID_to_name(1338716), ID_to_name(1345461), ID_to_name(1345462))

    #print(actors_with_bacon_number(transformed_tinydb, 1))

    #print(tinydb)
    #print(name_to_ID("Kevin Bacon"))

    #print(acted_together(transformed_smalldb, name_to_ID("Robert Viharo"), name_to_ID("Patrick Gorman")))
    #print(acted_together(transformed_smalldb, name_to_ID("Sten Hellstrom"), name_to_ID("Johan Akerblom")))

    #print(type(namesdb))
    #print(namesdb)

    #print(namesdb["Anthony J. Baker"])

    #for key, val in namesdb.items():
    #    if val == 65776:
    #        print(key)

    
        
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
