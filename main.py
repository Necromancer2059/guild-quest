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

        # ... (all commands and helper functions from previous versions)

        else:
            print(Fore.RED + "❌ Unknown command. Type 'help'.")

if __name__ == "__main__":
    main()
