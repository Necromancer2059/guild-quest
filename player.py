from quest import Quest
from item import Item

class Player:
    def __init__(self, name: str):
        self.name = name
        self.level = 1
        self.max_health = 50
        self.health = self.max_health
        self.attack = 10
        self.gold = 25
        self.exp = 0
        self.exp_to_next_level = 100
        self.active_quests = []
        self.inventory = []  # New: inventory list
    
    def gain_exp(self, amount: int):
        self.exp += amount
        print(f"💰 Gained {amount} experience!")
        if self.exp >= self.exp_to_next_level:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.attack += 5
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)
        print(f"🎉 LEVEL UP! You are now level {self.level}!")
        print(f"   Health: {self.max_health} | Attack: {self.attack}")
    
    def show_stats(self):
        print("=" * 40)
        print(f"👤 {self.name} - Level {self.level}")
        print("=" * 40)
        print(f"❤️  Health : {self.health}/{self.max_health}")
        print(f"⚔️  Attack : {self.attack}")
        print(f"💰 Gold   : {self.gold}")
        print(f"⭐ EXP    : {self.exp}/{self.exp_to_next_level}")
        print(f"📜 Active Quests: {len(self.active_quests)}")
        print(f"🎒 Inventory : {len(self.inventory)} items")
        print("=" * 40)
    
    def accept_quest(self, quest: Quest):
        if quest not in self.active_quests:
            self.active_quests.append(quest)
            print(f"✅ Accepted quest: {quest.title}")
        else:
            print("You already have this quest!")
    
    def show_active_quests(self):
        if not self.active_quests:
            print("You have no active quests.")
            return
        print("\n" + "="*40)
        print("📋 YOUR ACTIVE QUESTS")
        print("="*40)
        for quest in self.active_quests:
            quest.show_details()
    
    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)
        print(f"❤️  You healed for {amount} health. Current health: {self.health}/{self.max_health}")
    
    # New methods for inventory
    def add_to_inventory(self, item: Item):
        self.inventory.append(item)
        print(f"🎒 Added {item.name} to your inventory.")
    
    def use_item(self, item_name: str):
        for i, item in enumerate(self.inventory):
            if item.name.lower() == item_name.lower() or item_name.lower() in item.name.lower():
                if item.use(self):
                    del self.inventory[i]
                    return True
        print(f"Item '{item_name}' not found in inventory.")
        return False
