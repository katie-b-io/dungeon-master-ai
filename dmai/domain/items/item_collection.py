from dmai.utils.loader import Loader
from dmai.utils.exceptions import UnrecognisedItem
from dmai.domain.items.potion_of_healing import PotionOfHealing
from dmai.domain.items.item import Item


class ItemCollection:

    # class variables
    item_data = dict()

    def __init__(self) -> None:
        """ItemCollection class"""
        self.items = {}
        self._load_item_data()

    def __repr__(self) -> str:
        return "Item collection:\n{a}".format(a=self.items)

    def _load_item_data(self) -> None:
        """Set the self.item_data class variable data"""
        self.item_data = Loader.load_domain("magic_items")
        
    def _item_factory(self, item: str) -> Item:
        """Construct an item of specified type"""
        if item in self.item_data.keys():
            item_map = {"potion_of_healing": PotionOfHealing}
            if item in item_map:
                item_obj = item_map[item]
            else:
                item_obj = Item
        else:
            msg = "Cannot create item {e} - it does not exist!".format(
                e=item)
            raise UnrecognisedItem(msg)
        return item_obj(self.item_data[item])

    def _check_item(self, item_id: str) -> bool:
        """Method to return whether specified item exists.
        Returns a boolean."""
        if item_id not in self.item_data:
            msg = "Item {e} does not exist!".format(e=item_id)
            raise UnrecognisedItem(msg)
        return True

    def add_item(self, item_id: str, quantity: int = 1) -> bool:
        """Method to add specified item to inventory."""
        if self._check_item(item_id):
            if item_id in self.items:
                self.items[item_id]["quantity"] += quantity
            else:
                item_obj = self._item_factory(item_id)
                self.items[item_id] = {
                    "item": item_obj,
                    "quantity": quantity
                }
            return True
        return False
        
    def remove_item(self, item_id: str, quantity: int = 1) -> None:
        """Method to remove item of specified quantity from inventory."""
        if self._check_item(item_id):
            if item_id in self.items:
                self.items[item_id]["quantity"] -= quantity
            for item_id in self.items:
                if self.items[item_id]["quantity"] <= 0:
                    del self.items[item_id]
    
    def clear_items(self) -> None:
        """Method to clear inventory."""
        self.items = {}

    def has_item(self, item_id: str) -> tuple:
        """Method to return whether specified item exists.
        Returns a tuple with the boolean and a string with a reason."""
        try:
            if self._check_item(item_id):
                if not item_id in self.items:
                    return (False, "not in inventory")
                return (True, "")
            return (False, "unknown")
        except UnrecognisedItem:
            return (False, "unknown")

    def quantity_above_zero(self, item_id: str) -> bool:
        """Method to return whether quantity of specified item is above zero"""
        if item_id in self.items:
            return self.items[item_id]["quantity"] > 0

    def use_item(self, item_id: str) -> bool:
        """Method to use specified item.
        Returns bool for whether item was used"""
        try:
            if self._check_item(item_id):
                (has_item, reason) = self.has_item(item_id)
                if has_item:
                    self.items[item_id]["quantity"] = self.items[item_id]["quantity"] - 1
                    return self.items[item_id]["item"].use()
            return False
        except UnrecognisedItem:
            return False

    def stop_using_item(self, item_id: str) -> bool:
        """Method to stop using specified item.
        Returns bool for whether item was stopped being used"""
        try:
            if self._check_item(item_id):
                if item_id in self.items:
                    return self.items[item_id]["item"].stop()
            return False
        except UnrecognisedItem:
            return False

    def get_all(self) -> list:
        """Return a list with all the item ids"""
        return self.items.keys()

    def get_item(self, item_id: str) -> Item:
        """Return a query item object"""
        try:
            if self._check_item(item_id):
                if item_id in self.items:
                    return self.items[item_id]["item"]
            return False
        except UnrecognisedItem:
            return False

    def get_name(self, item_id: str) -> Item:
        """Return a query item name"""
        if item_id in self.item_data:
            return self.item_data[item_id]["name"]
        else:
            return item_id
        
    def get_formatted(self, item_id: str) -> str:
        """Return the formatted item with quantities"""
        if item_id in self.item_data:
            quantity = self.items[item_id]
            item = self.item_data[item_id]
            if self.items[item_id] == 1:
                return item["name"]
            else:
                return "{q} {e}".format(q=quantity, e=item["name"])
