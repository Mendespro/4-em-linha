import xmlrpc.client
import os
import time

# Função para imprimir o tabuleiro
def print_grid(grid):
    for row in grid:
        print('|'.join(row))
    print('---------------')
    print(' 1 2 3 4 5 6 7')

# Função principal do cliente
def main():
    os.system('cls')
    # Conecta-se ao servidor XML-RPC
    server = xmlrpc.client.ServerProxy('http://localhost:8000')
    print("Bem-vindo ao Connect 4!")
    
    # Registra o jogador
    try:
        player = server.register_player()
        print(f"Você é o jogador {player}.")
    except Exception as e:
        print("Erro ao registrar o jogador:", e)
        return

    while True:
        try:
            # Obtém o estado atual do tabuleiro do servidor
            grid = server.get_grid()
            # Imprime o tabuleiro
            os.system('cls')
            print_grid(grid)

            # Verifica de quem é a vez
            current_player = server.get_current_player()
            if current_player != player:
                print(f"A vez do jogador {current_player}. Aguarde sua vez.")
                time.sleep(0.1)
                continue

            print(f"Sua vez de jogar {current_player}!")
            # Solicita ao jogador que escolha uma coluna
            column = int(input("Escolha uma coluna (1-7): ")) - 1
            # Faz a jogada no servidor
            server.make_move(player, column)
            
            # Verifica se há um vencedor
            winner = server.check_winner()
            if winner:
                # Se houver um vencedor, imprime o tabuleiro e o vencedor e termina o jogo
                print_grid(server.get_grid())
                print(f"Voce venceu!")
                break
            
            # Verifica se o jogo terminou em empate
            draw = server.check_draw()
            if draw:
                # Se o jogo terminou em empate, imprime o tabuleiro e uma mensagem de empate e termina o jogo
                print_grid(server.get_grid())
                print("O jogo terminou em empate!")
                break
        
        except Exception as e:
            # Captura e imprime qualquer exceção ocorrida durante o jogo
            print("Erro:", e)

if __name__ == "__main__":
    main()