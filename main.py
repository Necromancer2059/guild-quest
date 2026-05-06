import random
from player import Player
from quest import Quest
from enemy import Enemy, fight
from shop import Shop
from save_manager import save_game, load_game
from achievements import AchievementSystem
from location import create_locations

def main():
    print("\n" + "═"*72)
    print("🏰  THE SILVER BLADE GUILD  🏰".center(72))
    print("═"*72)
    
    player, unlocked_quests = load_or_create_player()
    shop = Shop()
    locations = create_locations()
    current_location = locations["guild_hall"]
    achievement_system = AchievementSystem()
    player.achievement_system = achievement_system
    
    quests = create_quests()
    
    print(f"Current Location: {current_location.name}\n")
    
    while True:
        if player.health <= 0:
            print("\n💀 YOU HAVE BEEN DEFEATED...")
            break
        if all(q.completed for q in quests.values()):
            show_victory_screen(player)
            break
        
        cmd = input("\n> ").strip().lower()
        
        if cmd in ["quit", "exit"]:
            save_game(player, unlocked_quests)
            print("👋 Farewell!")
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
            # ... existing buy logic ...
            pass
        elif cmd.startswith("use "):
            # ... existing use logic ...
            pass
        elif cmd.startswith("equip "):
            player.equip_item(cmd[6:].strip())
        elif cmd.startswith("go "):
            location_key = cmd[3:].strip()
            if location_key in locations:
                current_location = locations[location_key]
                print(f"\nYou travel to **{current_location.name}**.")
                print(current_location.description)
            else:
                print("Unknown location. Available: guild_hall, forest, cave, dragon_lair")
        elif cmd == "fight":
            enemy = current_location.get_random_enemy()
            if enemy:
                if fight(player, enemy):
                    # Track kills etc.
                    player.achievement_system.check_achievements(player)
            else:
                print("There are no enemies here right now.")
        elif cmd == "rest" and current_location.name == "Guild Hall":
            rest_at_guild(player)
        else:
            print("Unknown command. Type 'help'.")

def show_help():
    print("\nCommands:")
    print("  go <place>     - Travel (guild_hall, forest, cave, dragon_lair)")
    print("  fight          - Fight in current location")
    print("  hall / go guild_hall - Return to safety")
    print("  questboard, accept, shop, equip, rest (in hall), achievements...")

# Keep your other helper functions (show_victory_screen, rest_at_guild, etc.)

if __name__ == "__main__":
    main()
