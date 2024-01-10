from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from pyqt_templates import TableModelTemplate

from .tp import TpManager


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
        if col > 0:
            dut = self.DATA.DUTS[col-1]
        else:
            dut = None

        # -------------------------------------------------------------------------------------------------------------
        if role == Qt.DisplayRole:
            if col == 0:
                return f'{tc.name}\n{tc.DESCRIPTION}'
            if col > 0:
                result = dut.TP_RESULTS[tc].result
                if result is None:
                    return ""
                else:
                    return f'{result}'

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
