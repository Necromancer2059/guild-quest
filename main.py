from player import Player

def main():
    print("=" * 50)
    print("🏰 WELCOME TO GUILD QUEST 🏰")
    print("=" * 50)
    print("You have just joined the famous 'Silver Blade Guild'.\n")
    
    player_name = input("What is your adventurer's name? > ").strip()
    if not player_name:
        player_name = "Hero"
    
    player = Player(player_name)
    
    print(f"\nWelcome to the guild, {player.name}!")
    print("Your adventure begins now...\n")
    
    while True:
        cmd = input("\n> ").strip().lower()
        
        if cmd in ["quit", "exit"]:
            print(f"Thanks for playing, {player.name}! See you next time.")
            break
            
        elif cmd == "help":
            print("\nAvailable commands:")
            print("  help  - Show this help")
            print("  stats - Show your character stats")
            print("  quit  - Exit the game")
            
        elif cmd == "stats":
            player.show_stats()
            
        else:
            print("Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    main()
