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
            Deck(column, row)
            for column in range(start[0], end[0] + 1)
            for row in range(start[1], end[1] + 1)]

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
    def __init__(self, ships: list[tuple[tuple]]) -> None:
        # Create a dict `self.field`.
        # Its keys are tuples - the coordinates of the non-empty cells,
        # A value for each cell is a reference to the ship
        # which is located in it
        self.field = {}
        for start, end in ships:
            cords = [
                (column, row)
                for column in range(start[0], end[0] + 1)
                for row in range(start[1], end[1] + 1)]
            ship = Ship(start, end)
            for cord in cords:
                self.field[cord] = ship

    def fire(self, location: tuple) -> None:
        # This function should check whether the location
        # is a key in the `self.field`
        # If it is, then it should check if this cell is the last alive
        # in the ship or not.
        ship = self.field.get(location)
        if ship:
            ship.fire(*location)
            if ship.is_drowned is True:
                print("Sunk!")
            else:
                print("Hit!")
        else:
            print("Miss!")

    def print_field(self) -> None:
        for column in range(9 + 1):
            for row in range(9 + 1):
                ship = self.field.get((column, row))
                if ship:
                    deck = ship.get_deck(column, row)
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


# ships = [
#     ((0, 0), (0, 3)),
#     ((0, 5), (0, 6)),
#     ((0, 8), (0, 9)),
#     ((2, 0), (4, 0)),
#     ((2, 4), (2, 6)),
#     ((2, 8), (2, 9)),
#     ((9, 9), (9, 9)),
#     ((7, 7), (7, 7)),
#     ((7, 9), (7, 9)),
#     ((9, 7), (9, 7)),
#
# ]
#
#
# battle = Battleship(ships)
# battle.print_field()
# battle.fire((2, 0))
# battle.fire((3, 0))
# battle.fire((4, 0))
# battle.print_field()
