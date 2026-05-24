import random
from colorama import init, Fore, Style

init(autoreset=True)

from player import Player
from quest import Quest
from enemy import Enemy, fight
from shop import Shop
from save_manager import save_game, load_game, list_saves
from achievements import AchievementSystem
from location import create_locations
from skills import SkillSystem
from item import Item

VERSION = "1.0.0"

def main():
    print(Fore.CYAN + "\n" + "═" * 95)
    print(Fore.YELLOW + "🏰  THE SILVER BLADE GUILD  🏰".center(95))
    print(Fore.CYAN + "═" * 95 + Style.RESET_ALL)
    print(Fore.WHITE + f"          Version {VERSION} - Final Release\n".center(95))

    player, unlocked_quests = load_or_create_player()
    
    shop = Shop()
    locations = create_locations()
    current_location = locations["guild_hall"]
    achievement_system = AchievementSystem()
    player.achievement_system = achievement_system
    player.skill_system = SkillSystem()

    quests = create_quests()

    print(Fore.GREEN + f"\n📍 Current Location: {current_location.name}\n")

    while True:
        if player.health <= 0:
            print(Fore.RED + "\n💀 YOU HAVE BEEN DEFEATED...")
            break

        if all(q.completed for q in quests.values()):
            show_victory_screen(player)
            save_game(player, unlocked_quests, 1)
            break

        cmd = input(Fore.WHITE + "\n> " + Style.RESET_ALL).strip().lower()

        if cmd in ["quit", "exit"]:
            save_game(player, unlocked_quests, 1)
            print(Fore.YELLOW + f"\n👋 Farewell, {player.name}!")
            break

        elif cmd == "help":
            show_help()
        elif cmd == "stats":
            player.show_stats()
        elif cmd == "achievements":
            achievement_system.show_achievements()
        elif cmd == "skills":
            player.skill_system.show_skills()
        elif cmd == "questboard":
            show_quest_board(quests, unlocked_quests)
        elif cmd.startswith("accept "):
            accept_quest(cmd[7:].strip(), player, quests, unlocked_quests)
        elif cmd == "quests":
            player.show_active_quests()
        elif cmd == "shop":
            shop.show_items()
        elif cmd.startswith("buy "):
            handle_buy(cmd, player, shop, unlocked_quests)
        elif cmd.startswith("use "):
            handle_use(cmd, player, unlocked_quests)
        elif cmd.startswith("equip "):
            player.equip_item(cmd[6:].strip())
        elif cmd == "inventory":
            show_inventory(player)
        elif cmd.startswith("go "):
            current_location = handle_go(cmd[3:].strip(), locations, current_location)
        elif cmd == "fight":
            handle_fight(player, current_location, achievement_system)
        elif cmd == "rest" and current_location.name == "Guild Hall":
            rest_at_guild(player)
        elif cmd.startswith("save "):
            try:
                slot = int(cmd.split()[1])
                save_game(player, unlocked_quests, slot)
            except:
                save_game(player, unlocked_quests, 1)
        elif cmd.startswith("load "):
            try:
                slot = int(cmd.split()[1])
                new_player, new_unlocked = load_game(slot)
                if new_player:
                    player = new_player
                    unlocked_quests = new_unlocked or ["goblin"]
                    player.achievement_system = achievement_system
                    player.skill_system = SkillSystem()
                    print(Fore.GREEN + f"✅ Loaded Slot {slot}!")
            except:
                print(Fore.RED + "Usage: load <1-3>")
        elif cmd == "saves":
            list_saves()
        elif cmd == "craft":
            show_crafting(player, unlocked_quests)
        elif cmd in ["version", "about"]:
            print(Fore.CYAN + f"\nGuild Quest v{VERSION} - Final Release")
        else:
            print(Fore.RED + "❌ Unknown command. Type 'help'.")

def load_or_create_player():
    player, unlocked = load_game(1)
    if player:
        print(Fore.GREEN + f"Welcome back, {player.name}!")
        return player, unlocked
    else:
        name = input(Fore.WHITE + "What is your name, adventurer? > " + Style.RESET_ALL).strip() or "Hero"
        player = Player(name)
        print(Fore.GREEN + f"\n🎉 Welcome to the Silver Blade Guild, {name}!\n")
        return player, ["goblin"]

def create_quests():
    return {
        "goblin": Quest("Goblin Trouble", "Defeat 3 goblins near the village.", 35, 70, 3),
        "wolf": Quest("Forest Menace", "Clear 2 wolves from the forest road.", 50, 100, 2),
        "bandit": Quest("Road Bandits", "Defeat the bandit leader.", 80, 160, 1),
        "dragon": Quest("Dragon of Eldergloom", "Defeat the ancient dragon!", 250, 600, 1, True)
    }

def show_help():
    print(Fore.CYAN + "\n📜 Available Commands:" + Style.RESET_ALL)
    print("  help | stats | achievements | skills | questboard | inventory | craft")
    print("  go <location> | fight | shop | buy <num> | use <item> | equip <item>")
    print("  rest | save <1-3> | load <1-3> | saves | version | quit")

