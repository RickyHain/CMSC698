from Objects.Game import Game

game = Game(1,6, 100, 10)

wins =0
losses = 0

game.start_game()

for j in range(1):
    for i in range (500000):
        game.reset_game()
    profit = game.player.get_proft()
    if profit >0:
        wins+=1
    else:
        losses +=1

    print (f"profit: {profit}")
    game.reset_player()

print(f"Wins: {wins}   Losses: {losses}")
game.update_csv()