from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from pyqt_templates import TableModelTemplate

# from .tp import TpMultyDutBase
from .tc import TcReadyState


# =====================================================================================================================
class TpTableModel(TableModelTemplate):
    DATA: "TpMultyDutBase"

    # AUX -------------------------------------------
    open__settings: Optional[bool] = None
    ADDITIONAL_COLUMNS: int = 3

    def rowCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.TCS__CLS)

    def columnCount(self, parent: QModelIndex = None, *args, **kwargs) -> int:
        return len(self.DATA.DEVICES__CLS.LIST__DUT) + self.ADDITIONAL_COLUMNS

    def headerData(self, section: Any, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> str:
        if role == Qt.DisplayRole:
            # ------------------------------
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "ТЕСТКЕЙС"
                if section == 1:
                    return "READY"
                if section == 2:
                    return "ASYNC"
                if section >= self.ADDITIONAL_COLUMNS:
                    return f"{section - self.ADDITIONAL_COLUMNS + 1}"
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
        if col == 1:
            pass
        if col == 2:
            if self.open__settings:
                flags |= Qt.ItemIsUserCheckable
        if col >= self.ADDITIONAL_COLUMNS:
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
        tc = list(self.DATA.TCS__CLS)[row]

        dut = None
        tc_dut = None
        if col >= self.ADDITIONAL_COLUMNS:
            dut = self.DATA.DEVICES__CLS.LIST__DUT[col - self.ADDITIONAL_COLUMNS]
            tc_dut = tc.TCS__INST[dut.INDEX]

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DisplayRole:
            if col == 0:
                return f'{tc.NAME}\n{tc.DESCRIPTION}'
            if col == 1:
                return '+' if tc.ready == TcReadyState.READY else '-'
            if col == 2:
                return '+' if tc.ASYNC else '-'
            if col >= self.ADDITIONAL_COLUMNS:
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
            if col == 1:
                if tc.ready == TcReadyState.READY:
                    return QColor("#50FF50")
                if tc.ready == TcReadyState.WARN:
                    return QColor("#5050FF")
                if tc.ready == TcReadyState.FAIL:
                    return QColor("#FF5050")

            if col >= self.ADDITIONAL_COLUMNS:
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

                if col == 1:
                    pass

                if col == 2:
                    if tc.ASYNC:
                        return Qt.Checked
                    else:
                        return Qt.Unchecked

                if col >= self.ADDITIONAL_COLUMNS:
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
        tc = list(self.DATA.TCS__CLS)[row]

        dut = None
        tc_dut = None
        if col >= self.ADDITIONAL_COLUMNS:
            dut = self.DATA.DEVICES__CLS.LIST__DUT[col - self.ADDITIONAL_COLUMNS]
            tc_dut = tc.TCS__INST[dut.INDEX]

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.CheckStateRole:
            if col == 0:
                tc.SKIP = value == Qt.Unchecked

            if col == 1:
                pass

            if col == 2:
                tc.ASYNC = value == Qt.Checked

            if col >= self.ADDITIONAL_COLUMNS:
                if tc_dut:
                    tc_dut.skip_tc_dut = value == Qt.Unchecked

        # FINAL -------------------------------------------------------------------------------------------------------
        self._data_reread()
        return True


# =====================================================================================================================
