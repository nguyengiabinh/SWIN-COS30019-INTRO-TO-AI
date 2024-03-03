# astar_search_weighted.py
import queue

class Node:
    def __init__(self, position, cost, heuristic):
        # Node class to represent a search node with position, cost, and heuristic
        self.position = position
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        # Custom comparison method for priority queue ordering
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def heuristic_cost_estimate(current, goal):
    # Calculate the heuristic cost estimate using Manhattan distance
    return abs(goal[0] - current[0]) + abs(goal[1] - current[1])

def reconstruct_path(came_from, current):
    # Reconstruct the path from the came_from dictionary
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]

def a_star_search_weighted(grid, start, goal, weight):
    # A* search algorithm with weighted heuristic
    rows, columns = len(grid), len(grid[0])
    open_set = queue.PriorityQueue()
    open_set.put(Node(start, 0, weight * heuristic_cost_estimate(start, goal)))  # Include weight in the heuristic
    came_from = {}
    g_score = {start: 0}
    visited_set = set()

    while not open_set.empty():
        current_node = open_set.get()
        visited_set.add(current_node.position)

        if current_node.position == goal:
            # Goal reached, reconstruct and return the path
            return reconstruct_path(came_from, current_node.position), visited_set

        for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_position = (current_node.position[0] + neighbor[0], current_node.position[1] + neighbor[1])

            if 0 <= neighbor_position[0] < columns and 0 <= neighbor_position[1] < rows and grid[neighbor_position[1]][neighbor_position[0]] != 'B':
                tentative_g_score = g_score[current_node.position] + 1

                if neighbor_position not in g_score or tentative_g_score < g_score[neighbor_position]:
                    # Update the g_score and add the neighbor to the priority queue
                    g_score[neighbor_position] = tentative_g_score
                    open_set.put(Node(neighbor_position, tentative_g_score, weight * heuristic_cost_estimate(neighbor_position, goal)))  # Include weight in the heuristic
                    came_from[neighbor_position] = current_node.position

    return None, visited_set
