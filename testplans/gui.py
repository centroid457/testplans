# from . import *
from .tc import TestCaseBase
# from .tp import TpMultyDutBase
from .tm import TpTableModel

import time

from pyqt_templates import *


# =====================================================================================================================
class TpGuiBase(Gui):
    # OVERWRITTEN -----------------------------------
    START = False

    TITLE = "[TestPlan] Universal"
    SIZE = (600, 300)

    # NEW -------------------------------------------
    DATA: "TpMultyDutBase"

    def __init__(self, data):
        self.TITLE = f"[TestPlan]{data.STAND_ID}/{data.STAND_DESCRIPTION[:20]}"
        super().__init__(data)

    # WINDOW ==========================================================================================================
    def wgt_create(self):
        self.TV_create()
        self.PTE_create()
        self.BTN_create()

        # DETAILS -----------------------------------------------------------------------------------------------------

        # layout_details ----------------------------------------------------------------------------------------------
        layout_details = QVBoxLayout()
        layout_details.addWidget(self.BTN)
        layout_details.addWidget(self.BTN_settings)
        layout_details.addWidget(self.PTE)

        # layout_main -------------------------------------------------------------------------------------------------
        layout_main = QHBoxLayout()
        layout_main.addWidget(self.TV)
        layout_main.addLayout(layout_details)
        self.setLayout(layout_main)

    # WGTS ============================================================================================================
    def BTN_create(self) -> None:
        self.BTN = QPushButton("START")
        self.BTN.setCheckable(True)

        self.BTN_settings = QPushButton("settings")
        self.BTN_settings.setCheckable(True)

    def PTE_create(self) -> None:
        self.PTE = QPlainTextEdit()

        # METHODS ORIGINAL ---------------------------------
        # self.PTE.setEnabled(True)
        # self.PTE.setUndoRedoEnabled(True)
        # self.PTE.setReadOnly(True)
        # self.PTE.setMaximumBlockCount(15)

        # self.PTE.clear()
        self.PTE.setPlainText("setPlainText")
        self.PTE.appendPlainText("appendPlainText")
        # self.PTE.appendHtml("")
        # self.PTE.anchorAt(#)
        # self.PTE.setSizeAdjustPolicy(#)

        # METHODS COMMON -----------------------------------
        self.PTE.setFont(QFont("Calibri (Body)", 7))

    def TV_create(self):
        # TODO: move examples to pyqtTemplate!
        self.TM = TpTableModel(self.DATA)

        self.TV = QTableView()
        self.TV.setModel(self.TM)
        self.TV.setSelectionMode(QTableView.SingleSelection)

        # self.TV.setStyleSheet("gridline-color: rgb(255, 0, 0)")
        # self.TV.setMinimumSize(400, 300)
        # self.TV.setShowGrid(True)
        # self.TV.setFont(QFont("Calibri (Body)", 7))
        # self.TV.setSortingEnabled(True)     # enable sorting
        self.TV.resizeColumnsToContents()   # set column width to fit contents
        # self.TV.setColumnWidth(0, 100)

        #
        hh = self.TV.horizontalHeader()
        hh.setSectionHidden(2, True)
        hh.setSectionsClickable(False)
        # hh.setStretchLastSection(True)

        # self.TV.selectRow(1)      # not working
        # self.TV.selectColumn(2)   # not working

        # self.TV.setSelectionModel(QItemSelection().select())

    # SLOTS ===========================================================================================================
    def slots_connect(self):
        self.BTN.toggled.connect(self.BTN__toggled)
        self.BTN_settings.toggled.connect(self.BTN_settings__toggled)
        self.DATA.signal__tp_finished.connect(lambda: self.BTN.setChecked(False))
        self.DATA.signal__tp_finished.connect(self.TM._data_reread)

        TestCaseBase.signals.signal__tc_state_changed.connect(lambda _: self.TM._data_reread())

        self.TV.selectionModel().selectionChanged.connect(self.TV_selectionChanged)
        self.TV.horizontalHeader().sectionClicked.connect(self.TV_hh_sectionClicked)

    def BTN__toggled(self, state: Optional[bool] = None) -> None:
        # print(f"btn {state=}")
        if self.DATA.isRunning():
            state = False

        if state:
            self.DATA.start()
            self.TM._data_reread()
        elif state is False:
            # if not self.DATA.isFinished():
            self.DATA.terminate()
            self.TM._data_reread()

    def BTN_settings__toggled(self, state: Optional[bool] = None) -> None:
        # print(f"BTN_select_tc_on_duts__toggled {state=}")
        self.TV.horizontalHeader().setSectionHidden(2, not state)
        self.TV.horizontalHeader().setSectionsClickable(state)
        self.TM.open__settings = state
        self.TM._data_reread()

    def TV_hh_sectionClicked(self, index: int) -> None:
        if index > 1:
            dut = self.DATA.DEVICES.LIST__DUT[index - self.TM.ADDITIONAL_COLUMNS]
            dut._bebug__SKIP_reverse()
            self.TM._data_reread()

    def TV_selectionChanged(self, first: QItemSelection, last: QItemSelection) -> None:
        # print("selectionChanged")
        # print(f"{first=}")  # first=<PyQt5.QtCore.QItemSelection object at 0x000001C79A107460>
        # ObjectInfo(first.indexes()[0]).print(_log_iter=True, skip_fullnames=["takeFirst", "takeLast"])

        if not first:
            # when item with noFlag IsSelectable
            return

        index: QModelIndex = first.indexes()[0]

        row = index.row()
        col = index.column()

        if not col > 1:
            return

        tc = list(self.DATA.TCS)[row]
        dut = self.DATA.DEVICES.LIST__DUT[col - self.TM.ADDITIONAL_COLUMNS]
        self.PTE.setPlainText(tc.TCS_ON_DUTS[dut.INDEX].info_pretty())

        # print(f"{row=}/{section=}/{dut=}/{tc=}")


# =====================================================================================================================
