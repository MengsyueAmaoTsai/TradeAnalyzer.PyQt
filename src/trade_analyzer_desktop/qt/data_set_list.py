from typing import Optional, List, Union

from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QWidget
from PyQt6.QtCore import pyqtSignal

from .data_set_list_item import DataSetListItem
from ..analysis import StatisticsResults


class DataSetList(QListWidget):

    item_checked: pyqtSignal = pyqtSignal(str, bool)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.__data_set_list_items: List[DataSetListItem] = [] 
    # -------------------------------------------------- Properties --------------------------------------------------
    @property
    def items(self) -> List[DataSetListItem]:
        """
        Returns all items in list.
        """
        return self.__data_set_list_items
    
    @property
    def checked_items(self) -> List[DataSetListItem]:
        """
        Returns current checked items
        """
        return list(filter(lambda item: item.is_checked and not item.is_benchmark, self.items))

    # -------------------------------------------------- Event Handlers --------------------------------------------------
    def on_data_set_item_checked(self, key: str, checked: bool) -> None:

        if len(self.checked_items) == 0:
            self.get_item(key).is_checked = True

        elif key.startswith("Benchmark") or len(self.checked_items) > 0:
            self.item_checked.emit(key, checked)

    # -------------------------------------------------- Public Methods --------------------------------------------------
    def add_data(self, key: str, statistics_results: StatisticsResults) -> None:
        """
        Add a data set item to list.
        """
        list_item: QListWidgetItem = QListWidgetItem()
        list_item_widget: DataSetListItem = DataSetListItem(self)
        list_item_widget.key = key 
        list_item_widget.statistics_results = statistics_results 
        list_item_widget.is_checked = True
        list_item_widget.checked.connect(self.on_data_set_item_checked)
        self.addItem(list_item)
        self.setItemWidget(list_item, list_item_widget)   
        self.__data_set_list_items.append(list_item_widget)

    def get_item(self, key: str) -> DataSetListItem:
        """
        Get data set item by key.
        """
        item: Union[DataSetListItem, None] = next(filter(lambda result: result.key == key, self.__data_set_list_items), None)
        assert(item is not None)
        return item
    
    # -------------------------------------------------- Private Method --------------------------------------------------
    