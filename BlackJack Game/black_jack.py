from Objects.Game import Game

game = Game("ch",6, 500, 10)

wins = 0
losses = 0

game.start_game()

for j in range(20):
    for i in range (100000):
        game.reset_game() 
    profit = game.player.get_proft()

    if profit >0:
        wins+=1
    else:
        losses +=1
    

    game.reset_player()
    print (f"profit: {profit}")

print(f"Wins: {wins}   Losses: {losses}")
# game.count_debug()
game.update_csv()