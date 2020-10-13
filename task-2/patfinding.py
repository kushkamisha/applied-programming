from queue import PriorityQueue
import pygame


WIDTH = 800
ROWS = 50
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Path Finding')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


def read_file(filename):
    with open(filename, 'r') as f:
        n = int(f.readline().replace("\n", ""))

        num_of_lines = 0
        coordinates = []
        for line in f:
            x, y = line.split(" ")
            x = int(x)
            y = int(y)
            coordinates.append((x, y))
            num_of_lines += 1

        if num_of_lines != int(n):
            raise Exception("The number of elements is not {}".format(n))

    return coordinates


class Square:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color,
            (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # checks if a square exists and isn't a barrier
        # RIGHT
        if self.row < self.total_rows - 1 and \
                        not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # LEFT
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # UP
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

        # DOWN
        if self.col < self.total_rows - 1 and \
                        not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    """Heuristic function"""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, curr, _draw):
    while curr in came_from:
        curr = came_from[curr]
        curr.make_path()
        _draw()


def find_path(_draw, grid, start, end):
    """A* algorithm to find the shortest path between start and end"""
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # f-score, counter, starting square
    came_from = {}

    g_score = {square: float("inf") for row in grid for square in row}
    g_score[start] = 0
    f_score = {square: float("inf") for row in grid for square in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr = open_set.get()[2] # get square
        open_set_hash.remove(curr)

        if curr == end:
            reconstruct_path(came_from, end, _draw)
            start.make_start()
            end.make_end()
            return True

        for neighbor in curr.neighbors:
            tmp_g_score = g_score[curr] + 1

            if tmp_g_score < g_score[neighbor]:
                came_from[neighbor] = curr
                g_score[neighbor] = tmp_g_score
                f_score[neighbor] = tmp_g_score + \
                    h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        _draw()

        if curr != start:
            curr.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            square = Square(i, j, gap, rows)
            grid[i].append(square)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for square in row:
            square.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def draw_line_btwn_points(width, grid, x1, y1, x2, y2):
    num_of_steps = 100
    gap = width // ROWS
    cord_step_x = abs(x2 * gap - x1 * gap) * 1000 // num_of_steps
    cord_step_y = abs(y2 * gap - y1 * gap) * 1000 // num_of_steps
    flip_x_sign = -1
    flip_y_sign = -1

    if x2 < x1:
        flip_x_sign = 1

    if y2 < y1:
        flip_y_sign = 1

    for i in range(num_of_steps):
        row, col = get_clicked_pos((
            x1 * gap + (-1) * flip_x_sign * i * cord_step_x // 1000,
            y1 * gap + (-1) * flip_y_sign * i * cord_step_y // 1000
        ), ROWS, width)
        grid[row][col].make_barrier()


def main(win, width):
    coordinates = read_file('input/triangle.txt')
    grid = make_grid(ROWS, width)

    start = None
    end = None
    completed = False

    x_prev = None
    y_prev = None
    x_first = None
    y_first = None
    for (x, y) in coordinates:
        if (x_first is None and y_first is None):
            x_first = x
            y_first = y
        if (x_prev is not None and y_prev is not None):
            draw_line_btwn_points(width, grid, x, y, x_prev, y_prev)
        x_prev = x
        y_prev = y
        grid[x][y].make_barrier()

    draw_line_btwn_points(width, grid, x_prev, y_prev, x_first, y_first)

    while True:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            # is left ctrl is pressed
            isCtrl = pygame.key.get_pressed()[pygame.K_LCTRL]

            if event.type == pygame.QUIT:
                pygame.quit()

            # left mouse button
            elif pygame.mouse.get_pressed()[0] and not isCtrl:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                square = grid[row][col]

                if not start and square != end:
                    start = square
                    start.make_start()
                elif not end and square != start:
                    end = square
                    end.make_end()
                elif square != end and square != start:
                    square.make_barrier()
            # left mouse button + ctrl key
            elif pygame.mouse.get_pressed()[0] and isCtrl:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                square = grid[row][col]
                square.reset()

                if square == start:
                    start = None
                elif square == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE \
                    and start and end and not completed:
                    for row in grid:
                        for square in row:
                            square.update_neighbors(grid)

                    find_path(
                        lambda: draw(win, grid, ROWS, width),
                        grid, start, end
                    )
                    completed = True

                if event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    completed = False
                    grid = make_grid(ROWS, width)


if __name__ == "__main__":
    main(WIN, WIDTH)
