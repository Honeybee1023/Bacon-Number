#!/usr/bin/env python3
import os
import sys
import pickle
import pytest

import lab

TEST_DIRECTORY = os.path.dirname(__file__)


def setup_module(module):
    """
    This function loads the various databases.  It will be run once every time
    test.py is invoked.
    """
    for i in ("tiny", "small", "large"):
        filename = os.path.join(TEST_DIRECTORY, "resources", f"{i}.pickle")
        with open(filename, "rb") as f:
            raw = pickle.load(f)
            setattr(module, f"raw_db_{i}", raw)
            setattr(module, f"db_{i}", lab.transform_data(raw))
            setattr(module, f"fset_{i}", {frozenset(i[:-1]) for i in raw})


def test_acted_together_01():
    # Simple test, two actors who acted together
    actor1 = 4724
    actor2 = 9210
    assert lab.acted_together(db_small, actor1, actor2) is True
    assert lab.acted_together(db_small, actor2, actor1) is True


def test_acted_together_02():
    # Simple test, two actors who had not acted together
    actor1 = 4724
    actor2 = 16935
    assert lab.acted_together(db_small, actor1, actor2) is False
    assert lab.acted_together(db_small, actor2, actor1) is False


def test_acted_together_03():
    # Simple test, nonexistent actor
    actor1 = 4724
    actor2 = 0
    assert lab.acted_together(db_small, actor1, actor2) is False
    assert lab.acted_together(db_small, actor2, actor1) is False


def test_acted_together_04():
    # actors in film 2 have not all been scene partners with each other
    filename = os.path.join(
        TEST_DIRECTORY,
        "resources",
        "tests",
        "test_actors_connecting_films_04.pickle",
    )
    with open(filename, "rb") as f:
        raw_databases = pickle.load(f)

    raw_data = raw_databases[0][0]
    transformed_data = lab.transform_data(raw_data)
    assert lab.acted_together(transformed_data, 7, 10) is True
    assert lab.acted_together(transformed_data, 10, 8) is False


def _run_pickled_together_test(n):
    filename = os.path.join(
        TEST_DIRECTORY,
        "resources",
        "tests",
        "acted_together_%02d.pickle" % n,
    )
    with open(filename, "rb") as f:
        tests = pickle.load(f)

    for _ in range(10_000):
        for a1, a2, v in tests:
            res = lab.acted_together(db_large, a1, a2)
            assert (
                res == v and isinstance(res, bool)
            ), f"expected {bool(v)} for {a1} and {a2} acting together, got {res}"

            res = lab.acted_together(db_tiny, a1, a2)
            assert res is False and isinstance(res, bool), f"expected False for {a1} and {a2} acting together, got {res}"

@pytest.mark.parametrize("test_num", [0, 1])
def test_acted_together_additional(test_num):
    _run_pickled_together_test(test_num)


def test_tiny_bacon_number_00():
    expected = {4724}
    result = lab.actors_with_bacon_number(db_tiny, 0)
    assert expected == result

def test_tiny_bacon_number_01():
    expected = {2876, 1532}
    result = lab.actors_with_bacon_number(db_tiny, 1)
    assert expected == result
    
def test_tiny_bacon_number_02():
    expected = {1640}
    result = lab.actors_with_bacon_number(db_tiny, 2)
    assert expected == result

def test_tiny_bacon_number_03():
    expected = set()
    result = lab.actors_with_bacon_number(db_tiny, 3)
    assert expected == result

def test_bacon_number_01():
    # Actors with Bacon number of 2
    num = 2
    expected = {1640, 1811, 2115, 2283, 2561, 2878, 3085, 4025, 4252, 4765,
                6541, 9827, 11317, 14104, 16927, 16935, 19225, 33668, 66785,
                90659, 183201, 550521, 1059002, 1059003, 1059004, 1059005,
                1059006, 1059007, 1232763}

    first_result = lab.actors_with_bacon_number(db_small, num)
    assert isinstance(first_result, set)
    assert first_result == expected

    second_result = lab.actors_with_bacon_number(db_small, num)
    assert isinstance(second_result, set)
    assert second_result == expected


def test_bacon_number_02():
    # Actors with Bacon number of 3
    num = 3
    expected = {52, 1004, 1248, 2231, 2884, 4887, 8979, 10500, 12521,
                14792, 14886, 15412, 16937, 17488, 19119, 19207, 19363,
                20853, 25972, 27440, 37252, 37612, 38351, 44712, 46866,
                46867, 48576, 60062, 75429, 83390, 85096, 93138, 94976,
                109625, 113777, 122599, 126471, 136921, 141458, 141459,
                141460, 141461, 141495, 146634, 168638, 314092, 349956,
                558335, 572598, 572599, 572600, 572601, 572602, 572603,
                583590, 931399, 933600, 1086299, 1086300, 1168416, 1184797,
                1190297, 1190298, 1190299, 1190300}

    first_result = lab.actors_with_bacon_number(db_small, num)
    assert isinstance(first_result, set)
    assert first_result == expected

    second_result = lab.actors_with_bacon_number(db_small, num)
    assert isinstance(second_result, set)
    assert second_result == expected


