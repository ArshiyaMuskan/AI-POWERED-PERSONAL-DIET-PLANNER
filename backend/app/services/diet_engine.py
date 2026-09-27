"""
Deterministic recommendation engine.

This intentionally avoids clinical nutrition calculations.
It selects educational meal examples based on the user's demo preferences.
"""

FOODS = {
    "vegetarian": {
        "breakfast": [
            "Oats with milk/yogurt, banana and nuts",
            "Vegetable poha with fruit",
            "Whole-grain toast with paneer and tomato",
        ],
        "lunch": [
            "Brown rice, dal, mixed vegetables and curd",
            "Whole-wheat roti, chana and vegetable salad",
            "Vegetable pulao with raita and cucumber",
        ],
        "snack": [
            "Fruit with a small handful of nuts",
            "Yogurt with fruit",
            "Roasted chickpeas",
        ],
        "dinner": [
            "Roti with mixed vegetable curry and dal",
            "Paneer and vegetable bowl with whole grains",
            "Vegetable khichdi with curd",
        ],
    },
    "vegan": {
        "breakfast": [
            "Oats with soy milk, banana and seeds",
            "Peanut-butter whole-grain toast with fruit",
            "Vegetable upma with fruit",
        ],
        "lunch": [
            "Brown rice, lentils and mixed vegetables",
            "Chickpea salad with whole grains",
            "Rajma with rice and cucumber salad",
        ],
        "snack": [
            "Fruit with nuts",
            "Roasted chickpeas",
            "Carrot/cucumber sticks with hummus",
        ],
        "dinner": [
            "Tofu and vegetable stir-fry with rice",
            "Lentil soup with whole-grain bread",
            "Vegetable quinoa bowl with beans",
        ],
    },
    "general": {
        "breakfast": [
            "Oats with yogurt, fruit and nuts",
            "Egg and vegetable whole-grain sandwich",
            "Idli with sambar and fruit",
        ],
        "lunch": [
            "Rice, dal, vegetables and optional lean protein",
            "Roti with chicken/fish or beans and vegetables",
            "Grain bowl with vegetables and protein",
        ],
        "snack": [
            "Fruit with nuts",
            "Yogurt and fruit",
            "Roasted chickpeas",
        ],
        "dinner": [
            "Roti with vegetables and dal or lean protein",
            "Grilled protein with vegetables and whole grains",
            "Vegetable soup with whole-grain toast and protein",
        ],
    },
}

GOAL_NOTES = {
    "balanced": "Focus on variety, regular meals and a mix of food groups.",
    "weight-management": "Use sensible portions and prioritize vegetables, fiber and protein-rich foods.",
    "fitness": "Include consistent protein sources, whole grains and recovery-friendly meals.",
}


def normalize_preference(value: str | None) -> str:
    value = (value or "general").lower()
    if "vegan" in value:
        return "vegan"
    if "vegetarian" in value:
        return "vegetarian"
    return "general"


def generate_local_plan(profile: dict) -> dict:
    preference = normalize_preference(profile.get("dietary_preference"))
    foods = FOODS[preference]
    goal = (profile.get("goal") or "balanced").lower()
    note = GOAL_NOTES.get(goal, GOAL_NOTES["balanced"])

    # Deterministic selection makes testing and demos reproducible.
    index = (int(profile.get("age") or 25) + int(float(profile.get("weight") or 60))) % 3

    return {
        "breakfast": foods["breakfast"][index],
        "lunch": foods["lunch"][(index + 1) % 3],
        "snack": foods["snack"][index],
        "dinner": foods["dinner"][(index + 2) % 3],
        "nutrition_summary": (
            "General educational summary: aim for variety across vegetables, "
            "fruit, whole grains and appropriate protein sources. " + note
        ),
        "hydration_reminder": (
            "General reminder: drink water regularly and adjust intake for "
            "weather, activity and personal needs."
        ),
    }
