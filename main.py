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

def main():
    print(Fore.CYAN + "\n" + "═" * 80)
    print(Fore.YELLOW + "🏰  THE SILVER BLADE GUILD  🏰".center(80))
    print(Fore.CYAN + "═" * 80 + Style.RESET_ALL)

    player, unlocked_quests = load_or_create_player()
    
    shop = Shop()
    locations = create_locations()
    current_location = locations["guild_hall"]
    achievement_system = AchievementSystem()
    player.achievement_system = achievement_system
    player.skill_system = SkillSystem()

    quests = create_quests()

    print(Fore.GREEN + f"\n📍 You are in: {current_location.name}\n")

    while True:
        if player.health <= 0:
            print(Fore.RED + "\n💀 YOU HAVE BEEN DEFEATED... Better luck next time.")
            break

        if all(q.completed for q in quests.values()):
            show_victory_screen(player)
            save_game(player, unlocked_quests, 1)
            break

        cmd = input(Fore.WHITE + "\n> " + Style.RESET_ALL).strip().lower()

        if cmd in ["quit", "exit"]:
            save_game(player, unlocked_quests, 1)
            print(Fore.YELLOW + f"\n👋 Farewell, {player.name}! Your legend lives on.")
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
                    print(Fore.GREEN + f"✅ Loaded Slot {slot} successfully!")
            except:
                print(Fore.RED + "Usage: load <1-3>")
        elif cmd == "saves":
            list_saves()
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
        "wolf": Quest("Forest Menace", "Clear 2 wolves from the eastern forest road.", 50, 100, 2),
        "bandit": Quest("Road Bandits", "Eliminate the bandit leader.", 80, 160, 1),
        "dragon": Quest("Dragon of Eldergloom", "Defeat the ancient dragon!", 250, 600, 1, True)
    }

def show_help():
    print(Fore.CYAN + "\n📜 Commands:" + Style.RESET_ALL)
    print("  help | stats | achievements | skills | questboard")
    print("  go <place> | fight | shop | buy <num> | use <item> | equip <item>")
    print("  rest (in hall) | save <1-3> | load <1-3> | saves | quit")

def show_victory_screen(player):
    print(Fore.YELLOW + "\n" + "★" * 80)
    print("🏆  LEGENDARY VICTORY  🏆".center(80))
    print("★" * 80 + Style.RESET_ALL)
    print(Fore.GREEN + f"\nCongratulations, {player.name}! You are now a Guild Legend!\n")
    player.show_stats()

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
        trigger_random_event()
        return new_loc
    else:
        print(Fore.RED + "Unknown location. Available: guild_hall, forest, cave, dragon_lair")
        return current

def trigger_random_event():
    events = [
        "You hear distant howling...",
        "A traveling merchant offers you a small discount next time.",
        "You found 5 gold on the ground!",
        "The wind carries whispers of an ancient dragon..."
    ]
    print(Fore.MAGENTA + f"✨ {random.choice(events)}")

def handle_fight(player, current_location, achievement_system):
    if current_location.name == "Guild Hall":
        print(Fore.YELLOW + "It's peaceful here.")
        return
    enemy = current_location.get_random_enemy()
    if enemy:
        if fight(player, enemy):
            if "Goblin" in enemy.name: achievement_system.stats["goblins_killed"] += 1
            if "Wolf" in enemy.name: achievement_system.stats["wolves_killed"] += 1
            achievement_system.check_achievements(player)
    else:
        print("No enemies here right now.")

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
        else:
            print("You already have this quest.")
    else:
        print("Quest not available.")

def show_quest_board(quests, unlocked_quests):
    print(Fore.CYAN + "\n📋 QUEST BOARD" + Style.RESET_ALL)
    print("="*55)
    for key in unlocked_quests:
        q = quests[key]
        status = "✅ Completed" if q.completed else "⏳ Available"
        print(f"• {q.title} [{status}]")
        print(f"   {q.description}\n")

if __name__ == "__main__":
    main()
