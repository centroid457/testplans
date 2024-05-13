from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from pyqt_templates import TableModelTemplate
from funcs_aux import NamesIndexed_Base, NamesIndexed_Templated

# from .tp import TpMultyDutBase


# =====================================================================================================================
class TpTableModel(TableModelTemplate):
    DATA: "TpMultyDutBase"
    HEADERS: "Headers"

    # AUX -------------------------------------------
    open__settings: Optional[bool] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class Headers(NamesIndexed_Base):
            TESTCASE = 0
            ASYNC = 1
            STARTUP = 2
            DUTS = NamesIndexed_Templated(3, self.DATA.DEVICES__CLS.COUNT)
            TEARDOWN = 3 + self.DATA.DEVICES__CLS.COUNT
            # FIXME: need resolve COUNT over DevicesIndexed!!!

        self.HEADERS = Headers()

    def rowCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.TCS__CLS)

    def columnCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return self.HEADERS.count()

    # def headerData(self, section: Any, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> str:
    #     if role == Qt.DisplayRole:
    #         # ------------------------------
    #         if orientation == Qt.Horizontal:
    #             return self.HEADERS[section]
    #
    #         # ------------------------------
    #         if orientation == Qt.Vertical:
    #             return str(section + 1)

    def flags(self, index: QModelIndex) -> int:
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        # -------------------------------------------------------------------------------------------------------------
        flags = super().flags(index)

        if col in [self.HEADERS.TESTCASE, self.HEADERS.ASYNC] or col in self.HEADERS.DUTS:
            flags |= Qt.ItemIsUserCheckable
            # flags |= Qt.ItemIsSelectable
        else:
            # flags -= Qt.ItemIsSelectable
            pass

        # clear SELECTABLE ---------

        return flags

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()
        tc = list(self.DATA.TCS__CLS)[row]

        dut = None
        tc_inst = None
        if col in self.HEADERS.DUTS:
            dut = self.DATA.DEVICES__CLS.LIST__DUT[col - self.HEADERS.DUTS.START_OUTER]
            tc_inst = tc.TCS__INST[dut.INDEX]

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DisplayRole:
            if col == self.HEADERS.TESTCASE:
                return f'{tc.NAME}\n{tc.DESCRIPTION}'
            if col == self.HEADERS.ASYNC:
                return '+' if tc.ASYNC else '-'
            if col == self.HEADERS.STARTUP:
                if tc.result__cls_startup is True:
                    return '+'
                elif tc.result__cls_startup is False:
                    return '-'
                else:
                    return
            if col in self.HEADERS.DUTS:
                if tc_inst:
                    if tc_inst.result is None:
                        return ""
                    else:
                        return f'{tc_inst.result}'
            if col == self.HEADERS.TEARDOWN:
                if tc.result__cls_teardown is True:
                    return '+'
                elif tc.result__cls_teardown is False:
                    return '-'
                else:
                    return

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
            if col == self.HEADERS.TESTCASE:
                return Qt.AlignVCenter
            else:
                return Qt.AlignCenter

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.TextColorRole:
            if tc.SKIP:
                return QColor('#a2a2a2')

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.BackgroundColorRole:
            if tc.SKIP:
                return QColor('#e2e2e2')
            if col == self.HEADERS.STARTUP:
                if tc.result__cls_startup is True:
                    return QColor("#50FF50")
                if tc.result__cls_startup is False:
                    return QColor("#FF5050")
            if col in self.HEADERS.DUTS:
                if tc_inst.skip_tc_dut or not dut.connect() or dut.SKIP:
                    return QColor('#e2e2e2')
                if tc_inst.result is True:
                    return QColor("#00FF00")
                if tc_inst.result is False:
                    return QColor("#FF5050")
                if tc_inst.progress > 0:
                    return QColor("#FFFF50")
            if col == self.HEADERS.TEARDOWN:
                if tc.result__cls_teardown is True:
                    return QColor("#50FF50")
                if tc.result__cls_teardown is False:
                    return QColor("#FF5050")

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:
            if self.open__settings:
                if col == self.HEADERS.TESTCASE:
                    if tc.SKIP:
                        return Qt.Unchecked
                    else:
                        return Qt.Checked
                if col == self.HEADERS.ASYNC:
                    if tc.ASYNC:
                        return Qt.Checked
                    else:
                        return Qt.Unchecked
                if col in self.HEADERS.DUTS:
                    if not tc_inst.SKIP and not dut.SKIP:
                        if tc_inst.skip_tc_dut:
                            return Qt.Unchecked
                        else:
                            return Qt.Checked

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.FontRole:
            if tc == self.DATA.tc_active:
                # QFont("Arial", 9, QFont.Bold)
                font = QFont()

                font.setBold(True)
                # font.setItalic(True)

                # font.setOverline(True)  # надчеркнутый
                # font.setStrikeOut(True)  # зачеркнутый
                font.setUnderline(True)  # подчеркнутый

                # не понял!! --------------------
                # font.setStretch(5)
                # font.setCapitalization()

                return font

    def setData(self, index: QModelIndex, value: Any, role: int = None) -> bool:
        # PREPARE -----------------------------------------------------------------------------------------------------
        row = index.row()
        col = index.column()
        tc = list(self.DATA.TCS__CLS)[row]

        dut = None
        tc_inst = None
        if col in self.HEADERS.DUTS:
            dut = self.DATA.DEVICES__CLS.LIST__DUT[col - self.HEADERS.DUTS.START_OUTER]
            tc_inst = tc.TCS__INST[dut.INDEX]

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:
            if col == self.HEADERS.TESTCASE:
                tc.SKIP = value == Qt.Unchecked

            if col == self.HEADERS.ASYNC:
                tc.ASYNC = value == Qt.Checked

            if col in self.HEADERS.DUTS:
                if tc_inst:
                    tc_inst.skip_tc_dut = value == Qt.Unchecked

        # FINAL -------------------------------------------------------------------------------------------------------
        self._data_reread()
        return True


# =====================================================================================================================
