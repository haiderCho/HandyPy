import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QStackedWidget, QMessageBox, QInputDialog,
                             QFrame, QScrollArea, QSizePolicy, QGraphicsDropShadowEffect)
from PyQt6.QtCore import QTimer, Qt, QSize, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QFont, QColor, QPalette, QBrush, QLinearGradient

# --- Constants & Theme ---
THEME = {
    "bg": "#121212",
    "surface": "#1E1E1E",
    "primary": "#BB86FC",
    "secondary": "#03DAC6",
    "text": "#FFFFFF",
    "text_dim": "#B0B0B0",
    "user_bubble": "#3700B3",
    "bot_bubble": "#2C2C2C",
    "input_bg": "#2C2C2C",
    "red": "#CF6679"
}

FONT_FAMILY = "Segoe UI" # Standard Windows font, looks clean

class ModernButton(QPushButton):
    def __init__(self, text, color=THEME["primary"], text_color="#000000", parent=None):
        super().__init__(text, parent)
        self.setFont(QFont(FONT_FAMILY, 10, QFont.Weight.Bold))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: {text_color};
                border-radius: 8px;
                padding: 10px 20px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {color}AA; 
            }}
            QPushButton:pressed {{
                background-color: {color}55;
            }}
        """)
        
        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

class ChatBubble(QFrame):
    def __init__(self, text, is_user=False, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("background: transparent;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        
        # Bubble Content
        self.bubble = QLabel(text)
        self.bubble.setFont(QFont(FONT_FAMILY, 11))
        self.bubble.setWordWrap(True)
        self.bubble.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        bg_color = THEME["user_bubble"] if is_user else THEME["bot_bubble"]
        text_color = THEME["text"]
        border_radius = "15px"
        
        # Different corners for user vs bot
        radius_style = "15px 15px 0px 15px" if is_user else "15px 15px 15px 0px"
        
        self.bubble.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border-radius: {border_radius};
                border-bottom-right-radius: {0 if is_user else 15}px;
                border-bottom-left-radius: {15 if is_user else 0}px;
                padding: 12px 16px;
            }}
        """)
        
        # Shadow for bubble
        shadow = QGraphicsDropShadowEffect(self.bubble)
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 2)
        self.bubble.setGraphicsEffect(shadow)

        if is_user:
            layout.addStretch()
            layout.addWidget(self.bubble)
        else:
            layout.addWidget(self.bubble)
            layout.addStretch()

class ChatBotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HandyPy ChatBot")
        self.setGeometry(100, 100, 450, 700) # Mobile-like aspect ratio
        
        # Set Window Background
        self.setStyleSheet(f"background-color: {THEME['bg']};")

        # Data
        self.user_name = "User"
        self.bot_name = "Bot"
        self.topic_file = "chatbot_data.txt"
        self.qa_data = []

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Stacked Widget for Navigation
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        # Initialize Pages
        self.init_welcome_page()
        self.init_info_page()
        self.init_topic_page()
        self.init_chat_page()

        # Add pages to stack
        self.stack.addWidget(self.page_welcome)
        self.stack.addWidget(self.page_info)
        self.stack.addWidget(self.page_topic)
        self.stack.addWidget(self.page_chat)

        self.stack.setCurrentWidget(self.page_welcome)

    def init_welcome_page(self):
        self.page_welcome = QWidget()
        layout = QVBoxLayout(self.page_welcome)
        layout.setContentsMargins(40, 60, 40, 40)
        layout.setSpacing(20)

        # Header Area (Time/Date)
        header_layout = QHBoxLayout()
        self.lbl_datetime = QLabel()
        self.lbl_datetime.setFont(QFont(FONT_FAMILY, 10))
        self.lbl_datetime.setStyleSheet(f"color: {THEME['text_dim']};")
        header_layout.addWidget(self.lbl_datetime)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        layout.addStretch()

        # Hero Section
        lbl_welcome = QLabel("Hello.")
        lbl_welcome.setFont(QFont(FONT_FAMILY, 48, QFont.Weight.Bold))
        lbl_welcome.setStyleSheet(f"color: {THEME['text']};")
        layout.addWidget(lbl_welcome)

        lbl_sub = QLabel("I'm your personal AI assistant.\nReady to help you.")
        lbl_sub.setFont(QFont(FONT_FAMILY, 16))
        lbl_sub.setStyleSheet(f"color: {THEME['text_dim']};")
        lbl_sub.setWordWrap(True)
        layout.addWidget(lbl_sub)

        layout.addStretch()

        # Action
        btn_start = ModernButton("Get Started", color=THEME["secondary"], text_color="#000000")
        btn_start.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_info))
        layout.addWidget(btn_start)

        # Footer
        lbl_footer = QLabel("Designed by haiderCho")
        lbl_footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_footer.setStyleSheet(f"color: {THEME['text_dim']}; font-size: 10px;")
        layout.addWidget(lbl_footer)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        self.update_datetime()

    def update_datetime(self):
        self.lbl_datetime.setText(time.strftime("%A, %d %B %H:%M"))

    def init_info_page(self):
        self.page_info = QWidget()
        layout = QVBoxLayout(self.page_info)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Back Button
        btn_back = QPushButton("← Back")
        btn_back.setStyleSheet(f"color: {THEME['text_dim']}; border: none; text-align: left; font-size: 14px;")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_welcome))
        layout.addWidget(btn_back)

        layout.addSpacing(20)

        lbl_title = QLabel("Let's get to know\neach other.")
        lbl_title.setFont(QFont(FONT_FAMILY, 24, QFont.Weight.Bold))
        lbl_title.setStyleSheet(f"color: {THEME['text']};")
        layout.addWidget(lbl_title)

        layout.addSpacing(20)

        # Inputs
        self.input_user_name = QLineEdit()
        self.input_user_name.setPlaceholderText("Your Name")
        self.style_input(self.input_user_name)
        layout.addWidget(self.input_user_name)

        self.input_bot_name = QLineEdit()
        self.input_bot_name.setPlaceholderText("Assistant Name")
        self.style_input(self.input_bot_name)
        layout.addWidget(self.input_bot_name)

        layout.addStretch()

        btn_continue = ModernButton("Continue")
        btn_continue.clicked.connect(self.submit_info)
        layout.addWidget(btn_continue)

    def style_input(self, widget):
        widget.setFixedHeight(50)
        widget.setFont(QFont(FONT_FAMILY, 12))
        widget.setStyleSheet(f"""
            QLineEdit {{
                background-color: {THEME['surface']};
                color: {THEME['text']};
                border: 1px solid {THEME['surface']};
                border-radius: 8px;
                padding: 0 15px;
            }}
            QLineEdit:focus {{
                border: 1px solid {THEME['primary']};
            }}
        """)

    def submit_info(self):
        u = self.input_user_name.text().strip()
        b = self.input_bot_name.text().strip()
        if u: self.user_name = u
        if b: self.bot_name = b
        self.stack.setCurrentWidget(self.page_topic)

    def init_topic_page(self):
        self.page_topic = QWidget()
        layout = QVBoxLayout(self.page_topic)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        btn_back = QPushButton("← Back")
        btn_back.setStyleSheet(f"color: {THEME['text_dim']}; border: none; text-align: left; font-size: 14px;")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_info))
        layout.addWidget(btn_back)

        layout.addSpacing(20)

        lbl_title = QLabel("Choose a Topic")
        lbl_title.setFont(QFont(FONT_FAMILY, 24, QFont.Weight.Bold))
        lbl_title.setStyleSheet(f"color: {THEME['text']};")
        layout.addWidget(lbl_title)

        layout.addSpacing(20)

        # Topic Card
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {THEME['surface']};
                border-radius: 12px;
            }}
        """)
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_topic = QLabel("General Chat")
        lbl_topic.setFont(QFont(FONT_FAMILY, 14, QFont.Weight.Bold))
        lbl_topic.setStyleSheet(f"color: {THEME['text']};")
        
        btn_go = QPushButton("Start >")
        btn_go.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_go.setStyleSheet(f"color: {THEME['secondary']}; font-weight: bold; border: none; font-size: 14px;")
        btn_go.clicked.connect(self.load_chat)

        card_layout.addWidget(lbl_topic)
        card_layout.addStretch()
        card_layout.addWidget(btn_go)

        layout.addWidget(card)
        layout.addStretch()

    def init_chat_page(self):
        self.page_chat = QWidget()
        layout = QVBoxLayout(self.page_chat)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setStyleSheet(f"background-color: {THEME['surface']}; border-bottom: 1px solid #333;")
        header.setFixedHeight(60)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(15, 0, 15, 0)

        btn_back = QPushButton("←")
        btn_back.setStyleSheet(f"color: {THEME['text']}; border: none; font-size: 20px; font-weight: bold;")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_topic))
        
        self.lbl_chat_title = QLabel("Chat")
        self.lbl_chat_title.setFont(QFont(FONT_FAMILY, 12, QFont.Weight.Bold))
        self.lbl_chat_title.setStyleSheet(f"color: {THEME['text']};")
        self.lbl_chat_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_menu = QPushButton("⋮")
        btn_menu.setStyleSheet(f"color: {THEME['text']}; border: none; font-size: 20px; font-weight: bold;")
        btn_menu.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_menu.clicked.connect(self.show_menu)

        header_layout.addWidget(btn_back)
        header_layout.addWidget(self.lbl_chat_title, 1)
        header_layout.addWidget(btn_menu)

        layout.addWidget(header)

        # Chat Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(f"background-color: {THEME['bg']}; border: none;")
        self.scroll_area.verticalScrollBar().setStyleSheet(f"""
            QScrollBar:vertical {{
                background: {THEME['bg']};
                width: 8px;
            }}
            QScrollBar::handle:vertical {{
                background: {THEME['surface']};
                border-radius: 4px;
            }}
        """)
        
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(15, 15, 15, 15)
        self.chat_layout.setSpacing(15)
        self.chat_layout.addStretch()

        self.scroll_area.setWidget(self.chat_container)
        layout.addWidget(self.scroll_area)

        # Input Area
        input_frame = QFrame()
        input_frame.setStyleSheet(f"background-color: {THEME['surface']};")
        input_layout = QHBoxLayout(input_frame)
        input_layout.setContentsMargins(10, 10, 10, 10)

        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type a message...")
        self.chat_input.setFont(QFont(FONT_FAMILY, 11))
        self.chat_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {THEME['input_bg']};
                color: {THEME['text']};
                border: none;
                border-radius: 20px;
                padding: 10px 15px;
            }}
        """)
        self.chat_input.returnPressed.connect(self.send_message)

        btn_send = QPushButton("➤")
        btn_send.setFixedSize(40, 40)
        btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_send.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME['primary']};
                color: white;
                border-radius: 20px;
                font-size: 16px;
            }}
            QPushButton:hover {{ background-color: {THEME['primary']}DD; }}
        """)
        btn_send.clicked.connect(self.send_message)

        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(btn_send)

        layout.addWidget(input_frame)

    def load_chat(self):
        try:
            with open(self.topic_file, 'r') as f:
                self.qa_data = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Data file not found.")
            return
        
        self.lbl_chat_title.setText(self.bot_name)
        self.stack.setCurrentWidget(self.page_chat)
        
        # Add initial greeting if empty
        if self.chat_layout.count() == 1: # Only stretch
            self.add_bubble(f"Hello {self.user_name}! I am {self.bot_name}.", False)

    def send_message(self):
        text = self.chat_input.text().strip()
        if not text: return
        
        self.chat_input.clear()
        self.add_bubble(text, True)
        
        # Process response
        QTimer.singleShot(600, lambda: self.process_response(text))

    def process_response(self, text):
        response = self.get_response(text)
        self.add_bubble(response, False)
        
        if response == 'Bye':
            QTimer.singleShot(1500, self.close)

    def add_bubble(self, text, is_user):
        bubble = ChatBubble(text, is_user)
        self.chat_layout.insertWidget(self.chat_layout.count()-1, bubble)
        
        # Scroll to bottom
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    def get_response(self, text):
        chat = text.lower().replace(' ', '')
        
        # Hardcoded responses
        if chat in ['whodevelopedyou?', 'whoinventedyou?', 'developer']:
            return "I was designed by haiderCho."
        if chat in ["what'smyname?", "myname?"]:
            return f"Your name is {self.user_name}."
        if chat in ["what'syourname?", "yourname?"]:
            return f"I am {self.bot_name}."
        if chat in ['bye', 'goodbye', 'exit']:
            return "Bye"
            
        # File matching
        for i in range(len(self.qa_data)):
            line = self.qa_data[i].lower().replace(' ', '')
            if line == chat:
                if i + 1 < len(self.qa_data):
                    return self.qa_data[i+1]
        
        return "I'm not sure how to answer that. You can teach me!"

    def show_menu(self):
        # Simple menu to add new answers
        text, ok = QInputDialog.getText(self, "Teach Bot", "Enter a new answer to add to the database:")
        if ok and text:
            try:
                with open(self.topic_file, 'a') as f:
                    f.write(text + "\n")
                self.load_chat() # Reload data
                QMessageBox.information(self, "Success", "I've learned something new!")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") # Better cross-platform look
    
    window = ChatBotWindow()
    window.show()
    sys.exit(app.exec())
