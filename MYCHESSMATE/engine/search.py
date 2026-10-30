import chess
import random
from engine.evaluation import evaluate_board

class ChessAI:
    def __init__(self, difficulty="Medium"):
        self.difficulty = difficulty
        if difficulty == "Easy":
            self.depth = 1
        elif difficulty == "Medium":
            self.depth = 2
        else:
            self.depth = 4

    def get_best_move(self, board: chess.Board) -> chess.Move:
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        # Easy difficulty occasionally introduces variance for a human feel
        if self.difficulty == "Easy" and len(legal_moves) > 1 and random.random() < 0.25:
            return random.choice(legal_moves)

        best_move = None
        best_value = -float('inf') if board.turn == chess.WHITE else float('inf')
        alpha = -float('inf')
        beta = float('inf')
        
        # Order captures first for better alpha-beta pruning efficiency
        legal_moves.sort(key=lambda m: board.is_capture(m), reverse=True)

        for move in legal_moves:
            board.push(move)
            value = self.alphabeta(board, self.depth - 1, alpha, beta, not board.turn)
            board.pop()
            
            if board.turn == chess.WHITE:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, value)
                
        return best_move if best_move else legal_moves[0]

    def alphabeta(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizing: bool) -> int:
        if depth == 0 or board.is_game_over():
            return evaluate_board(board)
            
        legal_moves = list(board.legal_moves)
        legal_moves.sort(key=lambda m: board.is_capture(m), reverse=True)

        if maximizing:
            max_eval = -float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.alphabeta(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.alphabeta(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval