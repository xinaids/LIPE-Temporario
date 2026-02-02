from src.screens.players.players import PlayerScreen
from src.screens.home.home import HomeScreen 

if __name__ == "__main__":
    cadastro = PlayerScreen()
    jogadores = cadastro.Show() 

    if jogadores:  
        home = HomeScreen(jogadores)
        home.Show()  