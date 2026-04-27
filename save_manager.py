import json
import os
from player import Player
from quest import Quest

def save_game(player, unlocked_quests):
    """Save player progress and unlocked quests to file"""
    data = {
        "player": {
            "name": player.name,
            "level": player.level,
            "health": player.health,
            "max_health": player.max_health,
            "attack": player.attack,
            "gold": player.gold,
            "exp": player.exp,
            "exp_to_next_level": player.exp_to_next_level,
            "active_quests": [
                {
                    "title": q.title,
                    "progress": q.progress,
                    "completed": q.completed
                } for q in player.active_quests
            ],
            "inventory": [item.name for item in player.inventory]
        },
        "unlocked_quests": unlocked_quests
    }
    
    try:
        with open("save_game.json", "w") as f:
            json.dump(data, f, indent=2)
        print("💾 Game saved successfully!")
    except Exception as e:
        print(f"Failed to save game: {e}")

def load_game():
    """Load player progress from file"""
    if not os.path.exists("save_game.json"):
        print("No save file found. Starting new game.")
        return None, None
    
    try:
        with open("save_game.json", "r") as f:
            data = json.load(f)
        
        # Re-create player
        player = Player(data["player"]["name"])
        player.level = data["player"]["level"]
        player.health = data["player"]["health"]
        player.max_health = data["player"]["max_health"]
        player.attack = data["player"]["attack"]
        player.gold = data["player"]["gold"]
        player.exp = data["player"]["exp"]
        player.exp_to_next_level = data["player"]["exp_to_next_level"]
        
        # Note: inventory and active quests are simplified for this commit
        print(f"✅ Loaded saved game for {player.name} (Level {player.level})")
        return player, data.get("unlocked_quests", ["goblin"])
        
    except Exception as e:
        print(f"Failed to load game: {e}")
        return None, None
