from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import os

# Classe para manipular requisições XML-RPC
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Classe que representa o servidor do Connect Four
class ConnectFourServer:
    def __init__(self):
        # Inicializa o tabuleiro vazio e define o jogador atual e o vencedor
        self.grid = [[' ' for _ in range(7)] for _ in range(6)]
        self.players = []
        self.current_player = None
        self.winner = None

    # Método para registrar um jogador
    def register_player(self):
        if len(self.players) < 2:
            player = 'X' if len(self.players) == 0 else 'O'
            self.players.append(player)
            if not self.current_player:
                self.current_player = player
            return player
        else:
            raise Exception("Dois jogadores já estão inscritos.")

    # Método para obter o estado atual do tabuleiro
    def get_grid(self):
        return self.grid

    # Método para obter o jogador atual
    def get_current_player(self):
        return self.current_player

    # Método para fazer uma jogada em uma coluna específica
    def make_move(self, player, column):
        # Verifica se o jogo já terminou
        if self.winner:
            raise Exception("O jogo acabou.")
        # Verifica se é a vez do jogador
        if player != self.current_player:
            raise Exception("Não é sua vez de jogar")
        # Verifica se a coluna é válida
        if not 0 <= column < 7:
            raise ValueError("Coluna inválida.")
        # Encontra a próxima linha vazia na coluna e faz a jogada
        for i in range(5, -1, -1):
            if self.grid[i][column] == ' ':
                self.grid[i][column] = player
                # Verifica se a jogada resultou em vitória
                if self.check_winner():
                    self.winner = player
                else:
                    # Alterna o jogador atual
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
                return
        # Se a coluna estiver cheia, levanta uma exceção
        raise ValueError("Coluna completa.")

    # Método para verificar se há um vencedor
    def check_winner(self):
        # Verifica todas as possíveis configurações de vitória no tabuleiro
        for row in self.grid:
            for j in range(4):
                if row[j] == row[j + 1] == row[j + 2] == row[j + 3] != ' ':
                    return True

        for j in range(7):
            for i in range(3):
                if self.grid[i][j] == self.grid[i + 1][j] == self.grid[i + 2][j] == self.grid[i + 3][j] != ' ':
                    return True

        for i in range(3):
            for j in range(4):
                if self.grid[i][j] == self.grid[i + 1][j + 1] == self.grid[i + 2][j + 2] == self.grid[i + 3][j + 3] != ' ':
                    return True
                if self.grid[i][j + 3] == self.grid[i + 1][j + 2] == self.grid[i + 2][j + 1] == self.grid[i + 3][j] != ' ':
                    return True

        return False

    # Método para verificar se o jogo terminou em empate
    def check_draw(self):
        return all(self.grid[0][j] != ' ' for j in range(7))

# Função principal do servidor
def main():
    os.system('cls')
    # Configura e inicia o servidor XML-RPC
    server = SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler, allow_none=True)
    server.register_instance(ConnectFourServer())
    print("Connect 4 server em funcionamento...")
    server.serve_forever()

if __name__ == "__main__":
    main()