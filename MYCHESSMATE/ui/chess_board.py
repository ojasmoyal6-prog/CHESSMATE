import chess
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QMouseEvent

class ChessBoardWidget(QWidget):
    move_made = Signal(str)

    def __init__(self, board=None):
        super().__init__()
        self.board = board if board else chess.Board()
        self.selected_square = None
        self.last_move = None
        self.interactive_enabled = True
        self.init_ui()

    def init_ui(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.squares = {}
        
        # High-definition Unicode chess piece mapping guaranteeing 100% visibility
        self.piece_symbols = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }

        for row in range(8):
            for col in range(8):
                sq_idx = chess.square(col, 7 - row)
                lbl = QLabel()
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setFont(QFont("Arial", 36, QFont.Bold))
                
                self.squares[sq_idx] = lbl
                self.grid.addWidget(lbl, row, col)

        self.setLayout(self.grid)
        self.setFixedSize(560, 560)
        self.update_board_visuals()

    def update_board(self, board, last_move=None):
        self.board = board
        self.last_move = last_move
        self.selected_square = None
        self.update_board_visuals()

    def update_board_visuals(self):
        legal_targets = []
        if self.selected_square is not None:
            for move in self.board.legal_moves:
                if move.from_square == self.selected_square:
                    legal_targets.append(move.to_square)

        king_in_check_square = None
        if self.board.is_check():
            king_in_check_square = self.board.king(self.board.turn)

        for row in range(8):
            for col in range(8):
                sq_idx = chess.square(col, 7 - row)
                lbl = self.squares[sq_idx]
                
                # Modern clean chess palette
                is_light = (row + col) % 2 == 0
                bg_color = "#eeeed2" if is_light else "#769656"
                
                if sq_idx == self.selected_square:
                    bg_color = "#baca2b" if is_light else "#d0ed57"
                elif self.last_move and (sq_idx == self.last_move.from_square or sq_idx == self.last_move.to_square):
                    bg_color = "#cdd26a" if is_light else "#aaa23a"
                elif sq_idx == king_in_check_square:
                    bg_color = "#eb4d4b"

                piece = self.board.piece_at(sq_idx)
                piece_text = self.piece_symbols[piece.symbol()] if piece else ''
                
                # Subtle legal move indicators
                indicator = ""
                if sq_idx in legal_targets:
                    indicator = " ◉" if piece else " •"

                lbl.setText(piece_text + indicator)
                
                # Ensure crisp contrast for white and black pieces
                text_color = "#f8f9fa" if (piece and piece.color == chess.WHITE) else "#1e272e"
                if sq_idx in legal_targets and not piece:
                    text_color = "#2f3640"

                lbl.setStyleSheet(f"""
                    background-color: {bg_color}; 
                    color: {text_color};
                    border-radius: 2px;
                """)

    def mousePressEvent(self, event: QMouseEvent):
        if not self.interactive_enabled:
            return

        x = event.pos().x()
        y = event.pos().y()
        if x < 0 or x >= self.width() or y < 0 or y >= self.height():
            return
            
        col = x // (self.width() // 8)
        row = y // (self.height() // 8)
        sq_idx = chess.square(col, 7 - row)
        
        if self.selected_square is None:
            piece = self.board.piece_at(sq_idx)
            if piece and piece.color == self.board.turn:
                self.selected_square = sq_idx
                self.update_board_visuals()
        else:
            move = chess.Move(self.selected_square, sq_idx)
            # Handle automatic pawn promotion to Queen for seamless gameplay
            piece = self.board.piece_at(self.selected_square)
            if piece and piece.piece_type == chess.PAWN and chess.square_rank(sq_idx) in [0, 7]:
                move = chess.Move(self.selected_square, sq_idx, promotion=chess.QUEEN)

            if move in self.board.legal_moves:
                self.board.push(move)
                self.last_move = move
                self.selected_square = None
                self.update_board_visuals()
                self.move_made.emit(move.uci())
            else:
                # Re-select if clicking another friendly piece, otherwise deselect
                if piece and piece.color == self.board.turn:
                    self.selected_square = sq_idx
                else:
                    self.selected_square = None
                self.update_board_visuals()
                