from game import GomokuGame
from player import GuiPlayer, RandomAIPlayer, ReinforceAIPlayer, GuiTestPlayer

game = GomokuGame(ReinforceAIPlayer, ReinforceAIPlayer)
game.start()
