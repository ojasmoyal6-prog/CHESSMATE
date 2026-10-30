import chess
from engine.evaluation import evaluate_board

class GameAnalyzer:
    def __init__(self, pgn_game):
        self.game = pgn_game

    def analyze_game(self):
        board = self.game.board()
        analysis_results = []
        
        eval_before = evaluate_board(board)
        move_num = 1
        
        for node in self.game.mainline():
            move = node.move
            # Simple engine lookahead for best move & evaluation
            from engine.search import ChessAI
            ai = ChessAI("Medium")
            best_move = ai.get_best_move(board)
            
            board.push(move)
            eval_after = evaluate_board(board)
            
            diff = eval_after - eval_before if board.turn == chess.BLACK else eval_before - eval_after
            
            classification = "🟢 Good"
            explanation = "Solid move maintaining position."
            
            if diff < -300:
                classification = "🔴 Blunder"
                explanation = "Severe loss of material or tactical oversight."
            elif diff < -150:
                classification = "🟡 Mistake"
                explanation = "Weakened position or missed a defensive resource."
            elif diff < -50:
                classification = "🔵 Inaccuracy"
                explanation = "Slightly sub-optimal compared to engine recommendation."
            elif diff > 100:
                classification = "🟢 Excellent"
                explanation = "Strong tactical or positional improvement!"
                
            analysis_results.append({
                "move_number": move_num,
                "player_move": board.san(move),
                "best_move": board.san(best_move) if best_move else "-",
                "eval_before": eval_before / 100.0,
                "eval_after": eval_after / 100.0,
                "classification": classification,
                "explanation": explanation
            })
            
            eval_before = eval_after
            move_num += 1
            
        return analysis_results