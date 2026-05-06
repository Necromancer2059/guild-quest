import random
from enemy import Enemy

class Location:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.enemies = []

    def get_random_enemy(self):
        if not self.enemies:
            return None
        return random.choice(self.enemies)

# Predefined locations
def create_locations():
    locations = {
        "guild_hall": Location("Guild Hall", "The safe and bustling heart of the Silver Blade Guild."),
        "forest": Location("Whispering Forest", "A dense forest filled with dangerous wildlife."),
        "cave": Location("Shadow Cave", "A dark and damp cave system near the mountains."),
        "dragon_lair": Location("Dragon's Lair", "The scorched ruins where the ancient dragon sleeps.")
    }
    
    # Add enemies to locations
    locations["forest"].enemies = [
        Enemy("Goblin", 25, 6, 8, 15),
        Enemy("Wolf", 35, 9, 12, 25),
        Enemy("Giant Spider", 28, 7, 10, 18)
    ]
    
    locations["cave"].enemies = [
        Enemy("Cave Troll", 60, 12, 25, 40),
        Enemy("Skeleton Warrior", 45, 10, 15, 30),
        Enemy("Bat Swarm", 20, 5, 5, 12)
    ]
    
    locations["dragon_lair"].enemies = [
        Enemy("Ancient Dragon", 110, 18, 120, 300)
    ]
    
    return locations
