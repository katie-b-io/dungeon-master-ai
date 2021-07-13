from dmai.utils.output_builder import OutputBuilder
from dmai.game.state import State
from dmai.utils.loader import Loader
from dmai.utils.exceptions import UnrecognisedItem
from dmai.domain.items.potion_of_healing import PotionOfHealing
from dmai.domain.items.silver_key import SilverKey
from dmai.domain.items.bronze_key import BronzeKey
from dmai.domain.items.item import Item
from dmai.utils.text import Text


class ItemCollection:

    # class variables
    item_data = dict()

    def __init__(self, state: State, output_builder: OutputBuilder) -> None:
        """ItemCollection class"""
        self.items = {}
        self.state = state
        self.output_builder = output_builder
        self._load_item_data()

        # prepare the items
        for item_id in self.state.item_quantity:
            item_obj = self._item_factory(item_id)
            self.items[item_id] = item_obj

    def __repr__(self) -> str:
        return "Item collection"

    def _load_item_data(self) -> None:
        """Set the self.item_data class variable data"""
        self.item_data = Loader.load_domain("magic_items")
        self.item_data["silver_key"] = {
            "name": "Silver Key",
            "type": "item",
            "description": "A simple silver key"
        }
        self.item_data["bronze_key"] = {
            "name": "Bronze Key",
            "type": "item",
            "description": "An elaborate bronze key"
        }
        
    def _item_factory(self, item: str) -> Item:
        """Construct an item of specified type"""
        if item in self.item_data.keys():
            item_map = {
                "potion_of_healing": PotionOfHealing,
                "silver_key": SilverKey,
                "bronze_key": BronzeKey
            }
            if item in item_map:
                item_obj = item_map[item]
            else:
                item_obj = Item
        else:
            msg = "Cannot create item {e} - it does not exist!".format(
                e=item)
            raise UnrecognisedItem(msg)
        return item_obj(self.item_data[item], self.state, self.output_builder)

    def _check_item(self, item_id: str) -> bool:
        """Method to return whether specified item exists.
        Returns a boolean."""
        if item_id not in self.item_data:
            return False
        return True

    def add_item(self, item_id: str, quantity: int = 1, item_data: dict = None) -> bool:
        """Method to add specified item to inventory."""
        if self._check_item(item_id):
            if item_id in self.state.item_quantity:
                self.state.item_quantity[item_id] += quantity
            else:
                item_obj = self._item_factory(item_id)
                self.items[item_id] = item_obj
                self.state.item_quantity[item_id] = quantity
            return True
        elif item_data:
            # new item to add to the inventory
            self.item_data[item_id] = item_data
            self.state.item_quantity[item_id] = quantity
            return True
        return False
        
    def remove_item(self, item_id: str, quantity: int = 1) -> None:
        """Method to remove item of specified quantity from inventory."""
        if self._check_item(item_id):
            if item_id in self.state.item_quantity:
                self.state.item_quantity[item_id] -= quantity
                if self.state.item_quantity[item_id] <= 0:
                    del self.state.item_quantity[item_id]
    
    def clear_items(self) -> None:
        """Method to clear inventory."""
        self.state.item_quantity = {}

    def has_item(self, item_id: str) -> tuple:
        """Method to return whether specified item exists.
        Returns a tuple with the boolean and a string with a reason."""
        try:
            if self._check_item(item_id):
                if not item_id in self.state.item_quantity:
                    return (False, "not in inventory")
                return (True, "")
            return (False, "unknown")
        except UnrecognisedItem:
            return (False, "unknown")

    def quantity_above_zero(self, item_id: str) -> bool:
        """Method to return whether quantity of specified item is above zero"""
        if item_id in self.state.item_quantity:
            return self.state.item_quantity[item_id] > 0

    def use_item(self, item_id: str) -> bool:
        """Method to use specified item.
        Returns bool for whether item was used"""
        try:
            if self._check_item(item_id):
                (has_item, reason) = self.has_item(item_id)
                if has_item:
                    used = self.items[item_id].use()
                    if used:
                        self.remove_item(item_id)
                    return used
            return False
        except UnrecognisedItem:
            return False

    def stop_using_item(self, item_id: str) -> bool:
        """Method to stop using specified item.
        Returns bool for whether item was stopped being used"""
        try:
            if self._check_item(item_id):
                if item_id in self.state.item_quantity:
                    return self.items[item_id].stop()
            return False
        except UnrecognisedItem:
            return False

    def get_all(self) -> list:
        """Return a list with all the item ids"""
        return self.state.item_quantity.keys()

    def get_item(self, item_id: str) -> Item:
        """Return a query item object"""
        try:
            if self._check_item(item_id):
                if item_id in self.state.item_quantity:
                    return self.items[item_id]
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
            quantity = self.state.item_quantity[item_id]
            item = self.item_data[item_id]
            if quantity == 1:
                return item["name"]
            else:
                return "{q} {e}".format(q=quantity, e=item["name"])
    
    def get_all_formatted(self) -> str:
        """Return the whole item collection properly formatted"""
        if not bool(self.get_all()):
            return "You have no items in your inventory."
        
        all = []
        for item in self.get_all():
            all.append(self.get_formatted(item))
        return "In your inventory you have {i}.".format(i=Text.properly_format_list(all))