def test_bacon_number_03():
    # large Bacon number, random graph
    filename = os.path.join(
        TEST_DIRECTORY,
        "resources",
        "tests",
        "bacon_number_3.pickle",
    )
    with open(filename, "rb") as f:
        raw_db = pickle.load(f)
    transformed_data = lab.transform_data(raw_db)


    result1 = lab.actors_with_bacon_number(transformed_data, 500)
    assert isinstance(result1, set)
    assert len(result1) == 12

    result2 = lab.actors_with_bacon_number(transformed_data, 501)
    assert isinstance(result2, set)
    assert len(result2) == 8

    for num in range(900, 1001):
        result = lab.actors_with_bacon_number(transformed_data, num)
        assert isinstance(result, set)
        assert len(result) == 5


def test_bacon_number_04():
    # random graph, large Bacon number with no people
    filename = os.path.join(
        TEST_DIRECTORY,
        "resources",
        "tests",
        "bacon_number_4.pickle",
    )
    with open(filename, "rb") as f:
        raw_db = pickle.load(f)
    transformed_data = lab.transform_data(raw_db)

    assert len(lab.actors_with_bacon_number(transformed_data, 10**20)) == 0
    assert len(lab.actors_with_bacon_number(transformed_data, 10**20)) == 0


def test_tiny_bacon_path():
    expected = lab.bacon_path(db_tiny, 1640)
    result = [4724, 2876, 1640]
    assert result == expected

def test_bacon_path_01():
    # Bacon path, small database, path does not exist
    actor_id = 2876669
    expected = None

    first_result = lab.bacon_path(db_small, actor_id)
    assert first_result == expected

    second_result = lab.bacon_path(db_small, actor_id)
    assert second_result == expected


def test_bacon_path_02():
    # Bacon path, small database, length of 4 (4 actors, 3 movies)
    actor_id = 46866
    len_expected = 4

    first_result = lab.bacon_path(db_small, actor_id)
    second_result = lab.bacon_path(db_small, actor_id)

    check_valid_path(fset_small, first_result, len_expected)
    check_end_points(first_result, 4724, {actor_id})
    check_valid_path(fset_small, second_result, len_expected)
    check_end_points(second_result, 4724, {actor_id})


def test_bacon_path_03():
    # Bacon path, large database, length of 3 (3 actors, 2 movies)
    actor_id = 1204
    len_expected = 3
    result = lab.bacon_path(db_large, actor_id)

    check_valid_path(fset_large, result, len_expected)
    check_end_points(result, 4724, {actor_id})



def test_bacon_path_04():
    # Bacon path, large database, length of 5 (5 actors, 4 movies)
    actor_id = 197897
    len_expected = 5
    result = lab.bacon_path(db_large, actor_id)

    check_valid_path(fset_large, result, len_expected)
    check_end_points(result, 4724, {actor_id})


def test_bacon_path_05():
    # Bacon path, large database, length of 7 (7 actors, 6 movies)
    actor_id = 1345462
    len_expected = 7
    first_result = lab.bacon_path(db_large, actor_id)

    # compute the result twice, to test for mutation of the db
    second_result = lab.bacon_path(db_large, actor_id)


    check_valid_path(fset_large, first_result, len_expected)
    check_end_points(first_result, 4724, {actor_id})
    check_valid_path(fset_large, second_result, len_expected)
    check_end_points(second_result, 4724, {actor_id})


def test_bacon_path_06():
    # Bacon path, large database, does not exist
    actor_id = 1204555
    expected = None
    result = lab.bacon_path(db_large, actor_id)
    assert result == expected


def test_tiny_actor_to_actor_path():
    expected = lab.actor_to_actor_path(db_tiny, 2876, 1640)
    result = [2876, 1640]
    assert result == expected


def test_actor_to_actor_path_01():
    # Actor path, large database, length of 8 (8 actors, 7 movies)
    actor_1 = 1345462
    actor_2 = 89614
    len_expected = 8

    first_result = lab.actor_to_actor_path(db_large, actor_1, actor_2)
    second_result = lab.actor_to_actor_path(db_large, actor_1, actor_2)

    check_valid_path(fset_large, first_result, len_expected)
    check_end_points(first_result, actor_1, {actor_2})
    check_valid_path(fset_large, second_result, len_expected)
    check_end_points(second_result, actor_1, {actor_2})

