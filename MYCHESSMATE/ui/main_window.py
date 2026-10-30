import chess
import random
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QStackedWidget, QComboBox, QTextEdit, QFrame
)
from PySide6.QtCore import Qt, QThread, Signal
from ui.chess_board import ChessBoardWidget
from engine.search import ChessAI

class AIWorker(QThread):
    finished = Signal(object)

    def __init__(self, board, difficulty):
        super().__init__()
        self.board = board
        self.difficulty = difficulty

    def run(self):
        ai = ChessAI(self.difficulty)
        best_move = ai.get_best_move(self.board)
        self.finished.emit(best_move)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChessMind - Play. Analyze. Improve.")
        self.setMinimumSize(1050, 720)
        
        self.board = chess.Board()
        self.difficulty = "Medium"
        self.personality = "Calm"
        
        self.central_stack = QStackedWidget()
        self.setCentralWidget(self.central_stack)
        
        self.init_main_menu()
        self.init_game_view()

    def init_main_menu(self):
        menu_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel("ChessMind")
        title.setStyleSheet("font-size: 44px; font-weight: bold; color: #2c3e50; font-family: 'Georgia';")
        title.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Play. Analyze. Improve.")
        subtitle.setStyleSheet("font-size: 15px; color: #7f8c8d; margin-bottom: 35px; letter-spacing: 3px;")
        subtitle.setAlignment(Qt.AlignCenter)
        
        settings_layout = QHBoxLayout()
        settings_layout.setAlignment(Qt.AlignCenter)
        
        self.diff_combo = QComboBox()
        self.diff_combo.addItems(["Easy", "Medium", "Hard"])
        self.diff_combo.setCurrentText("Medium")
        self.diff_combo.setStyleSheet("padding: 8px; font-size: 14px; border-radius: 4px;")
        self.diff_combo.currentTextChanged.connect(lambda t: setattr(self, 'difficulty', t))
        
        self.pers_combo = QComboBox()
        self.pers_combo.addItems(["Calm", "Competitive", "Coach"])
        self.pers_combo.setCurrentText("Calm")
        self.pers_combo.setStyleSheet("padding: 8px; font-size: 14px; border-radius: 4px;")
        self.pers_combo.currentTextChanged.connect(lambda t: setattr(self, 'personality', t))
        
        settings_layout.addWidget(QLabel("AI Difficulty:"))
        settings_layout.addWidget(self.diff_combo)
        settings_layout.addWidget(QLabel("AI Persona:"))
        settings_layout.addWidget(self.pers_combo)
        
        btn_play = QPushButton("PLAY CHESS")
        btn_play.setStyleSheet("font-size: 16px; font-weight: bold; padding: 14px 45px; background-color: #27ae60; color: white; border-radius: 6px; margin-top: 25px;")
        btn_play.clicked.connect(self.start_new_game)
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(settings_layout)
        layout.addWidget(btn_play, alignment=Qt.AlignCenter)
        
        menu_widget.setLayout(layout)
        self.central_stack.addWidget(menu_widget)

    def start_new_game(self):
        self.board = chess.Board()
        self.chess_board_ui.update_board(self.board)
        self.chess_board_ui.interactive_enabled = True
        self.history_box.clear()
        self.status_label.setText("Your Turn (White)")
        self.chat_label.setText("Let's have a clean game. Make your move!")
        self.central_stack.setCurrentIndex(1)

    def init_game_view(self):
        game_widget = QWidget()
        layout = QHBoxLayout()
        
        self.chess_board_ui = ChessBoardWidget(self.board)
        self.chess_board_ui.move_made.connect(self.on_player_move)
        
        sidebar = QVBoxLayout()
        
        self.status_label = QLabel("Your Turn (White)")
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        
        self.history_box = QTextEdit()
        self.history_box.setReadOnly(True)
        self.history_box.setPlaceholderText("Move history...")
        self.history_box.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dcdde1; border-radius: 6px; font-family: monospace; font-size: 13px;")
        
        chat_frame = QFrame()
        chat_frame.setStyleSheet("background-color: #f1f2f6; border-radius: 6px; padding: 12px;")
        chat_layout = QVBoxLayout(chat_frame)
        
        chat_title = QLabel("💬 AI Opponent")
        chat_title.setStyleSheet("font-weight: bold; color: #333;")
        self.chat_label = QLabel("Ready when you are.")
        self.chat_label.setWordWrap(True)
        self.chat_label.setStyleSheet("font-style: italic; color: #555;")
        
        chat_layout.addWidget(chat_title)
        chat_layout.addWidget(self.chat_label)
        
        btn_back = QPushButton("Main Menu")
        btn_back.setStyleSheet("padding: 10px; background-color: #7f8c8d; color: white; border-radius: 4px;")
        btn_back.clicked.connect(lambda: self.central_stack.setCurrentIndex(0))
        
        sidebar.addWidget(self.status_label)
        sidebar.addWidget(self.history_box, stretch=2)
        sidebar.addWidget(chat_frame)
        sidebar.addWidget(btn_back)
        
        layout.addWidget(self.chess_board_ui)
        layout.addLayout(sidebar)
        
        game_widget.setLayout(layout)
        self.central_stack.addWidget(game_widget)

    def on_player_move(self, move_uci):
        move = chess.Move.from_uci(move_uci)
        san_move = self.board.san(move) # Note: board was already pushed in widget
        # Re-format history accurately
        self.update_move_history_display()
        
        if self.board.is_game_over():
            self.handle_game_over()
            return
            
        self.chess_board_ui.interactive_enabled = False
        self.status_label.setText("AI is thinking...")
        self.trigger_ai_move()

    def trigger_ai_move(self):
        self.ai_worker = AIWorker(self.board, self.difficulty)
        self.ai_worker.finished.connect(self.on_ai_move_finished)
        self.ai_worker.start()

    def on_ai_move_finished(self, ai_move):
        if ai_move and ai_move in self.board.legal_moves:
            self.board.push(ai_move)
            self.chess_board_ui.update_board(self.board, last_move=ai_move)
            self.update_move_history_display()
            self.trigger_ai_commentary()

        if self.board.is_game_over():
            self.handle_game_over()
        else:
            self.chess_board_ui.interactive_enabled = True
            self.status_label.setText("Your Turn (White)")

    def update_move_history_display(self):
        # Rebuild clean move text representation from move stack
        temp_board = chess.Board()
        history_str = ""
        moves = list(self.board.move_stack)
        for i in range(0, len(moves), 2):
            move_num = (i // 2) + 1
            w_move = temp_board.san(moves[i])
            temp_board.push(moves[i])
            
            b_move = ""
            if i + 1 < len(moves):
                b_move = temp_board.san(moves[i+1])
                temp_board.push(moves[i+1])
                
            history_str += f"{move_num}. {w_move}  {b_move}\n"
        
        self.history_box.setText(history_str)

    def trigger_ai_commentary(self):
        comments = {
            "Calm": [
                "Interesting position.",
                "Let's see how this develops.",
                "Solid choice.",
                "Maintaining balance."
            ],
            "Competitive": [
                "Is that your best move?",
                "You're making this interesting.",
                "Let's turn up the pressure.",
                "I see what you're trying to do."
            ],
            "Coach": [
                "Good piece activation.",
                "Keep an eye on your king safety.",
                "Nice central control.",
                "Solid development."
            ]
        }
        chosen_comment = random.choice(comments.get(self.personality, comments["Calm"]))
        self.chat_label.setText(f'"{chosen_comment}"')

    def handle_game_over(self):
        self.chess_board_ui.interactive_enabled = False
        outcome = self.board.outcome()
        result_msg = "Game Over"
        if outcome:
            if outcome.winner == chess.WHITE:
                result_msg = "Checkmate! You Win! 🎉"
            elif outcome.winner == chess.BLACK:
                result_msg = "Checkmate! AI Wins."
            else:
                result_msg = f"Draw ({outcome.termination.name.title()})"
        self.status_label.setText(result_msg)
        self.chat_label.setText('"Good game! Well played."')