import pytest

from . import *
from . import TpManager, TestCase

from pyqt_templates import *
from object_info import ObjectInfo


# =====================================================================================================================
class TpTableModel(QAbstractTableModel):
    DATA: TpManager

    def __init__(self, data: TpManager):
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
                if dut.TP_RESULTS[tc].result is True:
                    return QColor("#00FF00")
                if dut.TP_RESULTS[tc].result is False:
                    return QColor("#FF5050")

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
class TpGui(Gui):
    # OVERWRITTEN -----------------------------------
    TITLE = "[TestPlan] Universal"
    SIZE = (600, 300)

    # NEW -------------------------------------------
    DATA: TpManager

    QTV: QTableView = None
    QPTE: QPlainTextEdit = None

    def __init__(self, data: TpManager):
        self.DATA = data
        super().__init__()

    def wgt_create(self):
        self.qtv_create()

        # DETAILS -----------------------------------------------------------------------------------------------------
        self.btn_start = QPushButton("START")
        self.btn_start.setCheckable(True)

        self.QPTE = QPlainTextEdit()

        # layout_details ----------------------------------------------------------------------------------------------
        layout_details = QVBoxLayout()
        layout_details.addWidget(self.btn_start)
        layout_details.addWidget(self.QPTE)

        # layout_main -------------------------------------------------------------------------------------------------
        layout_main = QHBoxLayout()
        layout_main.addWidget(self.QTV)
        layout_main.addLayout(layout_details)
        self.setLayout(layout_main)

    def qtv_create(self):
        self.QTV = QTableView(self)
        self.QTV.setModel(TpTableModel(self.DATA))
        self.QTV.setSelectionMode(QTableView.SingleSelection)

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
        # super().slots_connect()

        self.btn_start.clicked.connect(self._wgt_main__center)
        self.btn_start.clicked.connect(self.DATA.run)
        TestCase.signals.signal__tc_result_updated.connect(lambda z=None: print("signal__tc_result_updated.emit") or self.QTV.model().endResetModel())

        # fixme: change object for redraw
        # TestCase.signals.signal__tc_details_updated.connect(lambda z=None: print("signal__tc_details_updated.emit") or self.QPTE)

        self.QTV.selectionModel().selectionChanged.connect(self.selection_apply)

    def selection_apply(self, first: QItemSelection, last: QItemSelection) -> None:
        # print("selectionChanged")
        # print(f"{first=}")  # first=<PyQt5.QtCore.QItemSelection object at 0x000001C79A107460>
        # ObjectInfo(first.indexes()[0]).print(_log_iter=True, skip_fullnames=["takeFirst", "takeLast"])

        index: QModelIndex = first.indexes()[0]

        row = index.row()
        col = index.column()

        if not col > 0:
            return

        tc = list(self.DATA.TCS)[row]
        if col > 0:
            dut = self.DATA.DUTS[col-1]
        else:
            dut = None
        self.QPTE.setPlainText(str(dut.TP_RESULTS[tc].details))

        # print(f"{row=}/{col=}/{dut=}/{tc=}")


# =====================================================================================================================
