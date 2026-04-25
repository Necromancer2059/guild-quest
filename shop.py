from item import Item

class Shop:
    def __init__(self):
        self.items = [
            Item("Small Health Potion", "Restores 25 health", price=15, heal_amount=25),
            Item("Medium Health Potion", "Restores 40 health", price=25, heal_amount=40),
        ]

    def show_items(self):
        print("\n🛒 GUILD SHOP")
        print("=" * 40)
        print("Welcome to the guild shop! What would you like to buy?\n")
        for i, item in enumerate(self.items, 1):
            print(f"  {i}. {item.name} - {item.price} gold")
            print(f"     {item.description}")
        print("\nType 'buy 1' to purchase the first item, etc.")

    def buy_item(self, player, item_index: int):
        if item_index < 1 or item_index > len(self.items):
            print("Invalid item number.")
            return None
        
        item = self.items[item_index - 1]
        
        if player.gold < item.price:
            print(f"❌ Not enough gold! You need {item.price} gold.")
            return None
        
        player.gold -= item.price
        print(f"✅ Purchased: {item.name} for {item.price} gold.")
        return item
