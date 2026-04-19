from player import Player

def main():
    print("=" * 60)
    print("🏰 WELCOME TO THE SILVER BLADE GUILD 🏰")
    print("=" * 60)
    print("A simple text-based guild adventure.\n")
    
    player_name = input("Enter your adventurer's name: > ").strip()
    if not player_name:
        player_name = "Hero"
    
    player = Player(player_name)
    
    # Game state
    current_location = "guild_hall"
    
    print(f"\n🎉 Welcome to the guild, {player.name}!")
    print("You are now an official member of the Silver Blade Guild.\n")
    show_guild_hall()
    
    while True:
        cmd = input("\n> ").strip().lower()
        
        if cmd in ["quit", "exit"]:
            print(f"\nFarewell, {player.name}. May your blade stay sharp!")
            break
            
        elif cmd == "help":
            print("\n📜 Available commands:")
            print("  help     - Show this help")
            print("  stats    - Show your character stats")
            print("  hall     - Return to the Guild Hall")
            print("  quest    - View available quests")
            print("  shop     - Visit the guild shop")
            print("  quit     - Exit the game")
            
        elif cmd == "stats":
            player.show_stats()
            
        elif cmd in ["hall", "guild", "guild_hall"]:
            current_location = "guild_hall"
            show_guild_hall()
            
        elif cmd == "quest":
            print("\n🗡️  Quest Board (coming in next commits...)")
            print("No quests available yet. Check back soon!")
            
        elif cmd == "shop":
            print("\n🛒 Guild Shop (coming soon...)")
            print("Weapons, potions, and gear will be available here.")
            
        else:
            print("❌ Unknown command. Type 'help' to see available commands.")

def show_guild_hall():
    print("\n" + "="*50)
    print("🏛️  GUILD HALL")
    print("="*50)
    print("You stand in the bustling main hall of the Silver Blade Guild.")
    print(" seasoned adventurers are talking, sharpening weapons, and")
    print(" accepting new quests from the large board on the wall.")
    print("\nWhat would you like to do?")
    print("  • Type 'quest' to check the Quest Board")
    print("  • Type 'shop' to visit the Guild Shop")
    print("  • Type 'stats' to check your status")
    print("  • Type 'hall' to return here anytime")

if __name__ == "__main__":
    main()
