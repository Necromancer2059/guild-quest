import random

class Skill:
    def __init__(self, name: str, description: str, cost: int, damage_mult: float = 1.0, heal: int = 0):
        self.name = name
        self.description = description
        self.cost = cost
        self.damage_mult = damage_mult
        self.heal = heal
        self.unlocked = False
        self.level = 1

class SkillSystem:
    def __init__(self):
        self.mana = 30
        self.max_mana = 30
        self.skills = {
            "power": Skill("Power Strike", "Heavy attack that deals more damage", cost=8, damage_mult=1.8),
            "heal": Skill("Healing Light", "Restore health using mana", cost=10, heal=35),
            "iron": Skill("Iron Skin", "Reduce incoming damage for one turn", cost=6),
            "swift": Skill("Swift Attack", "Fast attack with high crit chance", cost=12, damage_mult=1.4)
        }

    def unlock_skills(self, player_level: int):
        if player_level >= 2 and not self.skills["power"].unlocked:
            self.skills["power"].unlocked = True
            print("🔥 New Skill Unlocked: Power Strike!")
        if player_level >= 4 and not self.skills["heal"].unlocked:
            self.skills["heal"].unlocked = True
            print("✨ New Skill Unlocked: Healing Light!")
        if player_level >= 6 and not self.skills["iron"].unlocked:
            self.skills["iron"].unlocked = True
            print("🛡️ New Skill Unlocked: Iron Skin!")
        if player_level >= 8 and not self.skills["swift"].unlocked:
            self.skills["swift"].unlocked = True
            print("⚡ New Skill Unlocked: Swift Attack!")

    def show_skills(self):
        print("\n🔮 YOUR SKILLS")
        print("="*50)
        print(f"Mana: {self.mana}/{self.max_mana}\n")
        for key, skill in self.skills.items():
            status = "✅ Unlocked" if skill.unlocked else "🔒 Locked"
            print(f"• {skill.name} ({key}) - {status}")
            print(f"   {skill.description} (Cost: {skill.cost} mana)")
