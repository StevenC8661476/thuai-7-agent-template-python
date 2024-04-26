from dataclasses import dataclass, field
from typing import List, Dict
import heapq

from agent.map import Map
from agent.position import Position


def manhattan_distance(lhs: Position[int], rhs: Position[int]) -> int:
    return abs(lhs.x - rhs.x) + abs(lhs.y - rhs.y)


def get_neighbors(game_map: Map, position: Position[int]) -> List[Position[int]]:
    # up, down, left, right
    deltas = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    return [
        Position[int](position.x + dx, position.y + dy)
        for dx, dy in deltas
        if is_valid_position(game_map, Position[int](position.x + dx, position.y + dy))
    ]


def is_valid_position(game_map: Map, position: Position[int]) -> bool:
    return (
        position not in game_map.obstacles
        and 0 <= position.x < game_map.length
        and 0 <= position.y < game_map.length
    )


def find_path_befs(
    game_map: Map, start: Position[int], end: Position[int]
) -> List[Position[int]]:
    """
    Find a path on the game map using the Best-First(Greedy) Search algorithm.

    Returns:
        List[Position[int]]: A list of positions representing the path from start to end. `[]` if no path is found.
    """

    @dataclass(order=True)
    class PrioritizedItem:
        # Here we implement the Greedy Search algorithm. So g_score is not needed.
        h_score: int  # heuristic score. The only score we need.
        position: Position[int] = field(compare=False)

    open_set: List[PrioritizedItem] = []
    heapq.heappush(open_set, PrioritizedItem(manhattan_distance(start, end), start))
    came_from: Dict[Position[int], Position[int]] = {}

    while open_set:
        _, current = heapq.heappop(open_set)

        # If reached the end...
        if current == end:
            break

        # Explore neighbors
        for neighbor in get_neighbors(game_map, current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                heapq.heappush(
                    open_set,
                    PrioritizedItem(manhattan_distance(neighbor, end), neighbor),
                )
    else:
        return []

    # Reconstruct the path
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