def test_actor_to_actor_path_02():
    # Actor path, large database, length of 5 (5 actors, 4 movies)
    actor_1 = 100414
    actor_2 = 57082
    len_expected = 5

    result = lab.actor_to_actor_path(db_large, actor_1, actor_2)

    check_valid_path(fset_large, result, len_expected)
    check_end_points(result, actor_1, {actor_2})


def test_actor_to_actor_path_03():
    # Bacon path, large database, length of 8 (8 actors, 7 movies)
    actor_1 = 43011
    actor_2 = 1379833
    len_expected = 8

    result = lab.actor_to_actor_path(db_large, actor_1, actor_2)

    check_valid_path(fset_large, result, len_expected)
    check_end_points(result, actor_1, {actor_2})


def test_actor_to_actor_path_04():
    # Bacon path, large database, does not exist
    actor_1 = 43011
    actor_2 = 1204555
    result = lab.actor_to_actor_path(db_large, actor_1, actor_2)

    assert result is None


def test_actor_to_actor_path_05():
    # actor to actor path, large database, length of 6
    actor_1 = 1372398
    actor_2 = 62597
    len_expected = 6

    result = lab.actor_to_actor_path(db_large, actor_1, actor_2)

    check_valid_path(fset_large, result, len_expected)
    check_end_points(result, actor_1, {actor_2})


def test_actor_to_actor_path_06():
    # actor to actor path, large database, length of 4
    actor_1 = 184581
    actor_2 = 170882
    len_expected = 4

    result = lab.actor_to_actor_path(db_large, actor_1, actor_2)

    check_valid_path(fset_large, result, len_expected)
    check_end_points(result, actor_1, {actor_2})


def test_actor_to_actor_path_07():
    # actor to actor path, random graph, long path
    filename = os.path.join(
        TEST_DIRECTORY,
        "resources",
        "tests",
        "bacon_number_3.pickle",
    )
    with open(filename, "rb") as f:
        raw_db = pickle.load(f)
    transformed_data = lab.transform_data(raw_db)

    actor_1 = 200223
    actor_2 = 900637
    len_expected = 1002

    result = lab.actor_to_actor_path(transformed_data, actor_1, actor_2)
    edges = {frozenset(x[:2]) for x in raw_db}
    check_valid_path(edges, result, len_expected)
    check_end_points(result, actor_1, {actor_2})


def test_actor_to_actor_path_08():
    # actor to actor path does not exist, slightly modified large db with unconnected actor pair
    actor_1 = 1234567890
    actor_2 = 1234567898
    data = raw_db_large + [(actor_1, actor_2, 0)]

    result_path = lab.actor_to_actor_path(lab.transform_data(data), 4724, actor_2)
    assert result_path is None


def _run_pickled_a2a_path_test(n):
    filename = os.path.join(
        TEST_DIRECTORY,
        "resources",
        "tests",
        "actor_to_actor_path_%02d.pickle" % n,
    )
    with open(filename, "rb") as f:
        tests = pickle.load(f)

    for actor_1, actor_2, expected_len in tests:
        result = lab.actor_to_actor_path(db_large, actor_1, actor_2)

        check_valid_path(fset_large, result, expected_len + 1)
        check_end_points(result, actor_1, {actor_2})


@pytest.mark.parametrize("test_num", [0, 1, 2, 3, 4])
def test_actor_to_actor_path_additional(test_num):
    # find many existing paths in large database
    _run_pickled_a2a_path_test(test_num)


def test_tiny_actor_path():
    expected = lab.actor_path(db_tiny, 4724, lambda p: p in {1640, 2876})
    result = [4724, 2876]

    expected2 = lab.actor_path(db_tiny, 4724, lambda p: False)
    result2 = None
    assert result == expected and result2 == expected2


def test_actor_path_01():
    # actor path, large database, no path
    result = lab.actor_path(db_large, 975260, lambda p: False)
    assert result is None


def test_actor_path_02():
    # actor path, large database, length 1 path
    result = lab.actor_path(db_large, 975260, lambda p: True)
    result2 = lab.actor_path(db_large, 975260, lambda p: p == 975260)
    assert result == result2 == [975260]


def test_actor_path_03():
    # actor path, large database
    actor_1 = 10526
    ppl = {536472, 44795, 240045, 19534}

    # unique closest actor 19534
    expected_len = 4
    first_result = lab.actor_path(db_large, actor_1, lambda p: p in ppl)
    check_valid_path(fset_large, first_result, expected_len)
    check_end_points(first_result, actor_1, {19534})


    # try again, change goal test to force longer path to non-unique actor
    second_result = lab.actor_path(db_large, actor_1, lambda p: p in ppl and p > 19534)
    check_valid_path(fset_large, second_result, expected_len + 1)
    check_end_points(second_result, actor_1, {536472, 44795})


