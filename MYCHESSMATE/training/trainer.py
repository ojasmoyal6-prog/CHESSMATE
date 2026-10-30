import random

class TrainingManager:
    PUZZLES = [
        {
            "category": "Knight Fork",
            "fen": "r1bqkb1r/pppp1ppp/2n5/4p3/2B1n3/5N2/PPPP1PPP/RNBQ1RK1 w kq - 0 5",
            "prompt": "Find the best attacking move to fork the opponent.",
            "solution": "Nxe5"
        },
        {
            "category": "Back Rank Mate",
            "fen": "6k1/5ppp/8/8/8/8/4RPPP/6K1 w - - 0 1",
            "prompt": "Deliver checkmate in one move.",
            "solution": "Re8#"
        }
    ]

    @staticmethod
    def get_random_puzzle():
        return random.choice(TrainingManager.PUZZLES)