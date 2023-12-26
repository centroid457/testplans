import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from pyqt_templates import *

from .base import *


# =====================================================================================================================
class MyTableModel(QAbstractTableModel):
    DATA: ManagerTp

    def __init__(self, data: ManagerTp):
        super().__init__()
        self.DATA = data

    def rowCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.TCS)

    def columnCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.DUTS) + 1

    def headerData(self, col: Any, orientation: Qt.Orientation, role: int = None) -> str:
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if col == 0:
                    return "Тесткейс"
                if col > 0:
                    return f"{col}"
            elif orientation == Qt.Vertical:
                return col + 1
        return QVariant()

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        flags = super().flags(index)

        if index.column() == 0:
            flags |= Qt.ItemIsUserCheckable
            flags |= Qt.ItemIsSelectable
        else:
            # flags -= Qt.ItemIsSelectable
            pass
        return flags

    def data(self, index: QModelIndex, role: int = None) -> Any:
        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        tc = list(self.DATA.TCS)[row]
        if col > 0:
            dut = self.DATA.DUTS[col-1]
        else:
            dut = None

        if role == Qt.DisplayRole:
            if col == 0:
                return f'{tc.name}\n{tc.DESCRIPTION}'
            if col > 0:
                return f'{dut.TP_RESULTS[tc].result}'

        elif role == Qt.ForegroundRole:
            if tc.SKIP:
                return QColor('#a2a2a2')

        elif role == Qt.BackgroundRole:
            if tc.SKIP:
                return QColor('#f2f2f2')

            if col > 0:
                if tc.result is True:
                    return QColor("green")
                if tc.result is False:
                    return QColor("red")

        if role == Qt.CheckStateRole:
            if col == 0:
                if tc.SKIP:
                    return Qt.Unchecked
                else:
                    return Qt.Checked

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        if not index.isValid():
            return False

        row = index.row()
        col = index.column()

        tc = list(self.DATA.TCS)[row]
        if col > 0:
            dut = self.DATA.DUTS[col-1]
        else:
            dut = None

        if role == Qt.CheckStateRole and col == 0:
            tc.SKIP = value == Qt.Unchecked
            self.data_reread()
        return True

    def data_reread(self) -> None:
        """
        just redraw model by reread all data!
        """
        self.endResetModel()


# =====================================================================================================================
class GuiTP(Gui):
    # OVERWRITTEN -----------------------------------
    TITLE = "[TestPlan] Universal"
    SIZE = (600, 300)

    # NEW -------------------------------------------
    DATA: ManagerTp
    QTV: QTableView = None

    def __init__(self, data: ManagerTp):
        self.DATA = data
        super().__init__()

    def wgt_create(self):
        self.qtv_create()

    def qtv_create(self):
        tm = MyTableModel(self.DATA)

        self.QTV = QTableView(self)
        self.QTV.setModel(tm)

        # self.QTV.setStyleSheet("gridline-color: rgb(255, 0, 0)")
        # self.QTV.setMinimumSize(400, 300)
        # self.QTV.setShowGrid(True)
        # self.QTV.setFont(QFont("Calibri (Body)", 12))
        # self.QTV.setSortingEnabled(True)     # enable sorting
        self.QTV.resizeColumnsToContents()   # set column width to fit contents
        # self.QTV.setColumnWidth(0, 100)

        # hh = self.QTV.horizontalHeader()
        # hh.setStretchLastSection(True)

    def slots_connect(self):
        TestCase.signals.signal__tc_result_updated.connect(lambda z=None: self.QTV.model().endResetModel() or print("signal__tc_result_updated.emit"))

        # fixme: change object for redraw
        TestCase.signals.signal__tc_details_updated.connect(lambda z=None: self.QTV.model().endResetModel() or print("signal__tc_details_updated.emit"))


# =====================================================================================================================
