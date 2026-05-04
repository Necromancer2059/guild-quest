class Item:
    def __init__(self, name: str, description: str, price: int, heal_amount: int = 0, 
                 attack_bonus: int = 0, health_bonus: int = 0, is_equipment: bool = False):
        self.name = name
        self.description = description
        self.price = price
        self.heal_amount = heal_amount
        self.attack_bonus = attack_bonus
        self.health_bonus = health_bonus
        self.is_equipment = is_equipment
        self.equipped = False

    def use(self, player):
        if self.heal_amount > 0:
            player.heal(self.heal_amount)
            return True
        return False
