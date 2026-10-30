import chess

# Piece-Square Tables for position evaluation (Centipawns)
PAWN_TABLE = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

ROOK_TABLE = [
      0,  0,  0,  0,  0,  0,  0,  0,
      5, 10, 10, 10, 10, 10, 10,  5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
      0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_MID_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10, -10,-10,-20,-20,-10,-10,-10,
     20,  20,  0,  0,  0,  0,  20, 20,
     20,  30, 10,  0,  0, 10,  30, 20
]

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def evaluate_board(board: chess.Board) -> int:
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -99999
        else:
            return 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    total_evaluation = 0
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = PIECE_VALUES[piece.piece_type]
            sq_idx = square if piece.color == chess.WHITE else chess.square_mirror(square)
            
            if piece.piece_type == chess.PAWN:
                value += PAWN_TABLE[sq_idx]
            elif piece.piece_type == chess.KNIGHT:
                value += KNIGHT_TABLE[sq_idx]
            elif piece.piece_type == chess.BISHOP:
                value += BISHOP_TABLE[sq_idx]
            elif piece.piece_type == chess.ROOK:
                value += ROOK_TABLE[sq_idx]
            elif piece.piece_type == chess.QUEEN:
                value += QUEEN_TABLE[sq_idx]
            elif piece.piece_type == chess.KING:
                value += KING_MID_TABLE[sq_idx]
                
            if piece.color == chess.WHITE:
                total_evaluation += value
            else:
                total_evaluation -= value

    # Mobility bonus
    mobility = len(list(board.legal_moves))
    if board.turn == chess.WHITE:
        total_evaluation += mobility * 2
    else:
        total_evaluation -= mobility * 2

    return total_evaluation