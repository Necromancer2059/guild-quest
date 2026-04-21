    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)
        print(f"❤️  You healed for {amount} health. Current health: {self.health}/{self.max_health}")
