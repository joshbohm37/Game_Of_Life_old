import random

def gen_grid(size):
    grid = []

    for row in range(size):
        tmp_row = []

        for col in range(size):
            # tmp_row.append(random.choices([0, 1], [3, 1])[0])
            tmp_row.append(0)

        grid.append(tmp_row)

    return grid

