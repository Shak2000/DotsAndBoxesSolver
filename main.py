class Game:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.player = 'A'

        self.vertical = []
        self.horizontal = []
        self.inner = []
        self.A = 0
        self.B = 0

        self.remaining = 0
        self.history = []

    def create(self, height: int = 4, width: int = 4):
        self.height = height
        self.width = width
        self.player = 'A'

        self.vertical = [['*' for j in range(width)] for i in range(height - 1)]
        self.horizontal = [['*' for j in range(width - 1)] for i in range(height)]
        self.inner = [['*' for j in range(width - 1)] for i in range(height - 1)]
        self.A = 0
        self.B = 0

        self.remaining = width * (height - 1) + height * (width - 1)
        self.history = []

    def switch(self):
        if self.player == 'A':
            self.player = 'B'
        else:
            self.player = 'A'

    def check_if_complete(self, x, y):
        if (0 <= y < self.height - 1 and 0 <= x < self.width - 1 and self.inner[y][x] == '*'
                and self.vertical[y][x] != '*' and self.vertical[y][x + 1] != '*'
                and self.horizontal[y][x] != '*' and self.horizontal[y + 1][x] != '*'):
            self.inner[y][x] = self.player

            if self.player == 'A':
                self.A += 1
            else:
                self.B += 1
            return True

        return False

    def place_vertical(self, x, y):
        if 0 <= y < self.height - 1 and 0 <= x < self.width:
            self.history.append((x, y, 'V'))
            self.vertical[y][x] = '|'
            self.remaining -= 1

            return True
        return False

    def place_horizontal(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width - 1:
            self.history.append((x, y, 'H'))
            self.horizontal[y][x] = '—'
            self.remaining -= 1

            return True
        return False

    def get_winner(self):
        if self.remaining > 0:
            return 'Undecided'

        elif self.A > self.B:
            return 'A'

        elif self.B > self.A:
            return 'B'

        else:
            return 'Tie'

    def undo(self):
        if len(self.history) > 0:
            x, y, direction = self.history.pop()

            if direction == 'V':
                self.vertical[y][x] = '*'
                self.remaining += 1

                if self.inner[y][x] == 'A':
                    self.A -= 1
                    self.inner[y][x] = '*'

                elif self.inner[y][x] == 'B':
                    self.B -= 1
                    self.inner[y][x] = '*'

                if self.inner[y][x + 1] == 'A':
                    self.A -= 1
                    self.inner[y][x + 1] = '*'

                elif self.inner[y][x + 1] == 'B':
                    self.B -= 1
                    self.inner[y][x + 1] = '*'

            elif direction == 'H':
                self.horizontal[y][x] = '*'
                self.remaining += 1

                if self.inner[y][x] == 'A':
                    self.A -= 1
                    self.inner[y][x] = '*'

                elif self.inner[y][x] == 'B':
                    self.B -= 1
                    self.inner[y][x] = '*'

                if self.inner[y + 1][x] == 'A':
                    self.A -= 1
                    self.inner[y + 1][x] = '*'

                elif self.inner[y + 1][x] == 'B':
                    self.B -= 1
                    self.inner[y + 1][x] = '*'

            return True
        return False

def main():
    print('Welcome to the Dots and Boxes solver!')


if __name__ == "__main__":
    main()
