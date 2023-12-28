import pytest

from object_info import ObjectInfo
from pyqt_templates import *

from . import *
from . import TpManager, TestCase


# =====================================================================================================================
class TpTableModel(TableModelTemplate):
    DATA: TpManager

    def rowCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.TCS)

    def columnCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.DUTS) + 1

    def headerData(self, section: Any, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> str:
        if role == Qt.DisplayRole:
            # ------------------------------
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Тесткейс"
                if section > 0:
                    return f"{section}"
            # ------------------------------
            if orientation == Qt.Vertical:
                return section + 1

    def flags(self, index: QModelIndex) -> int:
        flags = super().flags(index)

        if index.column() == 0:
            flags |= Qt.ItemIsUserCheckable
            flags |= Qt.ItemIsSelectable
        else:
            # flags -= Qt.ItemIsSelectable
            pass
        return flags

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        tc = list(self.DATA.TCS)[row]
        if col > 0:
            dut = self.DATA.DUTS[col-1]
        else:
            dut = None

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DisplayRole:
            if col == 0:
                return f'{tc.name}\n{tc.DESCRIPTION}'
            if col > 0:
                return f'{dut.TP_RESULTS[tc].result}'

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.TextAlignmentRole:
            """
            VARIANTS ALIGN
            --------------
            not exists NAME!!!} = 0         # (LEFT+TOP) [[[[[[[[DEFAULT IS [LEFT+TOP]]]]]]]]]
            
            AlignLeft=AlignLeading = 1      # LEFT(+TOP)
            AlignRight=AlignTrailing = 2    # RIGHT(+TOP)

            AlignTop = 32       # TOP(+LEFT)
            AlignBottom = 64    # BOT(+LEFT)

            AlignHCenter = 4    # HCENTER(+TOP)
            AlignVCenter = 128  # VCENTER(+LEFT)
            AlignCenter = 132   # VCENTER+HCENTER

            # =====MAYBE DID NOT FIGURED OUT!!!
            AlignAbsolute = 16      # (LEFT+TOP) == asDEFAULT
            AlignBaseline = 256     # (LEFT+TOP) == asDEFAULT

            AlignJustify = 8        # (LEFT+TOP) == asDEFAULT

            AlignHorizontal_Mask = 31   # TOP+RIGHT
            AlignVertical_Mask = 480    # LEFT+VCENTER
            """
            if col == 0:
                return Qt.AlignVCenter
            if col > 0:
                return Qt.AlignCenter

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.TextColorRole:
            if tc.SKIP:
                return QColor('#a2a2a2')

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.BackgroundColorRole:
            if tc.SKIP:
                return QColor('#f2f2f2')

            if col > 0:
                if dut.TP_RESULTS[tc].result is True:
                    return QColor("#00FF00")
                if dut.TP_RESULTS[tc].result is False:
                    return QColor("#FF5050")

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:
            if col == 0:
                if tc.SKIP:
                    return Qt.Unchecked
                else:
                    return Qt.Checked

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        # PREPARE -----------------------------------------------------------------------------------------------------
        row = index.row()
        col = index.column()

        tc = list(self.DATA.TCS)[row]
        if col > 0:
            dut = self.DATA.DUTS[col-1]
        else:
            dut = None

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:
            if col == 0:
                tc.SKIP = value == Qt.Unchecked

        # FINAL -------------------------------------------------------------------------------------------------------
        self._data_reread()
        return True


# =====================================================================================================================
class TpGui(Gui):
    # OVERWRITTEN -----------------------------------
    TITLE = "[TestPlan] Universal"
    SIZE = (600, 300)

    # NEW -------------------------------------------
    DATA: TpManager

    def __init__(self, data: TpManager):
        self.DATA = data
        super().__init__()

    def wgt_create(self):
        self.QTV_create()
        self.QPTE_create()

        # DETAILS -----------------------------------------------------------------------------------------------------
        self.btn_start = QPushButton("START")
        self.btn_start.setCheckable(True)

        # layout_details ----------------------------------------------------------------------------------------------
        layout_details = QVBoxLayout()
        layout_details.addWidget(self.btn_start)
        layout_details.addWidget(self.QPTE)

        # layout_main -------------------------------------------------------------------------------------------------
        layout_main = QHBoxLayout()
        layout_main.addWidget(self.QTV)
        layout_main.addLayout(layout_details)
        self.setLayout(layout_main)

    def QPTE_create(self) -> None:
        self.QPTE = QPlainTextEdit()

        # METHODS ORIGINAL ---------------------------------
        # self.QPTE.setEnabled(True)
        # self.QPTE.setUndoRedoEnabled(True)
        # self.QPTE.setReadOnly(True)
        # self.QPTE.setMaximumBlockCount(15)

        # self.QPTE.clear()
        self.QPTE.setPlainText("setPlainText")
        self.QPTE.appendPlainText("appendPlainText")
        # self.QPTE.appendHtml("")
        # self.QPTE.anchorAt(#)
        # self.QPTE.setSizeAdjustPolicy(#)

        # METHODS COMMON -----------------------------------
        self.QPTE.setFont(QFont("Calibri (Body)", 7))

    def QTV_create(self):
        self.QTM = TpTableModel(self.DATA)

        self.QTV = QTableView()
        self.QTV.setModel(self.QTM)
        self.QTV.setSelectionMode(QTableView.SingleSelection)

        # self.QTV.setStyleSheet("gridline-color: rgb(255, 0, 0)")
        # self.QTV.setMinimumSize(400, 300)
        # self.QTV.setShowGrid(True)
        # self.QTV.setFont(QFont("Calibri (Body)", 7))
        # self.QTV.setSortingEnabled(True)     # enable sorting
        self.QTV.resizeColumnsToContents()   # set column width to fit contents
        # self.QTV.setColumnWidth(0, 100)

        # hh = self.QTV.horizontalHeader()
        # hh.setStretchLastSection(True)

        # self.QTV.selectRow(1)
        # self.QTV.selectColumn(2)
        # self.QTV.setSelectionModel(QItemSelection().select())

    def slots_connect(self):
        # super().slots_connect()

        self.btn_start.clicked.connect(self._wgt_main__center)
        self.btn_start.clicked.connect(self.DATA.run)
        TestCase.signals.signal__tc_result_updated.connect(lambda z=None: print("signal__tc_result_updated.emit") or self.QTM._data_reread())

        # fixme: change object for redraw
        # TestCase.signals.signal__tc_details_updated.connect(lambda z=None: print("signal__tc_details_updated.emit") or self.QPTE)

        self.QTV.selectionModel().selectionChanged.connect(self.QTV_selection_changed)

    def QTV_selection_changed(self, first: QItemSelection, last: QItemSelection) -> None:
        # print("selectionChanged")
        # print(f"{first=}")  # first=<PyQt5.QtCore.QItemSelection object at 0x000001C79A107460>
        # ObjectInfo(first.indexes()[0]).print(_log_iter=True, skip_fullnames=["takeFirst", "takeLast"])

        if not first:
            # when item with noFlag IsSelectable
            return

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
        self.QPTE.setPlainText(dut.TP_RESULTS[tc].details_pretty())

        # print(f"{row=}/{section=}/{dut=}/{tc=}")


# =====================================================================================================================
