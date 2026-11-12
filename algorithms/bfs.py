from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):
    def search(self, initial: State) -> SearchResult:
        nodes_generated = 1
        nodes_expanded = 0

        if initial.is_goal:
            return SearchResult(initial, nodes_expanded, nodes_generated, 1, initial.cost)

        frontier = deque([initial])
        visited = {initial.tiles}
        max_frontier = 1

        while frontier:
            current = frontier.popleft()
            nodes_expanded += 1

            for child in current.neighbors():
                if child.tiles in visited:
                    continue
                nodes_generated += 1
                if child.is_goal:
                    return SearchResult(child, nodes_expanded, nodes_generated,
                                        max(max_frontier, len(frontier) + 1), child.cost)
                visited.add(child.tiles)
                frontier.append(child)

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
