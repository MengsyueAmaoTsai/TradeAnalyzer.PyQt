from typing import Optional, Union

from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QComboBox, QDoubleSpinBox, QPushButton, QMessageBox, QLabel, QDialog
from PyQt6.QtCore import pyqtSignal

from ..enums import Side, StrategyType, TradingPlatform, Resolution
from ..entities import Strategy
from ..repositories import StrategyRepository

class EditStrategyDialog(QDialog):

    strategy_updated: pyqtSignal = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        # Widgets
        self.__id_input: QLineEdit = QLineEdit(self)
        self.__id_input.setEnabled(False)
        self.__id_input.textChanged.connect(self.on_id_text_changed)
        
        self.__description_input: QLineEdit = QLineEdit(self)

        self.__type_combo: QComboBox = QComboBox(self)

        self.__resolution_combo: QComboBox = QComboBox(self)

        self.__side_combo: QComboBox = QComboBox(self)

        self.__platform_combo: QComboBox = QComboBox(self)

        self.__starting_capital_spinbox: QDoubleSpinBox = QDoubleSpinBox(self)

        self.__save_button: QPushButton = QPushButton("Save", self)
        self.__save_button.clicked.connect(self.on_save_button_clicked)
        self.__save_button.setEnabled(False)

        self.__close_button: QPushButton = QPushButton("Close", self)
        self.__close_button.clicked.connect(self.on_close_button_clicked)   

        # Layout
        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(QLabel("Strategy Id"), 0, 0, 1, 1)
        layout.addWidget(self.__id_input, 0, 1, 1, 3)
        
        layout.addWidget(QLabel("Description"), 1, 0, 1, 1)
        layout.addWidget(self.__description_input, 1, 1, 1, 3)

        layout.addWidget(QLabel("Type"), 2, 0, 1, 1)
        layout.addWidget(self.__type_combo, 2, 1, 1, 3)    

        layout.addWidget(QLabel("Resolution"), 3, 0, 1, 1)
        layout.addWidget(self.__resolution_combo, 3, 1, 1, 3)    

        layout.addWidget(QLabel("Side"), 4, 0, 1, 1)
        layout.addWidget(self.__side_combo, 4, 1, 1, 3)

        layout.addWidget(QLabel("Platform"), 5, 0, 1, 1)
        layout.addWidget(self.__platform_combo, 5, 1, 1, 3)

        layout.addWidget(QLabel("Starting Capital"), 6, 0, 1, 1)
        layout.addWidget(self.__starting_capital_spinbox, 6, 1, 1, 3)

        layout.addWidget(self.__save_button, 7, 2, 1, 1)
        layout.addWidget(self.__close_button, 7, 3, 1, 1)

        # Default Data
        for i, type in enumerate(StrategyType):
            self.__type_combo.addItem(type.value, type)
            
        for i, side in enumerate(Side):
            self.__side_combo.addItem(side.value, side)

        for i, resolution in enumerate(Resolution):
            self.__resolution_combo.addItem(resolution.value, resolution)

        for i, platform in enumerate(TradingPlatform):
            self.__platform_combo.addItem(platform.value, platform)

        self.__starting_capital_spinbox.setMaximum(10000 * 100000)
        self.__starting_capital_spinbox.setMinimum(10000 * 10)
        self.__starting_capital_spinbox.setValue(10000 * 1000)
        self.__starting_capital_spinbox.setSingleStep(1000)
        
    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def id(self) -> str:
        return self.__id_input.text().strip()

    @id.setter
    def id(self, id: str) -> None:
        self.__id_input.setText(id.strip())
    
    @property
    def description(self) -> str:
        return self.__description_input.text().strip()

    @description.setter
    def description(self, description: str) -> None:
        self.__description_input.setText(description.strip())

    @property
    def type(self) -> StrategyType:
        return self.__type_combo.currentData()

    @type.setter
    def type(self, type: StrategyType) -> None:
        index: int = list(StrategyType).index(type)
        self.__type_combo.setCurrentIndex(index)

    @property
    def resolution(self) -> Resolution:
        return self.__resolution_combo.currentData()

    @resolution.setter
    def resolution(self, resolution: Resolution) -> None:
        index: int = list(Resolution).index(resolution)
        self.__resolution_combo.setCurrentIndex(index)

    @property
    def side(self) -> Side:
        return self.__side_combo.currentData()

    @side.setter
    def side(self, side: Side) -> None:
        index: int = list(Side).index(side)
        self.__side_combo.setCurrentIndex(index)

    @property
    def platform(self) -> TradingPlatform:
        return self.__platform_combo.currentData()

    @platform.setter
    def platform(self, platform: TradingPlatform) -> None:
        index: int = list(TradingPlatform).index(platform)
        self.__platform_combo.setCurrentIndex(index)

    @property
    def starting_capital(self) -> float:
        return self.__starting_capital_spinbox.value()

    @starting_capital.setter
    def starting_capital(self, starting_capital: float) -> None:
        self.__starting_capital_spinbox.setValue(starting_capital)
        
    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_id_text_changed(self, id: str) -> None:
        self.__save_button.setEnabled(True) if not (id.isspace() or id.__eq__(str())) else self.__save_button.setEnabled(False)

    def on_save_button_clicked(self, checked: bool) -> None:
        strategy: Union[Strategy, None] = StrategyRepository.query_by_id(self.id)
        if not strategy:
            return 
        
        strategy.id = self.id
        strategy.description = self.description
        strategy.type = self.type
        strategy.resolution = self.resolution
        strategy.side = self.side
        strategy.platform = self.platform
        strategy.starting_capital = self.starting_capital

        result: bool = StrategyRepository.update(strategy)
        
        if not result:
            QMessageBox.warning(self, "WARN", "Error.")
            return

        QMessageBox.information(self, "INFO", "Strategy updated.")
        self.close()
        self.strategy_updated.emit()
        return 

    def on_close_button_clicked(self, checked: bool) -> None:
        self.close()

    # -------------------------------------------------- Public Methods --------------------------------------------------
    # -------------------------------------------------- Private Methods --------------------------------------------------
