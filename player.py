import random
import time
from threading import Event


class GomokuPlayer:
    def __init__(self, stone_color):
        if stone_color.lower() not in ['w', 'b']:
            raise Exception('stone_color should be "w" or "b"')
        self.stone_color = stone_color.lower()

    def think(self, game):
        """Return next move."""
        return None


class GuiPlayer(GomokuPlayer):
    def __init__(self, *args, **kwargs):
        super(GuiPlayer, self).__init__(*args, **kwargs)
        self._move_event = Event()
        self._next_move = None

    def think(self, game):
        # wait until move event set
        self._move_event.clear()
        self._move_event.wait()
        self._move_event.clear()
        return self._next_move

    def make_move(self, move):
        self._next_move = move
        self._move_event.set()


class RandomAIPlayer(GomokuPlayer):
    def think(self, game):
        time.sleep(0.1)
        return random.choice(game.get_legal_moves())

