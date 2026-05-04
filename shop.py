from item import Item

class Shop:
    def __init__(self):
        self.items = [
            # Potions
            Item("Small Health Potion", "Restores 25 health", price=15, heal_amount=25),
            Item("Medium Health Potion", "Restores 45 health", price=28, heal_amount=45),
            # Weapons
            Item("Iron Sword", "A sturdy iron sword", price=60, attack_bonus=8, is_equipment=True),
            Item("Steel Axe", "Heavy axe that hits hard", price=90, attack_bonus=12, is_equipment=True),
            # Armor
            Item("Leather Armor", "Basic protection", price=50, health_bonus=20, is_equipment=True),
            Item("Chainmail Vest", "Decent armor", price=85, health_bonus=35, is_equipment=True),
        ]

    def show_items(self):
        print("\n🛒 GUILD SHOP")
        print("=" * 50)
        for i, item in enumerate(self.items, 1):
            print(f"  {i}. {item.name} - {item.price} gold")
            print(f"     {item.description}")
            if item.attack_bonus > 0:
                print(f"     ⚔️  +{item.attack_bonus} Attack")
            if item.health_bonus > 0:
                print(f"     ❤️  +{item.health_bonus} Max Health")
        print("\nType 'buy <number>' to purchase.")
