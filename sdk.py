class Game:
    """
        A class to represent the game.
        On initialization, the user is prompted to input the board, and a solution will be printed.

    Attributes
    ----------
    INTRODUCTION : str
        the introduction to the game
    board : list
        the board
    possibilities : list
        the possibilities for each cell
    checkpoints : list
        the checkpoints

    Methods
    -------
    getBoard()
        Get the board from the user.
    printSolution()
        Print the solved board.
    getRow(y, matrix=None)
        Get a row from the board.
    getColumn(x, matrix=None)
        Get a column from the board.
    getBox(x, y, matrix=None)
        Get a box from the board.
    getCellPossibilities(x, y)
        Get the possibilities for a cell.
    getPotentialLocations(n, groupPossibilities)
        Get the potential locations for a number in a group.
    isSolved()
        Check if the board is solved.
    solveCells()
        Solve cells one at a time, once, by process of elimination.
    findMissingNumber(n, group, groupPossibilities)
        Find a missing number in a group.
    solveMissingNumbers()
        Solve missing numbers in groups.
    guess()
        Guess the first possibility of the first unresolved cell to be right, and save the current state in the likely case it was a bad guess.
    solve()
        Solve the board with multiple different algorithms (including blind trial and error).
    """

    INTRODUCTION = "Type in your sodoku. Like so:\n" + \
        "    1 0 0 0 0 0 0 0 0\n" + \
        "    0 2 0 0 0 0 0 0 0\n" + \
        "    0 0 3 0 0 0 0 0 0\n" + \
        "    0 0 0 0 0 4 0 0 0\n" + \
        "    0 0 0 0 5 0 0 0 0\n" + \
        "    0 0 0 6 0 0 0 0 0\n" + \
        "    0 0 0 0 0 0 7 0 0\n" + \
        "    0 0 0 0 0 0 0 8 0\n" + \
        "    0 0 0 0 0 0 0 0 9\n"
    
    def __init__(self) -> None:
        self.possibilities = [[[] for _ in range(9)] for _ in range(9)]
        self.checkpoints = []

        print(self.INTRODUCTION)
        # testing empty game
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.solve()
        self.printSolution()

    # I/O

    def getBoard(self) -> list:
        """
        Get the board from the user (0 represents a blank cell).

        Returns
        -------
        list
            a list of lists representing the board
        """
        board = []
        for _ in range(9):
            board.append(input(">>>    ").split(' '))

        for y in range(9):
            for x in range(9):
                board[y][x] = int(board[y][x])

        try:
            assert len(board) == 9
            for row in board:
                assert len(row) == 9

        except AssertionError:
            print("Invalid board.")
            return self.getBoard()

        return board
    
    def printSolution(self) -> None:
        """
        Print the solved board.
        """
        print("\nHere you go:")
        for y in range(9):
            for x in range(9):
                if not x: print()
                print(self.board[y][x], end=' ')

    # helper
    
    def getRow(self, y, matrix=None) -> list:
        """
        Get a row from the board.

        Parameters
        ----------
        y : int
            the row to get
        matrix : list, optional
            the matrix to get the row from (default is self.board)

        Returns
        -------
        list
            a list representing the row
        """
        if not matrix: matrix = self.board

        return matrix[y]
    
    def getColumn(self, x, matrix=None) -> list:
        """
        Get a column from the board.

        Parameters
        ----------
        x : int
            the column to get
        matrix : list, optional
            the matrix to get the column from (default is self.board)

        Returns
        -------
        list
            a list representing the column
        """
        if not matrix: matrix = self.board
        column = []
        for row in matrix:
            column.append(row[x])

        return column
    
    def getBox(self, x, y, matrix=None) -> list:
        """
        Get a box from the board.

        Parameters
        ----------
        x : int
            the x-coordinate of the box
        y : int
            the y-coordinate of the box
        matrix : list, optional
            the matrix to get the box from (default is self.board)

        Returns
        -------
        list
            a list representing the box
        """
        if not matrix: matrix = self.board

        square = []
        for yy in range(3):
            for xx in range(3):
                square.append(matrix[yy + y // 3 * 3][xx + x // 3 * 3])

        return square
    
    def getCellPossibilities(self, x, y) -> list:
        """
        Get the possibilities for a cell.

        Parameters
        ----------
        x : int
            the x-coordinate of the cell
        y : int
            the y-coordinate of the cell

        Returns
        -------
        list
            a list of possibilities for the cell
        """
        possibilities = []
        for n in range(1, 10):
            if n not in self.getRow(y) and n not in self.getColumn(x) and n not in self.getBox(x, y):
                possibilities.append(n)

        return possibilities

    def getPotentialLocations(self, n, groupPossibilities) -> list:
        """
        Get the potential locations for a number in a group.
        
        Parameters
        ----------
        n : int
            the number to find
        groupPossibilities : list
            the possibilities for the group

        Returns
        -------
        list
            a list of potential locations for the number
        """
        potentialLocations = []
        for x in range(9):
            if n in groupPossibilities[x]: potentialLocations.append(x)
        
        return potentialLocations

    def isSolved(self) -> bool:
        """
        Check if the board is solved.

        Returns
        -------
        bool
            whether the board is solved
        """
        for y in range(9):
            for x in range(9):
                if self.board[y][x] == 0: return False

        return True

    # solving algorithms
    
    def solveCells(self) -> bool:
        """
        Solve cells one at a time, once, by process of elimination (i.e. only one number can go in a cell).
        
        Returns
        -------
        bool
            whether any cells were solved
        """

        solvedAny = False

        # for each cell
        for y in range(9): 
            for x in range(9):

                # already solved
                if self.board[y][x] != 0: continue

                possibilities = self.getCellPossibilities(x, y)

                # guessed wrong
                if not possibilities: raise Exception("Wrong guess")

                # too many possibilities
                if len(possibilities) > 1:
                    self.possibilities[y][x] = possibilities
                    continue

                # solved                
                self.board[y][x] = possibilities[0]
                self.possibilities[y][x] = []
                solvedAny = True
        
        return solvedAny

    def findMissingNumber(self, n, group, groupPossibilities) -> int | None:
        """
        Find a missing number in a group.

        Parameters
        ----------
        n : int
            the number to find
        group : list
            the group to search
        groupPossibilities : list
            the possibilities for the group

        Returns
        -------
        int
            the location of the missing number
        """

        # not missing
        if n in group: return

        potentialLocations = self.getPotentialLocations(n, groupPossibilities)

        # guessed wrong
        if not potentialLocations: raise Exception("Wrong guess")
        
        # too many possibilities
        if len(potentialLocations) > 1: return

        # found solution
        return potentialLocations[0]

    def solveMissingNumbers(self) -> bool:
        """
        Solve missing numbers in groups (e.g. rows, columns, boxes).
        
        Returns
        -------
        bool
            whether any numbers were solved
        """

        solvedAny = False

        # for each potentially missing number
        for n in range(1, 10):

            # rows
            for y in range(9):
                solution = self.findMissingNumber(n, self.getRow(y), self.getRow(y, self.possibilities))
                if solution: 
                    self.board[y][solution] = n
                    self.possibilities[y][solution] = []
                    solvedAny = True

            # columns
            for x in range(9):
                solution = self.findMissingNumber(n, self.getColumn(x), self.getColumn(x, self.possibilities))
                if solution:
                    self.board[solution][x] = n
                    self.possibilities[solution][x] = []
                    solvedAny = True
            
            # boxes
            for y in range(0, 9, 3):
                for x in range(0, 9, 3):
                    solution = self.findMissingNumber(n, self.getBox(x, y), self.getBox(x, y, self.possibilities))
                    if solution: 
                        self.board[y + solution // 3][x + solution % 3] = n
                        self.possibilities[y + solution // 3][x + solution % 3] = []
                        solvedAny = True

        return solvedAny
    
    def guess(self) -> None:
        """
        Guess the first possibility of the first unresolved cell to be right, and save the current state in the likely case it was a bad guess.
        """

        # for each cell
        for y in range(9):
            for x in range(9):

                # already solved
                if self.board[y][x] != 0: continue
                
                # guessed wrong
                if not self.possibilities[y][x]: raise Exception("Wrong guess")

                # save current state minus the guess
                checkpointBoard = [row[:] for row in self.board]
                checkpointPossibilities = [[cell[:] for cell in row] for row in self.possibilities]
                checkpointPossibilities[y][x] = self.possibilities[y][x][1:]
                self.checkpoints.append((checkpointBoard, checkpointPossibilities))

                # make a guess
                self.board[y][x] = self.possibilities[y][x][0]
                self.possibilities[y][x] = []
                return
    
    def solve(self) -> None:
        """Solve the board with multiple different algorithms (including blind trial and error)."""
        skipToGuess = False # when a guess is wrong, try again

        while True:
            try:
                if not skipToGuess:
                    if self.solveCells(): continue
                    if self.solveMissingNumbers(): continue
                    if self.isSolved(): return

                else:
                    skipToGuess = False

                self.guess()

            except Exception:
                try:
                    self.board, self.possibilities = self.checkpoints.pop()
                
                except IndexError:
                    print("No solution found for this sudoku game.")
                    return
                
                skipToGuess = True



if __name__ == "__main__": Game()
