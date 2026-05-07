import json
import os
from player import Player
from quest import Quest

SAVE_DIR = "saves"
os.makedirs(SAVE_DIR, exist_ok=True)

def get_save_path(slot: int):
    return f"{SAVE_DIR}/save_slot_{slot}.json"

def save_game(player, unlocked_quests, slot: int = 1):
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
        },
        "unlocked_quests": unlocked_quests,
        "active_quests": [q.title for q in player.active_quests if not q.completed]
    }
    
    try:
        with open(get_save_path(slot), "w") as f:
            json.dump(data, f, indent=2)
        print(f"💾 Game saved to Slot {slot}!")
    except Exception as e:
        print(f"Save failed: {e}")

def load_game(slot: int = 1):
    path = get_save_path(slot)
    if not os.path.exists(path):
        return None, None
    
    try:
        with open(path, "r") as f:
            data = json.load(f)
        
        player = Player(data["player"]["name"])
        player.level = data["player"]["level"]
        player.health = data["player"]["health"]
        player.max_health = data["player"]["max_health"]
        player.attack = data["player"]["attack"]
        player.gold = data["player"]["gold"]
        player.exp = data["player"]["exp"]
        player.exp_to_next_level = data["player"]["exp_to_next_level"]
        
        print(f"✅ Loaded Slot {slot} - {player.name} (Level {player.level})")
        return player, data.get("unlocked_quests", ["goblin"])
    except:
        print(f"Failed to load Slot {slot}")
        return None, None

def list_saves():
    print("\n📂 Saved Games:")
    print("="*40)
    found = False
    for i in range(1, 4):
        path = get_save_path(i)
        if os.path.exists(path):
            try:
                with open(path) as f:
                    data = json.load(f)
                    print(f"Slot {i}: {data['player']['name']} - Level {data['player']['level']}")
                found = True
            except:
                print(f"Slot {i}: Corrupted")
    if not found:
        print("No saves found yet.")
