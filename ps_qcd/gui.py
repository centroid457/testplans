import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .base import *


# =====================================================================================================================
class MyTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self.data)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self.data[0])

    def data(self, index: QModelIndex, role: int = None) -> Any:
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.data[index.row()][index.column()])

    def headerData(self, col: Any, orientation: Qt.Orientation, role: int = None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.data[0][col])
        return QVariant()


# =====================================================================================================================
class MyWindow(QWidget):
    DATA: Any
    QTV: QTableView = None

    def __init__(self):
        super().__init__()
        self.data = [('apple', 'red', 'small'),
                     ('apple', 'red', 'medium'),
                     ('apple', 'green', 'small'),
                     ('banana', 'yellow', 'large')]
        self.tv_create()

    def tv_create(self):
        tm = MyTableModel(self.data)

        self.QTV = QTableView(self)
        self.QTV.setStyleSheet("gridline-color: rgb(255, 0, 0)")
        self.QTV.setModel(tm)
        self.QTV.setMinimumSize(400, 300)
        self.QTV.setShowGrid(True)
        self.QTV.setFont(QFont("Calibri (Body)", 12))
        self.QTV.setSortingEnabled(True)     # enable sorting
        self.QTV.resizeColumnsToContents()   # set column width to fit contents

        vh = self.QTV.verticalHeader()
        vh.setVisible(True)

        hh = self.QTV.horizontalHeader()
        hh.setStretchLastSection(True)

        for row in range(len(self.data)):
            self.QTV.setRowHeight(row, 18)


# =====================================================================================================================
def start_gui():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())


# =====================================================================================================================
if __name__ == "__main__":
    start_gui()


# =====================================================================================================================
