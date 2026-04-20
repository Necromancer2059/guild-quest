from player import Player
from quest import Quest

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
            print("  help      - Show commands")
            print("  stats     - Show character stats")
            print("  hall      - Go to Guild Hall")
            print("  quests    - View your active quests")
            print("  accept    - Accept the Goblin Trouble quest")
            print("  quit      - Exit game")
            
        elif cmd == "stats":
            player.show_stats()
            
        elif cmd in ["hall", "guild", "guild_hall"]:
            show_guild_hall(player, goblin_quest)
            
        elif cmd == "quests":
            player.show_active_quests()
            
        elif cmd == "accept":
            player.accept_quest(goblin_quest)
            
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
    print("\nCommands: 'accept' to take the quest | 'quests' to check progress")

if __name__ == "__main__":
    main()
