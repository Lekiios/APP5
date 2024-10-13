fragments_txt_path = 'assets/fragments.txt'
fragments_s_txt_path = 'assets/fragments_s.txt'
solution_path = 'assets/solution.txt'

# Read files
def read_files():
    # Read fragments real position (use map to index correctly with any solution order)
    fragments = {}
    with open(fragments_txt_path, 'r') as f:
        for line in f:
            index, x, y, angle = map(float, line.split())
            fragments[int(index)] = ( x, y, angle)

    # Read solution
    solution = {}
    with open(solution_path, 'r') as f:
        for line in f:
            index, x, y, angle = map(float, line.split())
            solution[int(index)] = ( x, y, angle)

    # Read invalid fragments
    with open(fragments_s_txt_path, 'r') as f_s:
        invalid_fragments = set(map(int, f_s.readlines()))

    return fragments, solution, invalid_fragments

# Evaluate precision of solution file
def precision(fragments, solution, invalid_fragments, delta_x=1, delta_y=1, delta_r=1):
    total = len(fragments)
    found = 0

    for index, (x_sol, y_sol, r_sol) in solution.items():
        # If invalid fragment in solution -1
        if index in invalid_fragments:
            found -= 1

        # else check position and angle
        elif index in fragments:
            x, y, r = fragments[index]

            # If solution within the tolerance add to precision
            if abs(x_sol - x) <= delta_x and abs(y_sol - y) <= delta_y and abs(r_sol - r) <= delta_r:
                found += 1

    # Give precision between 0% - 100% (0.0 - 1.0)
    if found <= 0:
        return 0
    return found / total

# Read files
fragments, solution, invalid_fragments = read_files()

# Process precision (you can adjust tolerance with delta x / y / r)
precision = precision(fragments, solution, invalid_fragments, delta_x=1, delta_y=1, delta_r=1)

print(f'Precision of reconstruction: {precision:.3f}')
