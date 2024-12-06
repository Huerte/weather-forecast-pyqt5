from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPainter, QColor, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton


def change_icon_color(widget, icon_path, color):
    # Load the original icon
    original_pixmap = QPixmap(icon_path)
    if original_pixmap.isNull():
        raise FileNotFoundError(f"Icon not found: {icon_path}")

    # Create a pixmap to apply the new color
    colored_pixmap = QPixmap(original_pixmap.size())
    colored_pixmap.fill(Qt.transparent)  # Ensure transparency

    # Paint the new color using the original pixmap as a mask
    painter = QPainter(colored_pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_Source)
    painter.fillRect(colored_pixmap.rect(), QColor(color))
    painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    painter.drawPixmap(0, 0, original_pixmap)
    painter.end()

    if isinstance(widget, QLabel):
        widget.setPixmap(colored_pixmap)
    elif isinstance(widget, QPushButton):
        widget.setIcon(QIcon(colored_pixmap))
    else:
        print("Nor a Button and Label")
