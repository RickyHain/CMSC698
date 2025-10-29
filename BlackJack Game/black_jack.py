from Objects.Game import Game

game = Game(1,6, 500, 10)

wins =0
losses = 0

game.start_game()

for j in range(500):
    for i in range (1000):
        game.reset_game()
    profit = game.player.get_proft()
    if profit >0:
        wins+=1
    else:
        losses +=1
    

    print (f"profit: {profit}")
    game.reset_player()

print(f"Wins: {wins}   Losses: {losses}")
# game.count_debug()
# game.update_csv()