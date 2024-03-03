import heapq
import math

def greedy_best_first_search(grid, start, goal):
    # Get the number of rows and columns in the grid
    rows, columns = len(grid), len(grid[0])

    # Initialize a set to keep track of visited positions
    visited = set()

    # Initialize a priority queue to store positions and their costs
    priority_queue = []

    # Dictionary to store the parent position of each position in the path
    came_from = {}

    # Push the start position with cost 0 into the priority queue
    heapq.heappush(priority_queue, (0, start))

    # Euclidean heuristic function to estimate the cost from a position to the goal
    def heuristic(position):
        return math.sqrt((position[0] - goal[0]) ** 2 + (position[1] - goal[1]) ** 2) + obstacle_cost(position)

    # determine the cost associated with obstacles at a position
    def obstacle_cost(position):
        x, y = position
        return math.inf if grid[y][x] == 'B' else 0  # Use infinity as the obstacle cost

    # determine the sorting order in the priority queue
    def sort_key(neighbor):
        x, y = neighbor
        heuristic_value = heuristic(neighbor)
        movement_priority = {(0, -1): 1, (-1, 0): 2, (0, 1): 3, (1, 0): 4}
        return (heuristic_value, movement_priority.get(neighbor, 5), x, y)

    # Main loop
    while priority_queue:
        current_cost, current_position = heapq.heappop(priority_queue)

        # If the current position is the goal, reconstruct the path and return it
        if current_position == goal:
            path = reconstruct_path(current_position, came_from)
            return path, visited

        # If the current position is not visited, mark it as visited
        if current_position not in visited:
            visited.add(current_position)

            # Get the neighbors of the current position
            neighbors = get_neighbors(current_position, grid, rows, columns)

            # Sort the neighbors based on the sort_key function
            neighbors.sort(key=sort_key)

            # Explore each neighbor and add it to the priority queue
            for neighbor_position in neighbors:
                if neighbor_position not in visited:
                    neighbor_cost = current_cost + heuristic(neighbor_position)
                    heapq.heappush(priority_queue, (neighbor_cost, neighbor_position))
                    came_from[neighbor_position] = current_position

    return None, visited

# Function to reconstruct the path from the goal to the start using the came_from dictionary
def reconstruct_path(goal, came_from):
    path = [goal]
    while came_from.get(path[-1]):
        path.append(came_from[path[-1]])
    return path[::-1]

# Function to get the neighbors of a position in the grid
def get_neighbors(position, grid, rows, columns):
    neighbors = []
    for move in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        neighbor_position = (position[0] + move[0], position[1] + move[1])
        if 0 <= neighbor_position[0] < columns and 0 <= neighbor_position[1] < rows:
            neighbors.append(neighbor_position)
    return neighbors



