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
        print("=" * 40)
