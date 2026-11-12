import random
import pytest

from puzzle.state import State, GOAL_STATE
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar

EASY = (1, 2, 3, 4, 5, 6, 0, 7, 8)
MEDIUM = (1, 2, 3, 0, 4, 6, 7, 5, 8)
HARD = (8, 1, 3, 4, 0, 2, 7, 6, 5)


def inversions(tiles):
    t = [x for x in tiles if x]
    return sum(a > b for i, a in enumerate(t) for b in t[i + 1:])


def apply(tiles, actions):
    tiles = list(tiles)
    d = {"UP": -3, "DOWN": 3, "LEFT": -1, "RIGHT": 1}
    for a in actions:
        b = tiles.index(0)
        n = b + d[a]
        tiles[b], tiles[n] = tiles[n], tiles[b]
    return tuple(tiles)


def test_neighbors_and_path():
    s = State((1, 2, 3, 4, 0, 5, 6, 7, 8))
    assert len(s.neighbors()) == 4
    assert len(State((0, 1, 2, 3, 4, 5, 6, 7, 8)).neighbors()) == 2
    child = s.neighbors()[0]
    assert child.path() == [s, child]
    assert child.actions() == ["UP"]
    assert s.actions() == []


def test_goal_initial():
    for alg in (BFS(), DFS(), AStar()):
        r = alg.search(State(GOAL_STATE))
        assert r.found and r.path_cost == 0 and r.actions == []


@pytest.mark.parametrize("tiles", [EASY, MEDIUM, HARD])
@pytest.mark.parametrize("alg", [BFS, DFS, AStar])
def test_solution_valid(tiles, alg):
    r = alg().search(State(tiles))
    assert r.found
    assert apply(tiles, r.actions) == GOAL_STATE
    assert r.depth == r.path_cost == len(r.actions)


@pytest.mark.parametrize("tiles", [EASY, MEDIUM, HARD])
def test_bfs_and_astar_optimal(tiles):
    b = BFS().search(State(tiles))
    a = AStar().search(State(tiles))
    assert b.path_cost == a.path_cost


def test_random_solvable_astar_matches_bfs():
    rng = random.Random(1)
    for _ in range(5):
        t = list(GOAL_STATE)
        rng.shuffle(t)
        if inversions(t) % 2:
            continue
        b = BFS().search(State(tuple(t)))
        a = AStar().search(State(tuple(t)))
        assert a.path_cost == b.path_cost
        assert a.nodes_expanded <= b.nodes_expanded


def test_unsolvable():
    t = (2, 8, 3, 1, 6, 4, 7, 0, 5)
    assert inversions(t) % 2 == 1
    for alg in (BFS(), DFS(), AStar()):
        assert not alg.search(State(t)).found


def test_heuristic():
    h = AStar().heuristic
    assert h(State(GOAL_STATE)) == 0
    assert h(State((1, 2, 3, 4, 5, 6, 0, 7, 8))) == 2


@pytest.mark.parametrize("tiles", [EASY, MEDIUM, HARD])
def test_astar_custom_heuristic(tiles):
    calls = []

    def zero(state):
        calls.append(state)
        return 0

    a = AStar(heuristic=zero).search(State(tiles))
    b = BFS().search(State(tiles))
    assert calls
    assert a.path_cost == b.path_cost
    assert apply(tiles, a.actions) == GOAL_STATE
