import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.mines = set()
        self.safes = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        return self.mines

    def known_safes(self):
        return self.safes

    def mark_mine(self, cell):
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)
            self.mines.add(cell)

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.safes.add(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        row, col = cell
        _neighbors = [
            (row+1, col),
            (row-1, col),
            (row, col-1),
            (row, col+1),
            (row+1, col+1),
            (row-1, col-1),
            (row+1, col-1),
            (row-1, col+1),
        ]
        neighbors = [n for n in _neighbors if (n not in self.safes) and n[0] > 0 and n[0] < self.width and n[1] > 0 and n[1] < self.height]
        sent = Sentence(neighbors, count)
        self.knowledge.append(sent)
        new_knowlege = []
        for info in self.knowledge:
            if info.cells.issubset(sent.cells):
                sent2 = sent
                sent1 = info
            elif sent.cells.issubset(info.cells):
                sent2 = info 
                sent1 = sent 
            else:
                continue 
            new_knowlege.append(Sentence(sent2.cells.difference(sent1.cells), sent2.count-sent1.count))
        self.knowledge += new_knowlege
        mines = []
        safes = []
        for knowledge in self.knowledge:
            if knowledge.count == len(knowledge.cells):
                for cell in knowledge.cells:
                    mines.append(cell)
            if knowledge.count == 0:
                for cell in knowledge.cells:
                    safes.append(cell)
        for c in mines:
            self.mark_mine(c)
        for c in safes:
            self.mark_safe(c)
        return

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        playable_safes = self.safes.difference(self.moves_made)
        if len(playable_safes) == 0:
            return None 
        return random.choice(tuple(playable_safes))

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible = set()
        for i in range(self.height):
            for j in range(self.width):
                possible.add((i,j))
        p = possible.difference(self.moves_made).difference(self.mines)
        return random.choice(tuple(p))
