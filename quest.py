class Quest:
    def __init__(self, title: str, description: str, reward_gold: int, reward_exp: int, goal: int = 0, is_boss: bool = False):
        self.title = title
        self.description = description
        self.reward_gold = reward_gold
        self.reward_exp = reward_exp
        self.goal = goal
        self.progress = 0
        self.completed = False
        self.is_boss = is_boss

    def show_details(self):
        status = "✅ Completed" if self.completed else f"⏳ In Progress ({self.progress}/{self.goal})"
        boss_tag = " 🔥 BOSS" if self.is_boss else ""
        print(f"\n📜 {self.title}{boss_tag}")
        print(f"   {self.description}")
        print(f"   Progress: {self.progress}/{self.goal if self.goal > 0 else '—'}")
        print(f"   Reward: {self.reward_gold} gold + {self.reward_exp} EXP")
        print(f"   Status: {status}")
