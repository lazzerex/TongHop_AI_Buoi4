from easyAI import TwoPlayerGame, AI_Player, Human_Player, Negamax

class TicTacToe(TwoPlayerGame):
    def __init__(self, players):
        self.players = players
        self.board = [0] * 9
        self.current_player = 1  # Người chơi đầu tiên

    def possible_moves(self):
        return [i for i, v in enumerate(self.board) if v == 0]

    def make_move(self, move):
        self.board[move] = self.current_player

    def unmake_move(self, move):
        self.board[move] = 0

    def lose(self):
        """Kiểm tra nếu người chơi hiện tại thua"""
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # hàng ngang
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # hàng dọc
            [0, 4, 8], [2, 4, 6]              # đường chéo
        ]
        opponent = 3 - self.current_player
        return any(all(self.board[i] == opponent for i in line) for line in wins)
    
    def win(self):
        """Kiểm tra nếu người chơi hiện tại thắng"""
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        return any(all(self.board[i] == self.current_player for i in line) for line in wins)

    def is_over(self):
        return self.win() or self.lose() or not any(v == 0 for v in self.board)

    def show(self):
        symbols = ['.', 'X', 'O']
        print("\n  +---+---+---+")
        for i in range(3):
            row = " | ".join(symbols[self.board[3*i + j]] for j in range(3))
            print(f"  | {row} |")
            print("  +---+---+---+")
        
        current_symbol = symbols[self.current_player]
        print(f"Lượt người chơi {self.current_player} ('{current_symbol}')")
        print()

    def scoring(self):
        """Hàm đánh giá cho minimax"""
        if self.win():
            return 100  # Thắng
        if self.lose():
            return -100  # Thua
        return 0  # Hòa hoặc chưa kết thúc

if __name__ == "__main__":
    # Sử dụng Negamax với depth=9
    ai_algo = Negamax(9)
    
    print("Tic Tac Toe với Minimax và Alpha-Beta Pruning")
    print("Bạn là 'O', AI là 'X'")
    print("Nhập số từ 0-8 tương ứng với vị trí:")
    print("  0 | 1 | 2")
    print("  3 | 4 | 5")
    print("  6 | 7 | 8")
    print()
    
    # Tạo game với AI đi trước (player 1)
    game = TicTacToe([Human_Player(),AI_Player(ai_algo)])
    
    # Bắt đầu game
    game.play()
    print("Game over!")