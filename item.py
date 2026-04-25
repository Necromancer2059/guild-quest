class Item:
    def __init__(self, name: str, description: str, price: int, heal_amount: int = 0):
        self.name = name
        self.description = description
        self.price = price
        self.heal_amount = heal_amount

    def use(self, player):
        if self.heal_amount > 0:
            player.heal(self.heal_amount)
            print(f"🧪 You used {self.name} and restored {self.heal_amount} health!")
            return True
        return False
