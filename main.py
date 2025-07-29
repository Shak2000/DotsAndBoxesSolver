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
        """Check if a square is complete (all 4 sides filled)"""
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

    def debug_check_square(self, x, y):
        """Debug method to check why a square isn't being captured"""
        if 0 <= y < self.height - 1 and 0 <= x < self.width - 1:
            print(f"\nDebugging square ({x}, {y}):")
            print(f"  Inner value: {self.inner[y][x]}")
            print(f"  Left vertical: {self.vertical[y][x]}")
            print(f"  Right vertical: {self.vertical[y][x + 1]}")
            print(f"  Top horizontal: {self.horizontal[y][x]}")
            print(f"  Bottom horizontal: {self.horizontal[y + 1][x]}")
            
            sides_filled = 0
            if self.vertical[y][x] != '*':
                sides_filled += 1
            if self.vertical[y][x + 1] != '*':
                sides_filled += 1
            if self.horizontal[y][x] != '*':
                sides_filled += 1
            if self.horizontal[y + 1][x] != '*':
                sides_filled += 1
            
            print(f"  Sides filled: {sides_filled}")
            print(f"  Should be captured: {sides_filled == 4}")
            print(f"  Current player: {self.player}")
        else:
            print(f"Invalid square coordinates ({x}, {y})")

    def debug_board_coordinates(self):
        """Debug method to show the coordinate system"""
        print("\nBoard coordinate system:")
        for y in range(self.height):
            for x in range(self.width):
                print(f"({x},{y})", end=" ")
            print()
        print("\nSquare coordinates (inner squares):")
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                print(f"({x},{y})", end=" ")
            print()

    def check_all_squares(self):
        """Check all squares and capture any that are complete"""
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                if self.inner[y][x] == '*':
                    # Count how many sides are filled
                    sides_filled = 0
                    if self.vertical[y][x] != '*':
                        sides_filled += 1
                    if self.vertical[y][x + 1] != '*':
                        sides_filled += 1
                    if self.horizontal[y][x] != '*':
                        sides_filled += 1
                    if self.horizontal[y + 1][x] != '*':
                        sides_filled += 1
                    
                    if sides_filled == 4:
                        self.inner[y][x] = self.player
                        if self.player == 'A':
                            self.A += 1
                        else:
                            self.B += 1

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

                # Check left square (if it exists)
                if 0 <= y < self.height - 1 and 0 <= x < self.width - 1:
                    if self.inner[y][x] == 'A':
                        self.A -= 1
                        self.inner[y][x] = '*'
                    elif self.inner[y][x] == 'B':
                        self.B -= 1
                        self.inner[y][x] = '*'

                # Check right square (if it exists)
                if 0 <= y < self.height - 1 and 0 <= x + 1 < self.width - 1:
                    if self.inner[y][x + 1] == 'A':
                        self.A -= 1
                        self.inner[y][x + 1] = '*'
                    elif self.inner[y][x + 1] == 'B':
                        self.B -= 1
                        self.inner[y][x + 1] = '*'

            elif direction == 'H':
                self.horizontal[y][x] = '*'
                self.remaining += 1

                # Check top square (if it exists)
                if 0 <= y < self.height - 1 and 0 <= x < self.width - 1:
                    if self.inner[y][x] == 'A':
                        self.A -= 1
                        self.inner[y][x] = '*'
                    elif self.inner[y][x] == 'B':
                        self.B -= 1
                        self.inner[y][x] = '*'

                # Check bottom square (if it exists)
                if 0 <= y + 1 < self.height - 1 and 0 <= x < self.width - 1:
                    if self.inner[y + 1][x] == 'A':
                        self.A -= 1
                        self.inner[y + 1][x] = '*'
                    elif self.inner[y + 1][x] == 'B':
                        self.B -= 1
                        self.inner[y + 1][x] = '*'

            return True
        return False

    def display(self):
        """Display the current game state"""
        print(f"\nPlayer A: {self.A} | Player B: {self.B} | Current Player: {self.player}")
        print(f"Remaining moves: {self.remaining}")
        print()
        
        # Display the game board
        for y in range(self.height):
            # Display dots and horizontal lines
            for x in range(self.width):
                print("•", end="")
                if x < self.width - 1:
                    print(f" {self.horizontal[y][x]} ", end="")
            print()
            
            # Display vertical lines and inner squares
            if y < self.height - 1:
                for x in range(self.width):
                    print(f"{self.vertical[y][x]}", end="")
                    if x < self.width - 1:
                        print(f" {self.inner[y][x]} ", end="")
                print()

    def debug_square(self, x, y):
        """Debug method to check the state of a specific square"""
        if 0 <= y < self.height - 1 and 0 <= x < self.width - 1:
            print(f"\nDebug square ({x}, {y}):")
            print(f"  Inner value: {self.inner[y][x]}")
            print(f"  Left vertical: {self.vertical[y][x]}")
            print(f"  Right vertical: {self.vertical[y][x + 1]}")
            print(f"  Top horizontal: {self.horizontal[y][x]}")
            print(f"  Bottom horizontal: {self.horizontal[y + 1][x]}")
            
            sides_filled = 0
            if self.vertical[y][x] != '*':
                sides_filled += 1
            if self.vertical[y][x + 1] != '*':
                sides_filled += 1
            if self.horizontal[y][x] != '*':
                sides_filled += 1
            if self.horizontal[y + 1][x] != '*':
                sides_filled += 1
            
            print(f"  Sides filled: {sides_filled}")
            print(f"  Should be captured: {sides_filled == 4}")
        else:
            print(f"Invalid square coordinates ({x}, {y})")

    def is_valid_vertical_move(self, x, y):
        """Check if a vertical move is valid"""
        return (0 <= y < self.height - 1 and 0 <= x < self.width and 
                self.vertical[y][x] == '*')

    def is_valid_horizontal_move(self, x, y):
        """Check if a horizontal move is valid"""
        return (0 <= y < self.height and 0 <= x < self.width - 1 and 
                self.horizontal[y][x] == '*')

    def get_valid_moves(self):
        """Get all valid moves as (x, y, direction) tuples"""
        moves = []
        
        # Vertical moves
        for y in range(self.height - 1):
            for x in range(self.width):
                if self.is_valid_vertical_move(x, y):
                    moves.append((x, y, 'V'))
        
        # Horizontal moves
        for y in range(self.height):
            for x in range(self.width - 1):
                if self.is_valid_horizontal_move(x, y):
                    moves.append((x, y, 'H'))
        
        return moves

    def make_move(self, x, y, direction):
        """Make a move and return True if successful"""
        if direction == 'V':
            if self.place_vertical(x, y):
                # Check for completed squares
                # Vertical line at (x,y) affects squares (x,y) and (x+1,y)
                if 0 <= y < self.height - 1 and 0 <= x < self.width - 1:
                    self.check_if_complete(x, y)
                if 0 <= y < self.height - 1 and 0 <= x + 1 < self.width - 1:
                    self.check_if_complete(x + 1, y)
                # Also check all squares to catch any missed ones
                self.check_all_squares()
                return True
        elif direction == 'H':
            if self.place_horizontal(x, y):
                # Check for completed squares
                # Horizontal line at (x,y) affects squares (x,y-1) and (x,y)
                # The line is between rows y and y+1, so it affects squares above and below
                if 0 <= y - 1 < self.height - 1 and 0 <= x < self.width - 1:
                    self.check_if_complete(x, y - 1)
                if 0 <= y < self.height - 1 and 0 <= x < self.width - 1:
                    self.check_if_complete(x, y)
                # Also check all squares to catch any missed ones
                self.check_all_squares()
                return True
        return False

    def debug_board_state(self):
        """Debug method to print the current board state"""
        print("\nDEBUG BOARD STATE:")
        print(f"Player A: {self.A}, Player B: {self.B}, Current Player: {self.player}")
        print("Vertical lines:")
        for y in range(self.height - 1):
            for x in range(self.width):
                print(f"V({x},{y}): {self.vertical[y][x]}", end=" ")
            print()
        print("Horizontal lines:")
        for y in range(self.height):
            for x in range(self.width - 1):
                print(f"H({x},{y}): {self.horizontal[y][x]}", end=" ")
            print()
        print("Inner squares:")
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                print(f"I({x},{y}): {self.inner[y][x]}", end=" ")
            print()
        print()

    def evaluate_position(self):
        """Evaluate the current position for minimax"""
        score = 0
        
        # Base score from captured squares (A is maximizer, B is minimizer)
        score += self.A * 10  # A's captured squares increase score
        score -= self.B * 10  # B's captured squares decrease score
        
        # Penalty for squares that can be captured by opponent next turn
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                if self.inner[y][x] == '*':
                    # Count how many sides are filled
                    sides_filled = 0
                    if self.vertical[y][x] != '*':
                        sides_filled += 1
                    if self.vertical[y][x + 1] != '*':
                        sides_filled += 1
                    if self.horizontal[y][x] != '*':
                        sides_filled += 1
                    if self.horizontal[y + 1][x] != '*':
                        sides_filled += 1
                    
                    # If 3 sides are filled, this square can be captured next turn
                    if sides_filled == 3:
                        if self.player == 'A':
                            score -= 5  # Penalty for A if B can capture
                        else:
                            score += 5  # Bonus for A if A can capture
        
        return score

    def copy(self):
        """Create a deep copy of the game state"""
        new_game = Game()
        new_game.height = self.height
        new_game.width = self.width
        new_game.player = self.player
        new_game.A = self.A
        new_game.B = self.B
        new_game.remaining = self.remaining
        
        # Deep copy arrays
        new_game.vertical = [row[:] for row in self.vertical]
        new_game.horizontal = [row[:] for row in self.horizontal]
        new_game.inner = [row[:] for row in self.inner]
        new_game.history = self.history[:]  # Shallow copy is fine for history
        
        return new_game

    def minimax(self, depth, alpha, beta, maximizing):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or self.remaining == 0:
            return self.evaluate_position()
        
        valid_moves = self.get_valid_moves()
        
        if maximizing:
            max_eval = float('-inf')
            for x, y, direction in valid_moves:
                # Create a copy of the game state
                game_copy = self.copy()
                
                # Make move on the copy
                game_copy.make_move(x, y, direction)
                game_copy.switch()
                
                # Recursive call
                eval = game_copy.minimax(depth - 1, alpha, beta, False)
                
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for x, y, direction in valid_moves:
                # Create a copy of the game state
                game_copy = self.copy()
                
                # Make move on the copy
                game_copy.make_move(x, y, direction)
                game_copy.switch()
                
                # Recursive call
                eval = game_copy.minimax(depth - 1, alpha, beta, True)
                
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, depth):
        """Get the best move for the current player using minimax"""
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None
            
        best_move = None
        best_value = float('-inf') if self.player == 'A' else float('inf')
        
        for x, y, direction in valid_moves:
            # Create a copy of the game state
            game_copy = self.copy()
            
            # Make move on the copy
            game_copy.make_move(x, y, direction)
            game_copy.switch()
            
            # Evaluate position from the perspective of the original player
            if self.player == 'A':
                value = game_copy.minimax(depth - 1, float('-inf'), float('inf'), False)
                if value > best_value:
                    best_value = value
                    best_move = (x, y, direction)
            else:
                value = game_copy.minimax(depth - 1, float('-inf'), float('inf'), True)
                if value < best_value:
                    best_value = value
                    best_move = (x, y, direction)
        
        return best_move


