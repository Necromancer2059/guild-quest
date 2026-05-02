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
    
    loaded_player, loaded_unlocked = load_game()
    
    if loaded_player:
        player = loaded_player
        unlocked_quests = loaded_unlocked
        print(f"Welcome back, {player.name}!\n")
    else:
        player_name = input("What is your name, adventurer? > ").strip()
        if not player_name:
            player_name = "Hero"
        player = Player(player_name)
        unlocked_quests = ["goblin"]
        print(f"\n🎉 Welcome to the Silver Blade Guild, {player.name}!\n")
    
    shop = Shop()
    
    quests = {
        "goblin": Quest("Goblin Trouble", "Defeat 3 goblins near the village.", 35, 70, 3),
        "wolf": Quest("Forest Menace", "Clear 2 wolves from the eastern forest road.", 50, 100, 2),
        "bandit": Quest("Road Bandits", "Eliminate the bandit leader on the trade route.", 80, 160, 1),
        "dragon": Quest("Dragon of Eldergloom", 
                       "The ancient dragon has awakened! Defeat it to save the kingdom.",
                       reward_gold=250, reward_exp=600, goal=1, is_boss=True)
    }
    
    show_guild_hall(player)
    
    while True:
        if player.health <= 0:
            print("\n💀 YOU HAVE BEEN DEFEATED...")
            break
        
        if all(q.completed for q in quests.values()):
            show_victory_screen(player)
            save_game(player, unlocked_quests)
            break
        
        cmd = input("\n> ").strip().lower()
        
        if cmd in ["quit", "exit"]:
            save_game(player, unlocked_quests)
            print(f"\n👋 Farewell, {player.name}!")
            break
            
        elif cmd == "help":
            show_help()
            
        elif cmd == "stats":
            player.show_stats()
            
        elif cmd in ["hall", "guild", "guild_hall"]:
            show_guild_hall(player)
            
        elif cmd == "questboard":
            show_quest_board(quests, unlocked_quests)
            
        elif cmd.startswith("accept "):
            quest_key = cmd[7:].strip()
            if quest_key in unlocked_quests:
                if quests[quest_key] not in player.active_quests:
                    player.accept_quest(quests[quest_key])
                else:
                    print("✅ You already accepted this quest.")
            else:
                print("Quest not unlocked yet.")
                
        elif cmd == "quests":
            player.show_active_quests()
            
        elif cmd == "fight":
            handle_fight(player, quests, unlocked_quests)
            save_game(player, unlocked_quests)
            
        elif cmd == "shop":
            shop.show_items()
            
        elif cmd.startswith("buy "):
            try:
                idx = int(cmd.split()[1])
                item = shop.buy_item(player, idx)
                if item:
                    player.add_to_inventory(item)
                    save_game(player, unlocked_quests)
            except:
                print("Usage: buy <number>")
                
        elif cmd.startswith("use "):
            item_name = cmd[4:].strip()
            if player.use_item(item_name):
                save_game(player, unlocked_quests)
                
        elif cmd == "save":
            save_game(player, unlocked_quests)
            print("💾 Progress saved!")
            
        elif cmd == "rest":
            rest_at_guild(player)
            
        elif cmd == "credits":
            show_credits()
            
        else:
            print("❌ Unknown command. Type 'help' for the full list.")

def show_guild_hall(player):
    print("\n" + "─"*65)
    print("🏛️  GUILD HALL".center(65))
    print("─"*65)
    
    events = [
        "A bard is singing tales of past heroes.",
        "An old adventurer gives you a nod of respect.",
        "A merchant is haggling loudly over rare ingredients.",
        "Sparks fly from the blacksmith's hammer.",
        "A group of rookies is training in the courtyard.",
        "The guild master glances at you approvingly."
    ]
    print(random.choice(events))
    print("The quest board is calling your name...\n")
    print("Tip: You can now type 'rest' to recover some health.")

def rest_at_guild(player):
    heal_amount = 30
    player.heal(heal_amount)
    print("You rested by the fireplace and feel refreshed.")

# (Keep the other functions: show_quest_board, show_help, show_victory_screen, 
# show_credits, handle_fight the same as in Commit #10)

if __name__ == "__main__":
    main()
