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
    def __init__(self):
        super().__init__()

        # data
        self.tabledata = [('apple', 'red', 'small'),
                          ('apple', 'red', 'medium'),
                          ('apple', 'green', 'small'),
                          ('banana', 'yellow', 'large')]
        self.createTable()

    def createTable(self):
        tm = MyTableModel(self.tabledata)

        self.tv = QTableView(self)
        self.tv.setStyleSheet("gridline-color: rgb(255, 0, 0)")
        self.tv.setModel(tm)
        self.tv.setMinimumSize(400, 300)
        self.tv.setShowGrid(True)
        self.tv.setFont(QFont("Calibri (Body)", 12))

        vh = self.tv.verticalHeader()
        vh.setVisible(True)

        hh = self.tv.horizontalHeader()
        hh.setStretchLastSection(True)

        self.tv.resizeColumnsToContents()   # set column width to fit contents

        nrows = len(self.tabledata)
        for row in range(nrows):
            self.tv.setRowHeight(row, 18)

        self.tv.setSortingEnabled(True)     # enable sorting


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
