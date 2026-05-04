import random
from player import Player
from quest import Quest
from enemy import Enemy, fight
from shop import Shop
from save_manager import save_game, load_game

def main():
    print("\n" + "═"*72)
    print("🏰  THE SILVER BLADE GUILD  🏰".center(72))
    print("═"*72)
    
    player, unlocked_quests = load_or_create_player()
    shop = Shop()
    quests = create_quests()
    
    show_guild_hall(player)
    
    while True:
        if check_game_over(player):
            break
        if check_victory(quests):
            show_victory_screen(player)
            break
        
        handle_command(input("\n> ").strip().lower(), player, quests, unlocked_quests, shop)

def load_or_create_player():
    loaded_player, loaded_unlocked = load_game()
    if loaded_player:
        print(f"Welcome back, {loaded_player.name}!\n")
        return loaded_player, loaded_unlocked
    else:
        name = input("What is your name, adventurer? > ").strip() or "Hero"
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

def handle_command(cmd, player, quests, unlocked_quests, shop):
    if cmd in ["quit", "exit"]:
        save_game(player, unlocked_quests)
        print(f"\n👋 Farewell, {player.name}!")
        exit()
    
    actions = {
        "help": lambda: show_help(),
        "stats": player.show_stats,
        "hall": lambda: show_guild_hall(player),
        "questboard": lambda: show_quest_board(quests, unlocked_quests),
        "quests": player.show_active_quests,
        "shop": shop.show_items,
        "save": lambda: (save_game(player, unlocked_quests), print("💾 Saved!")),
        "credits": show_credits,
        "rest": lambda: rest_at_guild(player)
    }
    
    if cmd in actions:
        actions[cmd]()
    elif cmd.startswith("accept "):
        accept_quest(cmd[7:].strip(), player, quests, unlocked_quests)
    elif cmd.startswith("buy "):
        try:
            item = shop.buy_item(player, int(cmd.split()[1]))
            if item:
                player.add_to_inventory(item)
                save_game(player, unlocked_quests)
        except:
            print("Usage: buy <number>")
    elif cmd.startswith("use "):
        if player.use_item(cmd[4:].strip()):
            save_game(player, unlocked_quests)
    elif cmd == "fight":
        handle_fight(player, quests, unlocked_quests)
        save_game(player, unlocked_quests)
    else:
        print("❌ Unknown command. Type 'help'.")

# (All other helper functions like show_guild_hall, rest_at_guild, show_help, etc. remain the same as previous commit)

if __name__ == "__main__":
    main()
        elif cmd.startswith("equip "):
            item_name = cmd[6:].strip()
            player.equip_item(item_name)
            save_game(player, unlocked_quests)
