class Quest:
    def __init__(self, title: str, description: str, reward_gold: int, reward_exp: int, goal: int = 0):
        self.title = title
        self.description = description
        self.reward_gold = reward_gold
        self.reward_exp = reward_exp
        self.goal = goal
        self.progress = 0
        self.completed = False

    def show_details(self):
        status = "✅ Completed" if self.completed else f"⏳ In Progress ({self.progress}/{self.goal})"
        print(f"\n📜 {self.title}")
        print(f"   {self.description}")
        print(f"   Progress: {self.progress}/{self.goal if self.goal > 0 else '—'}")
        print(f"   Reward: {self.reward_gold} gold + {self.reward_exp} EXP")
        print(f"   Status: {status}")