def show_inventory(player):
    print(Fore.MAGENTA + "\n🎒 INVENTORY" + Style.RESET_ALL)
    print("=" * 60)
    if not player.inventory:
        print("Your inventory is empty.")
    else:
        for i, item in enumerate(player.inventory, 1):
            status = " [Equipped]" if (getattr(player, 'equipped_weapon', None) == item or getattr(player, 'equipped_armor', None) == item) else ""
            print(f"{i}. {item.name}{status}")
    print("=" * 60)

def show_victory_screen(player):
    print(Fore.YELLOW + "\n" + "★" * 92)
    print("🏆  LEGENDARY VICTORY  🏆".center(92))
    print("★" * 92 + Style.RESET_ALL)
    print(Fore.GREEN + f"\nCongratulations, {player.name}!")
    print("You have completed all quests and defeated the Dragon of Eldergloom!")
    print("You are now a true Legend of the Silver Blade Guild.\n")
    player.show_stats()

def show_crafting(player, unlocked_quests):
    print(Fore.MAGENTA + "\n🔨 CRAFTING BENCH" + Style.RESET_ALL)
    print("=" * 60)
    print("1. Iron Sword      → 40 Gold")
    print("2. Steel Armor     → 65 Gold")
    print("3. Strong Potion   → 25 Gold")
    print("4. Mystic Ring     → 100 Gold (+5 Attack)")
    
    try:
        choice = input(Fore.WHITE + "\nCraft > " + Style.RESET_ALL).strip()
        crafted = None
        if choice == "1" and player.gold >= 40:
            player.gold -= 40
            crafted = Item("Iron Sword", "A reliable blade", 0, 0, attack_bonus=10, is_equipment=True)
        elif choice == "2" and player.gold >= 65:
            player.gold -= 65
            crafted = Item("Steel Armor", "Strong protection", 0, 0, health_bonus=35, is_equipment=True)
        elif choice == "3" and player.gold >= 25:
            player.gold -= 25
            crafted = Item("Strong Potion", "Restores 50 health", 0, heal_amount=50)
        elif choice == "4" and player.gold >= 100:
            player.gold -= 100
            crafted = Item("Mystic Ring", "Magical ring", 0, 0, attack_bonus=5, is_equipment=True)

        if crafted:
            player.add_to_inventory(crafted)
            print(Fore.GREEN + f"✅ Crafted: {crafted.name}!")
            save_game(player, unlocked_quests, 1)
    except:
        print(Fore.RED + "Crafting cancelled.")

# Helper Functions
def handle_buy(cmd, player, shop, unlocked_quests):
    try:
        idx = int(cmd.split()[1])
        item = shop.buy_item(player, idx)
        if item:
            player.add_to_inventory(item)
            save_game(player, unlocked_quests, 1)
    except:
        print(Fore.RED + "Usage: buy <number>")

def handle_use(cmd, player, unlocked_quests):
    if player.use_item(cmd[4:].strip()):
        save_game(player, unlocked_quests, 1)

def handle_go(loc_key, locations, current):
    if loc_key in locations:
        new_loc = locations[loc_key]
        print(Fore.CYAN + f"\n🚶 Traveling to {new_loc.name}...")
        print(Fore.WHITE + new_loc.description)
        return new_loc
    else:
        print(Fore.RED + "Unknown location.")
        return current

def handle_fight(player, current_location, achievement_system):
    if current_location.name == "Guild Hall":
        print(Fore.YELLOW + "It's peaceful here.")
        return
    enemy = current_location.get_random_enemy()
    if enemy and fight(player, enemy):
        drop = get_random_drop(enemy)
        if drop:
            player.add_to_inventory(drop)
            print(Fore.GREEN + f"🎁 Dropped: {drop.name}!")
        achievement_system.check_achievements(player)

def get_random_drop(enemy):
    if random.random() < 0.45:
        drops = [
            Item("Goblin Ear", "Trophy", 8),
            Item("Wolf Fang", "Sharp fang", 12),
            Item("Healing Herb", "Restores 20 HP", 0, heal_amount=20),
            Item("Rusty Dagger", "Old weapon", 0, 0, attack_bonus=4, is_equipment=True)
        ]
        return random.choice(drops)
    return None

def rest_at_guild(player):
    player.heal(45)
    if player.achievement_system:
        player.achievement_system.stats["rests"] += 1
        player.achievement_system.check_achievements(player)

def accept_quest(quest_key, player, quests, unlocked_quests):
    if quest_key in unlocked_quests and quest_key in quests:
        if quests[quest_key] not in player.active_quests:
            player.accept_quest(quests[quest_key])
            print(Fore.GREEN + f"✅ Accepted: {quests[quest_key].title}")

def show_quest_board(quests, unlocked_quests):
    print(Fore.CYAN + "\n📋 QUEST BOARD" + Style.RESET_ALL)
    print("="*65)
    for key in unlocked_quests:
        q = quests[key]
        status = "✅ Completed" if q.completed else "⏳ Available"
        print(f"• {q.title} [{status}]")
        print(f"   {q.description}\n")

if __name__ == "__main__":
    main()
