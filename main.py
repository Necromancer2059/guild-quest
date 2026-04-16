
**main.py**
```python
def main():
    print("=" * 50)
    print("🏰 WELCOME TO GUILD QUEST 🏰")
    print("=" * 50)
    print("You have just joined the famous 'Silver Blade Guild'.")
    print("Type 'help' at any time to see commands.\n")
    
    player_name = input("What is your adventurer's name? > ").strip()
    if not player_name:
        player_name = "Hero"
    
    print(f"\nWelcome, {player_name}! Your guild journey begins now...")
    print("\n(For now the game is just a skeleton. More features coming in next commits!)")

    while True:
        cmd = input("\n> ").strip().lower()
        if cmd in ["quit", "exit"]:
            print("Thanks for playing Guild Quest! See you next time.")
            break
        elif cmd == "help":
            print("Available commands: help, quit, stats (coming soon)")
        else:
            print("Unknown command. Type 'help' for options.")

if __name__ == "__main__":
    main()
