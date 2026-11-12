import heapq
from itertools import count
from typing import Callable, Optional
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):
    def __init__(self, heuristic: Optional[Callable[[State], int]] = None):
        if heuristic is not None:
            self.heuristic = heuristic

    def heuristic(self, state: State) -> int:
        total = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_index = tile - 1
            total += abs(index // 3 - goal_index // 3) + abs(index % 3 - goal_index % 3)
        return total

    def search(self, initial: State) -> SearchResult:
        nodes_generated = 1
        nodes_expanded = 0
        tie = count()

        frontier = [(self.heuristic(initial), next(tie), initial)]
        best_g = {initial.tiles: initial.cost}
        closed = set()
        max_frontier = 1

        while frontier:
            _, _, current = heapq.heappop(frontier)

            if current.tiles in closed:
                continue

            if current.is_goal:
                return SearchResult(current, nodes_expanded, nodes_generated,
                                    max_frontier, current.cost)

            closed.add(current.tiles)
            nodes_expanded += 1

            for child in current.neighbors():
                if child.tiles in closed:
                    continue
                known = best_g.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_g[child.tiles] = child.cost
                nodes_generated += 1
                f = child.cost + self.heuristic(child)
                heapq.heappush(frontier, (f, next(tie), child))

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
