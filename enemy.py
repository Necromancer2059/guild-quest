import random

class Enemy:
    def __init__(self, name: str, health: int, attack: int, gold_reward: int, exp_reward: int):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.gold_reward = gold_reward
        self.exp_reward = exp_reward

    def is_alive(self) -> bool:
        return self.health > 0

def fight(player, enemy):
    print(f"\n⚔️  A wild {enemy.name} appears!")
    
    while player.health > 0 and enemy.is_alive():
        print("\n" + "-"*40)
        print(f"❤️  Your Health: {player.health}/{player.max_health}")
        print(f"🟥 Enemy Health: {enemy.health}/{enemy.max_health}")
        
        action = input("\nWhat do you do? (attack / run) > ").strip().lower()
        
        if action == "attack":
            # Player attacks
            damage = random.randint(player.attack - 3, player.attack + 3)
            enemy.health -= damage
            print(f"✅ You hit the {enemy.name} for {damage} damage!")
            
            if not enemy.is_alive():
                print(f"🎉 You defeated the {enemy.name}!")
                player.gold += enemy.gold_reward
                player.gain_exp(enemy.exp_reward)
                return True
                
            # Enemy attacks back
            enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 2)
            player.health -= enemy_damage
            print(f"💥 The {enemy.name} hits you for {enemy_damage} damage!")
            
        elif action == "run":
            if random.random() < 0.7:  # 70% chance to escape
                print("🏃 You successfully ran away!")
                return False
            else:
                print("❌ You failed to escape!")
                # Enemy still attacks
                enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 2)
                player.health -= enemy_damage
                print(f"💥 The {enemy.name} hits you for {enemy_damage} damage!")
        else:
            print("Invalid action. Type 'attack' or 'run'.")
    
    if player.health <= 0:
        print("\n💀 You have been defeated...")
        print("Game Over.")
        return False
    
    return True
