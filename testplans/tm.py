from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from pyqt_templates import TableModelTemplate

from .tp import TestPlanBase


# =====================================================================================================================
class TpTableModel(TableModelTemplate):
    DATA: TestPlanBase

    # AUX -------------------------------------------
    open__settings: Optional[bool] = None

    def rowCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.TCS)

    def columnCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.DUTS) + 2

    def headerData(self, section: Any, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> str:
        if role == Qt.DisplayRole:
            # ------------------------------
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "ТЕСТКЕЙС"
                if section == 1:
                    return "ACYNC"
                if section > 1:
                    return f"{section-1}"
            # ------------------------------
            if orientation == Qt.Vertical:
                return str(section + 1)

    def flags(self, index: QModelIndex) -> int:
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()

        # -------------------------------------------------------------------------------------------------------------
        flags = super().flags(index)

        if col == 0:
            flags |= Qt.ItemIsUserCheckable
            # flags |= Qt.ItemIsSelectable
        if col > 1:
            if self.open__settings:
                flags |= Qt.ItemIsUserCheckable
                # flags |= Qt.ItemIsSelectable
        else:
            # flags -= Qt.ItemIsSelectable
            pass
        return flags

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        # PREPARE -----------------------------------------------------------------------------------------------------
        col = index.column()
        row = index.row()
        tc = list(self.DATA.TCS)[row]

        dut = None
        tc_dut = None
        if col > 1:
            dut = self.DATA.DUTS[col-2]
            tc_dut = dut.TP_RESULTS[tc]

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DisplayRole:
            if col == 0:
                return f'{tc.NAME}\n{tc.DESCRIPTION}'
            if col == 1:
                return '+' if tc.ACYNC else '-'
            if col > 1:
                if tc_dut:
                    if tc_dut.result is None:
                        return ""
                    else:
                        return f'{tc_dut.result}'

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
                return QColor('#e2e2e2')

            if col > 1:
                if tc_dut.skip_tc_dut or not dut.PRESENT or dut.SKIP:
                    return QColor('#e2e2e2')
                if tc_dut.result is True:
                    return QColor("#00FF00")
                if tc_dut.result is False:
                    return QColor("#FF5050")
                if tc_dut.progress > 0:
                    return QColor("#FFFF50")

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:
            if self.open__settings:
                if col == 0:
                    if tc.SKIP:
                        return Qt.Unchecked
                    else:
                        return Qt.Checked

                if col > 1:
                    if not tc_dut.SKIP and not dut.SKIP:
                        if tc_dut.skip_tc_dut:
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
        tc = list(self.DATA.TCS)[row]

        dut = None
        tc_dut = None
        if col > 1:
            dut = self.DATA.DUTS[col-2]
            tc_dut = dut.TP_RESULTS[tc]

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:
            if col == 0:
                tc.SKIP = value == Qt.Unchecked

            if col > 1:
                if tc_dut:
                    tc_dut.skip_tc_dut = value == Qt.Unchecked

        # FINAL -------------------------------------------------------------------------------------------------------
        self._data_reread()
        return True


# =====================================================================================================================