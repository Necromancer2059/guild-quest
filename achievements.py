class Achievement:
    def __init__(self, name: str, description: str, icon: str = "🏆"):
        self.name = name
        self.description = description
        self.icon = icon
        self.unlocked = False

class AchievementSystem:
    def __init__(self):
        self.achievements = [
            Achievement("First Steps", "Complete your first quest", "🌱"),
            Achievement("Goblin Slayer", "Defeat 10 goblins", "🟢"),
            Achievement("Wolf Hunter", "Defeat 5 wolves", "🐺"),
            Achievement("Merchant", "Spend 200 gold in the shop", "💰"),
            Achievement("Well Rested", "Rest at the guild 5 times", "🪵"),
            Achievement("Dragon Slayer", "Defeat the Dragon of Eldergloom", "🐉"),
            Achievement("Level 5", "Reach level 5", "⭐"),
            Achievement("Guild Legend", "Complete all quests", "👑")
        ]
        self.stats = {
            "goblins_killed": 0,
            "wolves_killed": 0,
            "gold_spent": 0,
            "rests": 0
        }

    def check_achievements(self, player, current_quest=None):
        unlocked_any = False
        
        for ach in self.achievements:
            if ach.unlocked:
                continue
                
            if ach.name == "First Steps" and current_quest and current_quest.completed:
                ach.unlocked = True
                unlocked_any = True
            elif ach.name == "Goblin Slayer" and self.stats["goblins_killed"] >= 10:
                ach.unlocked = True
                unlocked_any = True
            elif ach.name == "Wolf Hunter" and self.stats["wolves_killed"] >= 5:
                ach.unlocked = True
                unlocked_any = True
            elif ach.name == "Merchant" and self.stats["gold_spent"] >= 200:
                ach.unlocked = True
                unlocked_any = True
            elif ach.name == "Well Rested" and self.stats["rests"] >= 5:
                ach.unlocked = True
                unlocked_any = True
            elif ach.name == "Level 5" and player.level >= 5:
                ach.unlocked = True
                unlocked_any = True
            elif ach.name == "Dragon Slayer" and current_quest and current_quest.title == "Dragon of Eldergloom" and current_quest.completed:
                ach.unlocked = True
                unlocked_any = True
            elif ach.name == "Guild Legend" and all(q.completed for q in player.active_quests if hasattr(q, 'completed')):
                # Simplified check - you can improve this
                ach.unlocked = True
                unlocked_any = True

        if unlocked_any:
            print("🎉 New Achievement(s) Unlocked!")

    def show_achievements(self):
        print("\n" + "🏆 ACHIEVEMENTS".center(60))
        print("="*60)
        for ach in self.achievements:
            status = "✅" if ach.unlocked else "⬜"
            print(f"{status} {ach.icon} {ach.name}")
            print(f"   {ach.description}")
        print("="*60)
