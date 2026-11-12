from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        nodes_generated = 1
        nodes_expanded = 0

        stack = [initial]
        best_depth = {initial.tiles: 0}
        max_frontier = 1

        while stack:
            current = stack.pop()

            if best_depth.get(current.tiles, current.cost) < current.cost:
                continue

            if current.is_goal:
                return SearchResult(current, nodes_expanded, nodes_generated,
                                    max_frontier, current.cost)

            if current.cost >= self.depth_limit:
                continue

            nodes_expanded += 1
            for child in reversed(current.neighbors()):
                known = best_depth.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_depth[child.tiles] = child.cost
                nodes_generated += 1
                stack.append(child)

            max_frontier = max(max_frontier, len(stack))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
