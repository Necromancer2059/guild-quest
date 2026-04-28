import random
from player import Player
from quest import Quest
from enemy import Enemy, fight
from shop import Shop
from save_manager import save_game, load_game

def main():
    print("\n" + "═"*70)
    print("🏰  THE SILVER BLADE GUILD  🏰".center(70))
    print("═"*70)
    
    # Load or create new player
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
    
    # All quests including final boss
    quests = {
        "goblin": Quest("Goblin Trouble", "Defeat 3 goblins near the village.", 30, 60, 3),
        "wolf": Quest("Forest Menace", "Clear 2 wolves from the eastern forest road.", 45, 90, 2),
        "bandit": Quest("Road Bandits", "Eliminate the bandit leader on the trade route.", 70, 150, 1),
        "dragon": Quest("Dragon of Eldergloom", 
                       "The ancient dragon has awakened! Defeat it to save the kingdom.",
                       reward_gold=200, reward_exp=500, goal=1, is_boss=True)
    }
    
    show_guild_hall()
    
    while True:
        if player.health <= 0:
            print("\n💀 YOU HAVE BEEN DEFEATED...")
            print("Your journey ends here. The guild will remember your bravery.")
            break
        
        # Victory condition
        if all(q.completed for q in quests.values()):
            show_victory_screen(player)
            save_game(player, unlocked_quests)
            break
        
        cmd = input("\n> ").strip().lower()
        
        if cmd in ["quit", "exit"]:
            save_game(player, unlocked_quests)
            print(f"\n👋 Farewell, {player.name}. Your legend continues in the guild archives.")
            break
            
        elif cmd == "help":
            show_help()
            
        elif cmd == "stats":
            player.show_stats()
            
        elif cmd in ["hall", "guild", "guild_hall"]:
            show_guild_hall()
            
        elif cmd == "questboard":
            show_quest_board(quests, unlocked_quests)
            
        elif cmd.startswith("accept "):
            quest_key = cmd[7:].strip()
            if quest_key in unlocked_quests:
                if quests[quest_key] not in player.active_quests:
                    player.accept_quest(quests[quest_key])
                else:
                    print("You have already accepted this quest.")
            else:
                print("This quest is not yet unlocked.")
                
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
            
        else:
            print("❌ Unknown command. Type 'help' to see all commands.")

def show_guild_hall():
    print("\n" + "─"*60)
    print("🏛️  GUILD HALL".center(60))
    print("─"*60)
    print("The hall is filled with the sound of laughter and steel being sharpened.")
    print("A large quest board stands proudly on the wall.\n")
    print("Commands: questboard, accept <name>, fight, shop, stats, save")

def show_quest_board(quests, unlocked_quests):
    print("\n" + "📋 QUEST BOARD".center(60))
    print("─"*60)
    for key in unlocked_quests:
        q = quests[key]
        tag = " 🔥 BOSS" if q.is_boss else ""
        status = "✅ Completed" if q.completed else "⏳ Available"
        print(f"• {q.title}{tag}  [{status}]")
        print(f"  → {q.description}")
        print(f"  Reward: {q.reward_gold} gold + {q.reward_exp} EXP\n")

def show_help():
    print("\n📜 Available Commands:")
    print("  help              - Show this help")
    print("  stats             - View your character sheet")
    print("  hall              - Return to the Guild Hall")
    print("  questboard        - View available quests")
    print("  accept <name>     - Accept a quest (goblin, wolf, bandit, dragon)")
    print("  quests            - List your active quests")
    print("  fight             - Battle for your current quest")
    print("  shop              - Visit the guild shop")
    print("  use <item>        - Use item from inventory")
    print("  save              - Save your progress")
    print("  quit              - Save and exit the game")

def show_victory_screen(player):
    print("\n" + "★"*70)
    print("🏆  LEGENDARY VICTORY  🏆".center(70))
    print("★"*70)
    print(f"\nCongratulations, {player.name}!")
    print("You have defeated the Dragon of Eldergloom and brought peace to the land.")
    print("Your name will be forever etched in the halls of the Silver Blade Guild.")
    print("\nFinal Stats:")
    player.show_stats()
    print("\nThank you for playing Guild Quest!")

def handle_fight(player, quests, unlocked_quests):
    active = [q for q in player.active_quests if not q.completed and q.goal > 0]
    if not active:
        print("You have no active combat quests. Check the questboard!")
        return
    
    current_quest = active[0]
    
    # Choose enemy
    if current_quest.title == "Goblin Trouble":
        enemy = Enemy("Goblin", 25, 6, 8, 15)
    elif current_quest.title == "Forest Menace":
        enemy = Enemy("Wolf", 35, 9, 12, 25)
    elif current_quest.title == "Road Bandits":
        enemy = Enemy("Bandit Leader", 55, 13, 25, 45)
    else:  # Dragon - Final Boss
        enemy = Enemy("Ancient Dragon", health=120, attack=18, gold_reward=100, exp_reward=300)
        print("🐉 The ground shakes as the mighty Dragon of Eldergloom appears!")
    
    if fight(player, enemy):
        current_quest.progress += 1
        if current_quest.progress >= current_quest.goal:
            current_quest.completed = True
            player.gold += current_quest.reward_gold
            player.gain_exp(current_quest.reward_exp)
            print(f"\n🎉 QUEST COMPLETED: {current_quest.title}!")
            
            # Unlock next quest
            order = ["goblin", "wolf", "bandit", "dragon"]
            try:
                current_idx = order.index([k for k, v in quests.items() if v == current_quest][0])
                if current_idx + 1 < len(order):
                    next_key = order[current_idx + 1]
                    if next_key not in unlocked_quests:
                        unlocked_quests.append(next_key)
                        print(f"🌟 New quest unlocked: {quests[next_key].title}!")
            except:
                pass

if __name__ == "__main__":
    main()
