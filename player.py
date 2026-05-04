    def __init__(self, name: str):
        # ... existing code ...
        self.inventory = []
        self.equipped_weapon = None
        self.equipped_armor = None

    def show_stats(self):
        weapon = self.equipped_weapon.name if self.equipped_weapon else "None"
        armor = self.equipped_armor.name if self.equipped_armor else "None"
        
        print("=" * 45)
        print(f"👤 {self.name} - Level {self.level}")
        print("=" * 45)
        print(f"❤️  Health : {self.health}/{self.max_health}")
        print(f"⚔️  Attack : {self.attack}")
        print(f"💰 Gold   : {self.gold}")
        print(f"⭐ EXP    : {self.exp}/{self.exp_to_next_level}")
        print(f"🗡️  Weapon : {weapon}")
        print(f"🛡️  Armor  : {armor}")
        print(f"🎒 Inventory : {len(self.inventory)} items")
        print("=" * 45)

    def equip_item(self, item_name: str):
        for item in self.inventory:
            if item.is_equipment and item_name.lower() in item.name.lower():
                if item.attack_bonus > 0:  # Weapon
                    if self.equipped_weapon:
                        print(f"Unequipped {self.equipped_weapon.name}")
                    self.equipped_weapon = item
                    print(f"⚔️  Equipped {item.name} (+{item.attack_bonus} Attack)")
                else:  # Armor
                    if self.equipped_armor:
                        print(f"Unequipped {self.equipped_armor.name}")
                    self.equipped_armor = item
                    self.max_health += item.health_bonus
                    self.health += item.health_bonus
                    print(f"🛡️  Equipped {item.name} (+{item.health_bonus} Max Health)")
                item.equipped = True
                return True
        print("Item not found or cannot be equipped.")
        return False
