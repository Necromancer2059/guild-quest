from player import Player
from quest import Quest
from enemy import Enemy, fight

def main():
    print("=" * 60)
    print("🏰 WELCOME TO THE SILVER BLADE GUILD 🏰")
    print("=" * 60)
    
    player_name = input("Enter your adventurer's name: > ").strip()
    if not player_name:
        player_name = "Hero"
    
    player = Player(player_name)
    
    # First quest
    goblin_quest = Quest(
        title="Goblin Trouble",
        description="The nearby village is being harassed by goblins. Defeat 3 goblins.",
        reward_gold=30,
        reward_exp=60
    )
    goblin_quest.goal = 3
    
    print(f"\n🎉 Welcome to the guild, {player.name}!\n")
    
    while True:
        cmd = input("\n> ").strip().lower()
        
        if cmd in ["quit", "exit"]:
            print(f"\nFarewell, {player.name}. Safe travels!")
            break
            
        elif cmd == "help":
            print("\n📜 Commands:")
            print("  help      - Show this help")
            print("  stats     - Show character stats")
            print("  hall      - Go to Guild Hall")
            print("  quests    - View your active quests")
            print("  accept    - Accept the Goblin Trouble quest")
            print("  fight     - Fight a goblin (only if you have the quest)")
            print("  quit      - Exit game")
            
        elif cmd == "stats":
            player.show_stats()
            
        elif cmd in ["hall", "guild", "guild_hall"]:
            show_guild_hall(player, goblin_quest)
            
        elif cmd == "quests":
            player.show_active_quests()
            
        elif cmd == "accept":
            player.accept_quest(goblin_quest)
            
        elif cmd == "fight":
            if goblin_quest in player.active_quests and not goblin_quest.completed:
                goblin = Enemy(name="Goblin", health=25, attack=6, gold_reward=8, exp_reward=15)
                if fight(player, goblin):
                    # Update quest progress
                    goblin_quest.progress += 1
                    print(f"Quest progress: {goblin_quest.progress}/{goblin_quest.goal}")
                    
                    if goblin_quest.progress >= goblin_quest.goal:
                        goblin_quest.completed = True
                        player.gold += goblin_quest.reward_gold
                        player.gain_exp(goblin_quest.reward_exp)
                        print(f"\n🎉 QUEST COMPLETED: {goblin_quest.title}!")
                        print(f"You received {goblin_quest.reward_gold} gold and {goblin_quest.reward_exp} EXP!")
            else:
                print("You don't have an active quest that requires fighting right now.")
                print("Go to the hall and 'accept' the Goblin Trouble quest first.")
            
        else:
            print("❌ Unknown command. Type 'help' for options.")

def show_guild_hall(player, goblin_quest):
    print("\n" + "="*55)
    print("🏛️  GUILD HALL - Quest Board")
    print("="*55)
    print("A large wooden board displays available quests.")
    print("\nCurrent Quest Available:")
    print(f"   • {goblin_quest.title}")
    print(f"     {goblin_quest.description}")
    print(f"     Reward: {goblin_quest.reward_gold} gold + {goblin_quest.reward_exp} EXP")
    print("\nTip: After accepting, type 'fight' to battle goblins!")

if __name__ == "__main__":
    main()
