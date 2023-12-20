import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .base import *


# =====================================================================================================================
class MyTableModel(QAbstractTableModel):
    DATA: ManagerTp

    def __init__(self, data: ManagerTp):
        super().__init__()
        self.DATA = data

    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self.DATA.TCS)

    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self.DATA.DUTS) + 2

    def headerData(self, col: Any, orientation: Qt.Orientation, role: int = None) -> str:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if col == 0:
                    return "USE"
                elif col == 1:
                    return "NAME"
                elif col > 1:
                    return f"dut{col - 1}"
            elif orientation == Qt.Vertical:
                return col + 1
        return QVariant()

    def data(self, index: QModelIndex, role: int = None) -> Any:
        col = index.column()
        row = index.row()

        tc = list(self.DATA.TCS)[row]
        dut = self.DATA.DUTS[col - 2]

        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            if col == 0:
                return QVariant()
            elif col == 1:
                return f'{tc.name}\n{tc.DESCRIPTION}'
            elif col > 1:
                return f'{dut.TP_RESULTS[tc].result}'


# =====================================================================================================================
class Gui(QWidget):
    _QAPP: QApplication = QApplication([])

    DATA: ManagerTp
    QTV: QTableView = None

    def __init__(self, data: ManagerTp):
        super().__init__()
        self.DATA = data

        self.wgt_create()
        self.slots_connect()

        self.show()
        sys.exit(self._QAPP.exec_())

    def wgt_create(self):
        self.setWindowTitle("[TestPlan] Universal")
        self.setMinimumWidth(600)
        self.qtv_create()

    def qtv_create(self):
        tm = MyTableModel(self.DATA)

        self.QTV = QTableView(self)
        self.QTV.setModel(tm)

        self.QTV.setStyleSheet("gridline-color: rgb(255, 0, 0)")
        self.QTV.setMinimumSize(400, 300)
        self.QTV.setShowGrid(True)
        self.QTV.setFont(QFont("Calibri (Body)", 12))
        self.QTV.setSortingEnabled(True)     # enable sorting
        self.QTV.resizeColumnsToContents()   # set column width to fit contents

        hh = self.QTV.horizontalHeader()
        hh.setStretchLastSection(True)

    def slots_connect(self):
        pass


# =====================================================================================================================
