class Quest:
    def __init__(self, title: str, description: str, reward_gold: int, reward_exp: int):
        self.title = title
        self.description = description
        self.reward_gold = reward_gold
        self.reward_exp = reward_exp
        self.completed = False
        self.progress = 0
        self.goal = 0  # e.g. kill 3 goblins

    def show_details(self):
        status = "✅ Completed" if self.completed else "⏳ In Progress"
        print(f"\n📜 Quest: {self.title}")
        print(f"   {self.description}")
        print(f"   Progress: {self.progress}/{self.goal}")
        print(f"   Reward: {self.reward_gold} gold + {self.reward_exp} EXP")
        print(f"   Status: {status}")
