from typing import Set, Dict

from CSP import CSP, Variable, Value


class Sudoku(CSP):
    def __init__(self, MRV=True, LCV=True):
        super().__init__(MRV=MRV, LCV=LCV)
        self._variables = set()
        self._matrix = []

        for x in range(9):
            temp = []
            for y in range(9):
                var = Cell(x, y)
                temp.append(var)
                self._variables.add(var)
            self._matrix.append(temp)

    @property
    def variables(self) -> Set['Cell']:
        """ Return the set of variables in this CSP. """
        return self._variables

    def getCell(self, x: int, y: int) -> 'Cell':
        """ Get the  variable corresponding to the cell on (x, y) """
        return self._matrix[x][y]

    def neighbors(self, var: 'Cell') -> Set['Cell']:
        """ Return all variables related to var by some constraint. """
        return self._variables - {var}
        # neighbors = set()
        #
        # x, y = var.row , var.colum
        # for i in range(9):
        #     if self.getCell(x, i) != var:
        #         neighbors.add(self.getCell(x, i))  # Colum
        #     if self.getCell(i, y) != var:
        #         neighbors.add(self.getCell(i, y))  # Row
        #
        # x, y = y // 3, x // 3
        # for i in range(3):
        #     for j in range(3):
        #         tvar = self.getCell(3 * x + j, 3 * y + i)
        #         if tvar != var:
        #             neighbors.add(tvar)
        # return neighbors

    def isValidPairwise(self, var1: 'Cell', val1: Value, var2: 'Cell', val2: Value) -> bool:
        """ Return whether this pairwise assignment is valid with the constraints of the csp. """
        if ( (var1.row == var2.row) or (var1.colum == var2.colum) or (var1.block == var2.block) ) and val1 == val2:
            return False
        return True

    def assignmentToStr(self, assignment: Dict['Cell', Value]) -> str:
        """ Formats the assignment of variables for this CSP into a string. """
        s = ""
        for y in range(9):
            if y != 0 and y % 3 == 0:
                s += "---+---+---\n"
            for x in range(9):
                if x != 0 and x % 3 == 0:
                    s += '|'

                cell = self.getCell(x, y)
                s += str(assignment.get(cell, ' '))
            s += "\n"
        return s

    def parseAssignment(self, path: str) -> Dict['Cell', Value]:
        """ Gives an initial assignment for a Sudoku board from file. """
        initialAssignment = dict()

        with open(path, "r") as file:
            for y, line in enumerate(file.readlines()):
                if line.isspace():
                    continue
                assert y < 9, "Too many rows in sudoku"

                for x, char in enumerate(line):
                    if char.isspace():
                        continue

                    assert x < 9, "Too many columns in sudoku"

                    var = self.getCell(x, y)
                    val = int(char)

                    if val == 0:
                        continue

                    assert val > 0 and val < 10, f"Impossible value in grid"
                    initialAssignment[var] = val
        return initialAssignment

class Cell(Variable):
    def __init__(self, x , y):
        super().__init__()
        self.row = x
        self.colum = y
        self.block = (self.colum // 3) + (self.row // 3) * 3

    @property
    def startDomain(self) -> Set[Value]:
        """ Returns the set of initial values of this variable (not taking constraints into account). """
        return set(range(1, 10))
