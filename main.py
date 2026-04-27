from player import Player
from quest import Quest
from enemy import Enemy, fight
from shop import Shop
from save_manager import save_game, load_game

def main():
    print("=" * 65)
    print("🏰 WELCOME TO THE SILVER BLADE GUILD 🏰")
    print("=" * 65)
    
    # Try to load saved game
    loaded_player, loaded_unlocked = load_game()
    
    if loaded_player:
        player = loaded_player
        unlocked_quests = loaded_unlocked
        print("Welcome back, adventurer!")
    else:
        player_name = input("Enter your adventurer's name: > ").strip()
        if not player_name:
            player_name = "Hero"
        player = Player(player_name)
        unlocked_quests = ["goblin"]
        print(f"\n🎉 Welcome to the guild, {player.name}!\n")
    
    shop = Shop()
    
    # Define all quests
    quests = {
        "goblin": Quest("Goblin Trouble", "Defeat 3 goblins harassing the village.", 30, 60, 3),
        "wolf": Quest("Forest Menace", "Defeat 2 wolves on the forest road.", 45, 90, 2),
        "bandit": Quest("Road Bandits", "Defeat 1 bandit leader ambushing merchants.", 70, 150, 1)
    }
    
    show_guild_hall(player, quests, unlocked_quests)
    
    while True:
        if player.health <= 0:
            print("\n💀 GAME OVER - You have been defeated...")
            print("Better luck next time, adventurer.")
            break
        
        # Check victory condition
        if all(q.completed for q in [quests[k] for k in unlocked_quests if k in quests]):
            print("\n🎊 CONGRATULATIONS!")
            print(f"{player.name}, you have completed all available quests!")
            print("You are now a respected member of the Silver Blade Guild.")
            print("Thank you for playing Guild Quest!")
            save_game(player, unlocked_quests)
            break
        
        cmd = input("\n> ").strip().lower()
        
        if cmd in ["quit", "exit"]:
            save_game(player, unlocked_quests)
            print(f"\nFarewell, {player.name}. Your progress has been saved.")
            break
            
        elif cmd == "help":
            print("\n📜 Commands:")
            print("  help            - Show this help")
            print("  stats           - Show character stats")
            print("  hall            - Return to Guild Hall")
            print("  questboard      - Show available quests")
            print("  accept <name>   - Accept a quest (goblin / wolf / bandit)")
            print("  quests          - View your active quests")
            print("  fight           - Fight for active combat quests")
            print("  shop            - Visit the Guild Shop")
            print("  use <item>      - Use an item from inventory")
            print("  save            - Manually save your progress")
            print("  quit            - Exit and save")
            
        elif cmd == "stats":
            player.show_stats()
            
        elif cmd in ["hall", "guild", "guild_hall"]:
            show_guild_hall(player, quests, unlocked_quests)
            
        elif cmd == "questboard":
            show_quest_board(quests, unlocked_quests)
            
        elif cmd.startswith("accept "):
            quest_key = cmd[7:].strip()
            if quest_key in unlocked_quests and quest_key in quests:
                if quests[quest_key] not in player.active_quests:
                    player.accept_quest(quests[quest_key])
                else:
                    print("You already accepted this quest.")
            else:
                print("Quest not available.")
                
        elif cmd == "quests":
            player.show_active_quests()
            
        elif cmd == "fight":
            handle_fight(player, quests, unlocked_quests)
            save_game(player, unlocked_quests)  # Auto-save after combat
            
        elif cmd == "shop":
            shop.show_items()
            
        elif cmd.startswith("buy "):
            try:
                item_index = int(cmd.split()[1])
                bought_item = shop.buy_item(player, item_index)
                if bought_item:
                    player.add_to_inventory(bought_item)
                    save_game(player, unlocked_quests)
            except (IndexError, ValueError):
                print("Usage: buy <number>")
                
        elif cmd.startswith("use "):
            item_name = cmd[4:].strip()
            player.use_item(item_name)
            save_game(player, unlocked_quests)
            
        elif cmd == "save":
            save_game(player, unlocked_quests)
            
        else:
            print("❌ Unknown command. Type 'help' for options.")

def show_guild_hall(player, quests, unlocked_quests):
    print("\n" + "="*60)
    print("🏛️  GUILD HALL")
    print("="*60)
    print("You stand in the lively main hall of the Silver Blade Guild.\n")
    print("Available actions:")
    print("  • questboard      - See available quests")
    print("  • accept <name>   - Accept a quest")
    print("  • fight           - Engage in combat")
    print("  • shop            - Buy potions")
    print("  • save            - Save your progress")

def show_quest_board(quests, unlocked_quests):
    print("\n" + "="*50)
    print("📋 QUEST BOARD")
    print("="*50)
    for key in unlocked_quests:
        q = quests[key]
        status = "✅ Completed" if q.completed else f"⏳ ({q.progress}/{q.goal})"
        print(f"• {q.title} ({key}) - {status}")
        print(f"  {q.description}")
        print(f"  Reward: {q.reward_gold}g + {q.reward_exp}xp\n")

def handle_fight(player, quests, unlocked_quests):
    active_combat_quests = [q for q in player.active_quests if not q.completed and q.goal > 0]
    if not active_combat_quests:
        print("No active combat quests. Accept one from the quest board.")
        return
    
    current_quest = active_combat_quests[0]
    
    if current_quest.title == "Goblin Trouble":
        enemy = Enemy("Goblin", 25, 6, 8, 15)
    elif current_quest.title == "Forest Menace":
        enemy = Enemy("Wolf", 35, 9, 12, 25)
    else:
        enemy = Enemy("Bandit", 50, 12, 20, 40)
    
    if fight(player, enemy):
        current_quest.progress += 1
        if current_quest.progress >= current_quest.goal:
            current_quest.completed = True
            player.gold += current_quest.reward_gold
            player.gain_exp(current_quest.reward_exp)
            print(f"\n🎉 QUEST COMPLETED: {current_quest.title}!")
            
            # Unlock next quest
            if current_quest.title == "Goblin Trouble" and "wolf" not in unlocked_quests:
                unlocked_quests.append("wolf")
                print("🌲 New quest unlocked: Forest Menace!")
            elif current_quest.title == "Forest Menace" and "bandit" not in unlocked_quests:
                unlocked_quests.append("bandit")
                print("🏴‍☠️ New quest unlocked: Road Bandits!")

if __name__ == "__main__":
    main()
