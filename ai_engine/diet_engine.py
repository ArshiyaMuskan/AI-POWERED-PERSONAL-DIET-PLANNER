from backend.app.services.diet_engine import generate_local_plan

if __name__ == "__main__":
    demo = {
        "age": 22,
        "weight": 65,
        "dietary_preference": "vegetarian",
        "goal": "balanced",
        "activity_level": "moderate",
    }
    print(generate_local_plan(demo))