def test_actor_path_04():
    # actor path, large database, path length 7 to non-unique end point
    actor_1 = 152597
    result = lab.actor_path(db_large, actor_1, lambda p: p in {129507, 1400266, 1355798})
    expected_len = 7
    check_valid_path(fset_large, result, expected_len)
    check_end_points(result, actor_1, {1400266, 1355798})



def test_actor_path_05():
    # actor path, large database, path length 2 to unique end point
    actor_1 = 26473
    result = lab.actor_path(db_large, actor_1, lambda p: p in {105656, 118946})
    expected_len = 2
    check_valid_path(fset_large, result, expected_len)
    check_end_points(result, actor_1, {118946})


def test_actor_path_06():
    # actor path, large database, path length 8 to unique end point
    actor_1 = 129507
    actor_2 = 152597
    result = lab.actor_path(db_large, actor_1, lambda p: p == actor_2)
    expected_len = 8
    check_valid_path(fset_large, result, expected_len)
    check_end_points(result, actor_1, {actor_2})


def test_actors_connecting_films_01():
    # tests actors_connecting_films, large database, path length 2
    check_connected_film_path(18860, 75181, 2)


def test_actors_connecting_films_02():
    # tests actors_connecting_films, large database, path length 5
    check_connected_film_path(142416, 44521, 5)


def test_actors_connecting_films_03():
    # check that we can find a length 1 path when an actor is in both movies
    expected = [[19302], [19303]]
    assert lab.actors_connecting_films(db_large, 177361, 177361) in expected

    # note that film 1 is not in the large database, so there is no path!
    assert lab.actors_connecting_films(db_large, 177361, 1) is None
    assert lab.actors_connecting_films(db_large, 1, 44521) is None


    # a random tree, where movies 0 and 1 do exist, but there is no path
    # to connect the actors between them
    filename = os.path.join(
        TEST_DIRECTORY,
        "resources",
        "tests",
        "test_actors_connecting_films_03.pickle",
    )
    with open(filename, "rb") as f:
        raw_data = pickle.load(f)

    transformed_data = lab.transform_data(raw_data)

    assert lab.actors_connecting_films(transformed_data, 0, 1) is None
    assert lab.actors_connecting_films(transformed_data, 1, 0) is None



def  test_actors_connecting_films_04():
    # This test uses a series of random databases with three films:
    # movie 0, movie 1, and movie 2.
    # We are trying to find the shortest path from movie 0 to movie 1.

    # However, there are multiple paths to get from movie 0 to movie 1
    # through a series of pairs of actors in movie 2 (remember -- just because
    # two actors have appeared in the same movie does not mean they have acted
    # together). This test makes sure that you are correctly finding the shortest
    # path of directly connected actors according to the raw database.

    filename = os.path.join(
        TEST_DIRECTORY,
        "resources",
        "tests",
        "test_actors_connecting_films_04.pickle",
    )
    with open(filename, "rb") as f:
        raw_databases = pickle.load(f)

    m0 = 0
    m1 = 1
    for raw_data, pairs, m0a, m1a, expected_len in raw_databases:
        transformed_data = lab.transform_data(raw_data)
        result = lab.actors_connecting_films(transformed_data, m0, m1)
        check_valid_path(pairs, result, expected_len)
        assert result[0] in m0a, f'path does not start with actor in film1! {result=}'
        assert result[-1] in m1a, f'path does not end with actor in film2! {result=}'



def check_end_points(result_path, start_point, end_points):
    '''
    result_path : result path found using lab function
    start_point : an actor id that the path should start with
    end_points : a set of actor ids that represent valid end points
    '''
    assert result_path[0] == start_point, f'path does not start with desired actor! {result_path=}'
    assert result_path[-1] in end_points, f'path does not end with a desired actor! {result_path=}'

def check_valid_path(edges, result_path, expected_len):
    '''
    edges : a set of frozenset actor pairs present in the data base
    result_path : result path found using lab function
    expected_len : length of expected path
    '''
    end_err = f' in found path {result_path}'
    assert len(result_path) == expected_len, f"expected a path of length {expected_len}, got {len(result_path)}" + end_err
    assert isinstance(result_path, list), f"expected a path to be a list or None, got {type(result_path)}" + end_err
    assert all(frozenset(i) in edges for i in zip(result_path, result_path[1:])), f"invalid connection" + end_err


def check_connected_film_path(m1, m2, expected_length):
    m1a = set()
    m2a = set()
    for a, b, c in raw_db_large:
        if c == m1:
            s = m1a
        elif c == m2:
            s = m2a
        else:
            continue
        s.add(a)
        s.add(b)
    result = lab.actors_connecting_films(db_large, m1, m2)
    assert result[0] in m1a, f'path does not start with actor in film1! {result=}'
    assert result[-1] in m2a, f'path does not end with actor in film2! {result=}'
    check_valid_path(fset_large, result, expected_length)

