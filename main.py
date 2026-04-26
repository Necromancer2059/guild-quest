from player import Player
from quest import Quest
from enemy import Enemy, fight
from shop import Shop

def main():
    print("=" * 60)
    print("🏰 WELCOME TO THE SILVER BLADE GUILD 🏰")
    print("=" * 60)
    
    player_name = input("Enter your adventurer's name: > ").strip()
    if not player_name:
        player_name = "Hero"
    
    player = Player(player_name)
    shop = Shop()
    
    # Define all quests
    quests = {
        "goblin": Quest(
            title="Goblin Trouble",
            description="The nearby village is being harassed by goblins. Defeat 3 goblins.",
            reward_gold=30,
            reward_exp=60,
            goal=3
        ),
        "wolf": Quest(
            title="Forest Menace",
            description="Wolves have been attacking travelers on the forest road. Defeat 2 wolves.",
            reward_gold=45,
            reward_exp=90,
            goal=2
        ),
        "bandit": Quest(
            title="Road Bandits",
            description="A group of bandits is ambushing merchants. Defeat 1 bandit leader.",
            reward_gold=70,
            reward_exp=150,
            goal=1
        )
    }
    
    # Track which quests are unlocked
    unlocked_quests = ["goblin"]
    completed_count = 0
    
    print(f"\n🎉 Welcome to the guild, {player.name}!\n")
    show_guild_hall(player, quests, unlocked_quests)
    
    while True:
        cmd = input("\n> ").strip().lower()
        
        if cmd in ["quit", "exit"]:
            print(f"\nFarewell, {player.name}. Safe travels!")
            break
            
        elif cmd == "help":
            print("\n📜 Commands:")
            print("  help          - Show this help")
            print("  stats         - Show character stats")
            print("  hall          - Return to Guild Hall")
            print("  questboard    - Show available quests")
            print("  accept <name> - Accept a quest (e.g. accept goblin)")
            print("  quests        - View your active quests")
            print("  fight         - Fight current enemy (if you have a combat quest)")
            print("  shop          - Visit the Guild Shop")
            print("  use <item>    - Use an item (e.g. use potion)")
            print("  quit          - Exit game")
            
        elif cmd == "stats":
            player.show_stats()
            
        elif cmd in ["hall", "guild", "guild_hall"]:
            show_guild_hall(player, quests, unlocked_quests)
            
        elif cmd == "questboard":
            show_quest_board(quests, unlocked_quests)
            
        elif cmd.startswith("accept "):
            quest_key = cmd[7:].strip()
            if quest_key in unlocked_quests and quest_key in quests:
                player.accept_quest(quests[quest_key])
                print(f"✅ You accepted: {quests[quest_key].title}")
            else:
                print("That quest is not available or already accepted.")
                
        elif cmd == "quests":
            player.show_active_quests()
            
        elif cmd == "fight":
            handle_fight(player, quests, unlocked_quests)
            
        elif cmd == "shop":
            shop.show_items()
            
        elif cmd.startswith("buy "):
            try:
                item_index = int(cmd.split()[1])
                bought_item = shop.buy_item(player, item_index)
                if bought_item:
                    player.add_to_inventory(bought_item)
            except (IndexError, ValueError):
                print("Usage: buy <number>  (e.g. buy 1)")
                
        elif cmd.startswith("use "):
            item_name = cmd[4:].strip()
            player.use_item(item_name)
            
        else:
            print("❌ Unknown command. Type 'help' for options.")

def show_guild_hall(player, quests, unlocked_quests):
    print("\n" + "="*60)
    print("🏛️  GUILD HALL")
    print("="*60)
    print("You stand in the lively main hall of the Silver Blade Guild.")
    print("Adventurers are sharing stories and checking the quest board.\n")
    print("Available actions:")
    print("  • questboard   - See all available quests")
    print("  • accept <name>- Accept a quest (goblin, wolf, bandit)")
    print("  • fight        - Engage in combat for active quests")
    print("  • shop         - Buy potions and supplies")
    print("  • stats / quests - Check your progress")

def show_quest_board(quests, unlocked_quests):
    print("\n" + "="*50)
    print("📋 QUEST BOARD")
    print("="*50)
    for key in unlocked_quests:
        q = quests[key]
        status = "✅ Completed" if q.completed else "⏳ Available"
        print(f"• {q.title} ({key})")
        print(f"  {q.description}")
        print(f"  Reward: {q.reward_gold} gold + {q.reward_exp} EXP | Status: {status}\n")

def handle_fight(player, quests, unlocked_quests):
    active_combat_quests = [q for q in player.active_quests if not q.completed and q.goal > 0]
    
    if not active_combat_quests:
        print("You have no active combat quests right now.")
        print("Accept a quest from the quest board first.")
        return
    
    # For simplicity, we pick the first active combat quest
    current_quest = active_combat_quests[0]
    
    if current_quest.title == "Goblin Trouble":
        enemy = Enemy("Goblin", health=25, attack=6, gold_reward=8, exp_reward=15)
    elif current_quest.title == "Forest Menace":
        enemy = Enemy("Wolf", health=35, attack=9, gold_reward=12, exp_reward=25)
    else:
        enemy = Enemy("Bandit", health=50, attack=12, gold_reward=20, exp_reward=40)
    
    if fight(player, enemy):
        current_quest.progress += 1
        print(f"Quest progress: {current_quest.progress}/{current_quest.goal}")
        
        if current_quest.progress >= current_quest.goal:
            current_quest.completed = True
            player.gold += current_quest.reward_gold
            player.gain_exp(current_quest.reward_exp)
            print(f"\n🎉 QUEST COMPLETED: {current_quest.title}!")
            print(f"Reward received: {current_quest.reward_gold} gold + {current_quest.reward_exp} EXP")
            
            # Unlock next quest
            if current_quest.title == "Goblin Trouble" and "wolf" not in unlocked_quests:
                unlocked_quests.append("wolf")
                print("🌲 New quest unlocked: Forest Menace!")
            elif current_quest.title == "Forest Menace" and "bandit" not in unlocked_quests:
                unlocked_quests.append("bandit")
                print("🏴‍☠️ New quest unlocked: Road Bandits!")

if __name__ == "__main__":
    main()
