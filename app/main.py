class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self,
                 start: tuple,
                 end: tuple,
                 is_drowned: bool = False) -> None:
        # Create decks and save them to a list `self.decks`
        self.is_drowned = is_drowned
        self.decks = [
            Deck(row, column)
            for row in range(start[0], end[0] + 1)
            for column in range(start[1], end[1] + 1)]

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if row == deck.row and column == deck.column:
                return deck

    def fire(self, row: int, column: int) -> None:
        # Change the `is_alive` status of the deck
        # And update the `is_drowned` value if it's needed
        self.get_deck(row, column).is_alive = False
        if any([deck.is_alive for deck in self.decks]) is False:
            self.is_drowned = True


class Battleship:
    def __init__(self, ships: list[tuple]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for start, end in ships:
            cords = [
                (row, column)
                for row in range(start[0], end[0] + 1)
                for column in range(start[1], end[1] + 1)]
            ship = Ship(start, end)
            for cord in cords:
                self.field[cord] = ship
        self._validate_input(ships)

    def fire(self, location: tuple) -> str:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        ship = self.field.get(location)
        if ship:
            ship.fire(*location)
            if ship.is_drowned is True:
                return "Sunk!"
            else:
                return "Hit!"
        else:
            return "Miss!"

    def print_field(self) -> None:
        for row in range(9 + 1):
            for column in range(9 + 1):
                ship = self.field.get((row, column))
                if ship:
                    deck = ship.get_deck(row, column)
                    if ship.is_drowned:
                        print(" X ", end="")
                        continue
                    elif deck.is_alive:
                        print(u" \u25A1 ", end="")
                    else:
                        print(" * ", end="")
                else:
                    print(" ~ ", end="")
            print("")

    def _validate_input(self, ships: list[tuple]) -> None:
        if len(ships) < 10:
            raise ValueError(f"Count of ships should be"
                             f"equal 10, got {len(ships)} instead")
        single = 0
        double = 0
        triple = 0
        quadro = 0
        ships = list(self.field.values())
        for ship in set(ships):
            if ships.count(ship) == 1:
                single += 1
            elif ships.count(ship) == 2:
                double += 1
            elif ships.count(ship) == 3:
                triple += 1
            elif ships.count(ship) == 4:
                quadro += 1
        if [single, double, triple, quadro] != [4, 3, 2, 1]:
            raise ValueError(f"There should be: \n"
                             f"4 one-deck ships, got {single} instead\n"
                             f"3 double-deck ships, got {double} instead\n"
                             f"2 three-deck ships, got {triple} instead\n"
                             f"1 four-deck ship, got {quadro} instead")
        for cord, ship in self.field.items():
            row, column = cord
            column -= 1
            self._check_ceil(row, column, ship)
            row -= 1
            self._check_ceil(row, column, ship)
            column += 1
            self._check_ceil(row, column, ship)
            column += 1
            self._check_ceil(row, column, ship)
            row += 1
            self._check_ceil(row, column, ship)
            row += 1
            self._check_ceil(row, column, ship)
            column -= 1
            self._check_ceil(row, column, ship)
            column -= 1
            self._check_ceil(row, column, ship)

    def _check_ceil(self, row: int, column: int, ship: Ship) -> None:
        if (self.field.get((row, column))
                and self.field.get((row, column)) != ship):
            raise ValueError("Ships cannot be in neighboring cells"
                             "(even if cells are neighbors by diagonal)")
