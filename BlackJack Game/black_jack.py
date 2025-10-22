from Objects.Game import Game

game = Game(1,6, 500, 10)

game.start_game()

for i in range (500):
    game.reset_game()