import math
import ast

def thief_and_cops(grid, orientations, fov):
    # Fn to Calculate the range for cop's field of view
    def is_within_fov(cop_orientation, fov, angle):                 
        half_fov = fov / 2
        lower_bound = (cop_orientation - half_fov) % 360
        upper_bound = (cop_orientation + half_fov) % 360

        if lower_bound < upper_bound:
            return lower_bound < angle < upper_bound
        else:                                                       # Special Case: Handles cases when upper bound exceeds 360 degrees 
            return angle > lower_bound or angle < upper_bound                  

    # Fn to look for positions of Cops and Thiefs on the grid
    def find_positions(grid):                                       
        cop_position = {}
        thief_position = None
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if isinstance(cell, int) and cell != 0:             # Way to find a non-zero integer
                    cop_position[cell] = (i, j)
                elif cell == T:
                    thief_position = (i, j)            
        return cop_position, thief_position

    # Fn to map the visbility of the cop(s)
    def cop_visibility_map(grid, orientations, FoV):
        cop_positions, thief_position = find_positions(grid)
        if thief_position is None:                                  # Where is thief?
            raise ValueError("Thief ran away? Can't find thief if there is no thief to find. Result: [],[]")
        visible_cells = {cop_id: set() for cop_id in cop_positions} # Dictionary to store visible cells for each cop
        visible_thief = []

        sorted_cop_positions = sorted(cop_positions.items())        # Sorting cop positions by cop IDs
        for index, (cop_id, (cop_x, cop_y)) in enumerate(sorted_cop_positions):
            # Accessing orientations and fovs by indices
            cop_orientation = orientations[index]
            fov = FoV[index]
            cop_center = (cop_x + 0.5, cop_y + 0.5)

            if fov < 0 or fov > 360:                                # Special case: Handles abnormal FoV values
                print("Cops are great but they can't be that good.")
                continue
            elif fov == 0:
                continue

            visible_cells[cop_id].add((cop_x, cop_y))               # Marking the cell the cop is on as visible   
            max_distance = max(len(grid), len(grid[0]))             # Max range of grid size
            for dx in range(-max_distance, max_distance + 1):
                for dy in range(-max_distance, max_distance + 1):
                    cell_x, cell_y = cop_x + dx, cop_y + dy

                    if not (0 <= cell_x < len(grid) and 0 <= cell_y < len(grid[0])):    # Skip cells outside the given grid
                        continue                                    
                    
                    # All corners of a cell for detection
                    corners = [
                        (cell_x, cell_y), 
                        (cell_x, cell_y + 1), 
                        (cell_x + 1, cell_y), 
                        (cell_x + 1, cell_y + 1)
                    ]
                    for corner in corners:
                        angle = math.degrees(math.atan2(-(corner[0] - cop_center[0]), (corner[1] - cop_center[1]))) % 360  # Slope calculation

                        if is_within_fov(cop_orientation, fov, angle):      # Break if any of the corners are already visible
                            visible_cells[cop_id].add((cell_x, cell_y))
                            break

            if thief_position in visible_cells[cop_id]:                     # If thief is on any of the visible cells of the cop in check.
                visible_thief.append(cop_id)

        return visible_cells, visible_thief, thief_position

    # Fn to find the closest safe cell
    def find_closest_safe_cell(thief_position, visible_cells, grid):        
        q = [(thief_position, 0)]
        visited = set()                                         # To avoid redundant pre-checked cells.
        visited.add(thief_position)

        while q:
            (x, y), distance = q.pop(0)

            is_safe = True
            for cells in visible_cells.values():                # Safe checks
                if (x, y) in cells:
                    is_safe = False
                    break

            if is_safe:                                         # If cell at question is safe
                return [x, y]

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:   # Continue exploring
                new_x, new_y = x + dx, y + dy
                new_position = (new_x, new_y)

                # Check if cell has been visited
                if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and new_position not in visited:
                    visited.add(new_position)
                    q.append((new_position, distance + 1))

        return None                 # No safe cell found for this distance/cost                                             

    
    
    
    # Visiblity map for cop(s) and their sight on thief 
    visible_cells, visible_thief, thief_position = cop_visibility_map(grid, orientations, fov)
    closest_safe_cell = find_closest_safe_cell(thief_position, visible_cells, grid)
    
    return visible_thief, closest_safe_cell

    

T = 'T'                             # When the Thief T in grid is not a string

""""""""" Input """""""""
# # Sample Input
# # Uncomment to run it manually.
# grid = [[0, 0, 0, 0, 0],[T, 0, 0, 0, 2],[0, 0, 0, 0, 0],[0, 0, 1, 0, 0],[0, 0, 0, 0, 0]]
# orientations = [180, 150] 
# fov = [60, 60]

# Comment to run manually.
grid = ast.literal_eval(input("Please enter the grid: ").replace("T", "'T'"))
orientations = ast.literal_eval(input("Please enter the orientations: "))
fov = ast.literal_eval(input("Please enter the FoV values: "))

""""""""" Result """""""""
result = thief_and_cops(grid, orientations, fov)
print("Result: "f"{result[0]} , {result[1]}")