def main():
    print('Welcome to the Dots and Boxes solver!')
    
    game = Game()
    game_active = False
    
    while True:
        if not game_active:
            print("\n" + "="*50)
            print("MAIN MENU")
            print("="*50)
            print("1. Play a new game")
            print("2. Quit")
            
            choice = input("\nEnter your choice (1-2): ").strip()
            
            if choice == '1':
                try:
                    height = int(input("Enter board height (default 4): ") or "4")
                    width = int(input("Enter board width (default 4): ") or "4")
                    if height < 2 or width < 2:
                        print("Board dimensions must be at least 2x2!")
                        continue
                    game.create(height, width)
                    game_active = True
                    print(f"\nNew {width}x{height} game created!")
                except ValueError:
                    print("Invalid input! Please enter valid numbers.")
                    continue
            elif choice == '2':
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please enter 1 or 2.")
        else:
            print("\n" + "="*50)
            print("GAME MENU")
            print("="*50)
            game.display()
            print("\n1. Make a move")
            print("2. Let computer make a move")
            print("3. Undo a move")
            print("4. Restart the game")
            print("5. Quit the game")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                # User makes a move
                print("\nWhat type of move would you like to make?")
                print("1. Vertical line")
                print("2. Horizontal line")
                
                move_type = input("Enter your choice (1-2): ").strip()
                
                if move_type == '1':
                    try:
                        x = int(input("Enter x coordinate: "))
                        y = int(input("Enter y coordinate: "))
                        
                        if game.is_valid_vertical_move(x, y):
                            if game.make_move(x, y, 'V'):
                                game.switch()
                                print("Move successful!")
                            else:
                                print("Invalid move!")
                        else:
                            print("Invalid coordinates for vertical move!")
                    except ValueError:
                        print("Invalid input! Please enter valid numbers.")
                elif move_type == '2':
                    try:
                        x = int(input("Enter x coordinate: "))
                        y = int(input("Enter y coordinate: "))
                        
                        if game.is_valid_horizontal_move(x, y):
                            if game.make_move(x, y, 'H'):
                                game.switch()
                                print("Move successful!")
                            else:
                                print("Invalid move!")
                        else:
                            print("Invalid coordinates for horizontal move!")
                    except ValueError:
                        print("Invalid input! Please enter valid numbers.")
                else:
                    print("Invalid choice! Please enter 1 or 2.")
                    
            elif choice == '2':
                # Computer makes a move
                try:
                    depth = int(input("Enter search depth for computer move: "))
                    if depth < 1:
                        print("Depth must be at least 1!")
                        continue
                    
                    print("Computer is thinking...")
                    best_move = game.get_best_move(depth)
                    
                    if best_move:
                        x, y, direction = best_move
                        if game.make_move(x, y, direction):
                            print(f"Computer placed a {direction.lower()} line at ({x}, {y})")
                            game.switch()
                        else:
                            print("Computer made an invalid move!")
                    else:
                        print("No valid moves available!")
                except ValueError:
                    print("Invalid input! Please enter a valid number.")
                    
            elif choice == '3':
                # Undo a move
                if game.undo():
                    game.switch()
                    print("Move undone!")
                else:
                    print("No moves to undo!")
                    
            elif choice == '4':
                # Restart the game
                game_active = False
                print("Game restarted!")
                
            elif choice == '5':
                # Quit the game
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice! Please enter 1-5.")
            
            # Check if game is over
            winner = game.get_winner()
            if winner != 'Undecided':
                game.display()
                print(f"\nGame Over! Winner: {winner}")
                game_active = False


if __name__ == "__main__":
    main()
