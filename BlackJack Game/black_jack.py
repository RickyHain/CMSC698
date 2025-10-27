from Objects.Game import Game

game = Game(1,6, 500, 10)

wins =0
losses = 0

game.start_game()

#Make sure that my model is staying within +-10k after 5000 hands

for j in range(10):
    for i in range (500):
        game.reset_game()
    profit = game.player.get_proft()
    if profit >0:
        wins+=1
    else:
        losses +=1

print(f"Wins: {wins}   Losses: {losses}")
game.update_csv()