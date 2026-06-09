#!/usr/bin/env python3
"""
Helical Gear Design Software
AGMA Standards - Imperial Units (Inch System)
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Helical Gear Design Software")
    app.setOrganizationName("AGMA Engineering Tools")

    font = QFont("Segoe UI", 9)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
