import random
import os
from colorama import init, Fore, Style

# Initialize colors
init(autoreset=True)

from player import Player
from quest import Quest
from enemy import Enemy, fight
from shop import Shop
from save_manager import save_game, load_game, list_saves
from achievements import AchievementSystem
from location import create_locations

def main():
    print(Fore.CYAN + "\n" + "═" * 78)
    print(Fore.YELLOW + "🏰  THE SILVER BLADE GUILD  🏰".center(78))
    print(Fore.CYAN + "═" * 78)

    player, unlocked_quests = load_or_create_player()
    
    shop = Shop()
    locations = create_locations()
    current_location = locations["guild_hall"]
    achievement_system = AchievementSystem()
    player.achievement_system = achievement_system

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
        elif cmd.startswith("go "):
            loc_key = cmd[3:].strip()
            if loc_key in locations:
                current_location = locations[loc_key]
                print(Fore.CYAN + f"\n🚶 You travel to the {current_location.name}.")
                print(Fore.WHITE + current_location.description)
            else:
                print(Fore.RED + "Unknown location.")
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
                    print(Fore.GREEN + "✅ Character loaded successfully!")
            except:
                print(Fore.RED + "Usage: load <1-3>")
        elif cmd == "saves":
            list_saves()
        else:
            print(Fore.RED + "❌ Unknown command. Type 'help'.")

# === Helper Functions (with colors) ===
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

def show_help():
    print(Fore.CYAN + "\n📜 Available Commands:" + Style.RESET_ALL)
    print("  help, stats, achievements, questboard, go <location>")
    print("  fight, shop, buy <num>, use <item>, equip <item>")
    print("  rest (in hall), save <1-3>, load <1-3>, saves, quit")

def show_victory_screen(player):
    print(Fore.YELLOW + "\n" + "★" * 78)
    print("🏆  LEGENDARY VICTORY  🏆".center(78))
    print("★" * 78 + Style.RESET_ALL)
    print(Fore.GREEN + f"\nCongratulations, {player.name}!")
    player.show_stats()

# Keep your existing helper functions (handle_buy, handle_use, handle_fight, etc.)
# You can keep them the same as the previous full main.py I gave you.

if __name__ == "__main__":
    main()            handle_buy(cmd, player, shop, unlocked_quests)
        elif cmd.startswith("use "):
            handle_use(cmd, player, unlocked_quests)
        elif cmd.startswith("equip "):
            player.equip_item(cmd[6:].strip())
        elif cmd.startswith("go "):
            handle_travel(cmd[3:].strip(), locations, current_location)
            current_location = locations.get(cmd[3:].strip(), current_location)
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
                    print("✅ Character loaded successfully!")
            except:
                print("Usage: load <1-3>")
        elif cmd == "saves":
            list_saves()
        else:
            print("❌ Unknown command. Type 'help' for the list of commands.")

def load_or_create_player():
    # Try to load slot 1 by default
    player, unlocked = load_game(1)
    if player:
        print(f"Welcome back, {player.name}!")
        return player, unlocked
    else:
        name = input("What is your name, adventurer? > ").strip()
        if not name:
            name = "Hero"
        player = Player(name)
        print(f"\n🎉 Welcome to the Silver Blade Guild, {name}!\n")
        return player, ["goblin"]

def create_quests():
    return {
        "goblin": Quest("Goblin Trouble", "Defeat 3 goblins near the village.", 35, 70, 3),
        "wolf": Quest("Forest Menace", "Clear 2 wolves from the eastern forest road.", 50, 100, 2),
        "bandit": Quest("Road Bandits", "Eliminate the bandit leader on the trade route.", 80, 160, 1),
        "dragon": Quest("Dragon of Eldergloom", "Defeat the ancient dragon to save the kingdom!", 250, 600, 1, True)
    }

def show_help():
    print("\n📜 Available Commands:")
    print("  help                    - Show this help")
    print("  stats                   - Show character stats")
    print("  achievements            - Show achievements")
    print("  questboard              - Show available quests")
    print("  accept <name>           - Accept a quest")
    print("  go <location>           - Travel (guild_hall, forest, cave, dragon_lair)")
    print("  fight                   - Fight in current location")
    print("  shop                    - Visit the shop")
    print("  buy <number>            - Buy item")
    print("  use <item>              - Use item")
    print("  equip <item>            - Equip weapon or armor")
    print("  rest                    - Rest (only in Guild Hall)")
    print("  save <1-3>              - Save game")
    print("  load <1-3>              - Load game")
    print("  saves                   - List all saves")
    print("  quit                    - Save and exit")

def show_victory_screen(player):
    print("\n" + "★" * 75)
    print("🏆  LEGENDARY VICTORY  🏆".center(75))
    print("★" * 75)
    print(f"\nCongratulations, {player.name}!")
    print("You have defeated the Dragon and become a legend of the guild!")
    player.show_stats()

def handle_buy(cmd, player, shop, unlocked_quests):
    try:
        idx = int(cmd.split()[1])
        item = shop.buy_item(player, idx)
        if item:
            player.add_to_inventory(item)
            save_game(player, unlocked_quests, 1)
    except:
        print("Usage: buy <number>")

def handle_use(cmd, player, unlocked_quests):
    item_name = cmd[4:].strip()
    if player.use_item(item_name):
        save_game(player, unlocked_quests, 1)

def handle_travel(location_key, locations, current_location):
    if location_key in locations:
        print(f"\n🚶 You travel to the **{locations[location_key].name}**.")
        print(locations[location_key].description)
    else:
        print("Unknown location. Try: guild_hall, forest, cave, dragon_lair")

def handle_fight(player, current_location, achievement_system):
    if current_location.name == "Guild Hall":
        print("It's peaceful here. No enemies in the Guild Hall.")
        return
    enemy = current_location.get_random_enemy()
    if enemy:
        if fight(player, enemy):
            if "Goblin" in enemy.name:
                achievement_system.stats["goblins_killed"] += 1
            elif "Wolf" in enemy.name:
                achievement_system.stats["wolves_killed"] += 1
            achievement_system.check_achievements(player)
    else:
        print("No enemies here right now.")

def rest_at_guild(player):
    heal_amount = 40
    player.heal(heal_amount)
    if player.achievement_system:
        player.achievement_system.stats["rests"] += 1
        player.achievement_system.check_achievements(player)

def accept_quest(quest_key, player, quests, unlocked_quests):
    if quest_key in unlocked_quests and quest_key in quests:
        if quests[quest_key] not in player.active_quests:
            player.accept_quest(quests[quest_key])
        else:
            print("You already accepted this quest.")
    else:
        print("Quest not available or not unlocked.")

def show_quest_board(quests, unlocked_quests):
    print("\n📋 QUEST BOARD")
    print("="*50)
    for key in unlocked_quests:
        q = quests[key]
        status = "✅ Completed" if q.completed else "⏳ Available"
        print(f"• {q.title} [{status}]")
        print(f"   {q.description}")
        print(f"   Reward: {q.reward_gold} gold + {q.reward_exp} EXP\n")

if __name__ == "__main__":
    main()
