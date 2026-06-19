import random
import time
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

def show_title_screen():
    print(Fore.CYAN + "\n" + "═" * 95)
    print(Fore.YELLOW + "🏰  THE SILVER BLADE GUILD  🏰".center(95))
    print(Fore.CYAN + "═" * 95 + Style.RESET_ALL)
    print(Fore.WHITE + f"          Version {VERSION} - Final Release".center(95))
    print(Fore.WHITE + "       Built commit-by-commit\n".center(95))
    
    time.sleep(0.8)
    print(Fore.WHITE + "The grand doors of the Silver Blade Guild open...")
    time.sleep(1.1)
    print(Fore.GREEN + "Your legend as a new adventurer begins now...\n")
    time.sleep(0.7)

def main():
    show_title_screen()

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

# Keep your helper functions (show_help, show_inventory, show_victory_screen, handle_buy, etc.)

if __name__ == "__main__":
    main()
