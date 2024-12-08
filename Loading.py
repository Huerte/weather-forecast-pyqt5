from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget


class LoadingOverlay(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(parent.size())

        # Transparent backgrounds with centered layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Loading animation
        self.loading_label = QLabel()
        self.loading_label.setAttribute(Qt.WA_TranslucentBackground)  # Make the label backgrounds transparent
        # Load the GIF animation
        movie = QMovie("assets/animation/loading.gif")
        movie.setScaledSize(QSize(75, 75))
        self.loading_label.setMovie(movie)
        movie.start()
        # Keep reference to the movie to prevent garbage collection
        self.movie = movie
        # Optionally, set the parent widget to be transparent too (if needed)
        self.loading_label.setStyleSheet("backgrounds: transparent;")

        # Add label to layout
        loading_wrapper = QWidget()
        loading_wrapper.setAttribute(Qt.WA_TranslucentBackground)
        loading_layout = QVBoxLayout(loading_wrapper)
        loading_layout.setAlignment(Qt.AlignCenter)
        loading_layout.addWidget(self.loading_label)

        main_layout.addWidget(loading_wrapper)

    def resizeEvent(self, event):
        """Ensure the overlay stays centered when resized."""
        self.setFixedSize(self.parent().size())
        super().resizeEvent(event)