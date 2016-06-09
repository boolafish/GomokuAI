class GomokuGame:
    def __init__(self, player1_cls, player2_cls):
        self._board = [['.'] * 15 for _ in range(15)]
        self.players = [player1_cls('b'), player2_cls('w')]
        self.moves = 0
        self._event_callback = None

    def start(self):
        while not self.is_final_state():
            move = self.current_player.think(self)

            # Check if the move is legal. If yes, update board.
            if self.is_legal_move(move):
                self._board[move[0]][move[1]] = self.current_player.stone_color
            else:
                raise Exception('Illegal!')

            if self._event_callback:
                me = MoveEvent(self.current_player.stone_color, move)
                self._event_callback(me)
            self.moves += 1
        print('GG')

    def get_current_board(self):
        """Return a copy of current board."""
        return tuple([tuple(row) for row in self._board])

    @property
    def current_player(self):
        return self.players[self.moves % 2]

    def is_final_state(self):
        # todo: implement this
        if not self.get_legal_moves():
            return True
        else:
            return False

    def get_legal_moves(self):
        moves = []
        for row in range(15):
            for col in range(15):
                if self._board[row][col] is '.':
                    moves.append((row, col))
        return moves

    def is_legal_move(self, move):
        # If None, the move is not occupied by any stone.
        if self._board[move[0]][move[1]] is '.':
            return True

    def set_event_callback(self, func):
        self._event_callback = func


class MoveEvent:
    def __init__(self, stone_color, move):
        self.stone_color = stone_color
        self.move = move
