from typing import List, Dict, Tuple, Optional, Union
import random
from datetime import datetime
from collections import Counter
from davia import Davia

app = Davia()

# Define snack map
snack_map: Dict[Tuple[str, str], List[str]] = {
    ("Tired", "Low"): ["Dark Chocolate", "Chia Pudding", "Energy Bar"],
    ("Tired", "High"): ["Iced Coffee", "Espresso Shot", "Caffeine Gummies"],
    ("Stressed", "Low"): ["Green Tea", "Almonds", "Cucumber Slices"],
    ("Stressed", "High"): ["Spicy Chips", "Popcorn", "Cold Brew"],
    ("Happy", "High"): ["Bubble Tea", "Nachos", "Fruit Punch"],
    ("Happy", "Low"): ["Gummies", "Cupcake", "Chocolate Muffin"],
    ("Focused", "High"): ["Trail Mix", "Greek Yogurt", "Protein Bar"],
    ("Focused", "Low"): ["Banana with Peanut Butter", "Boiled Egg", "Avocado Toast"]
}

# Store history log
log: List[Dict[str, str]] = []

@app.task
def get_snack_options(mood: str, energy: str) -> Dict[str, List[str]]:
    try:
        options = snack_map.get((mood, energy), ["Granola Bar"])
        return {"options": options}
    except Exception as e:
        return {"error": str(e)}

@app.task
def choose_snack(
    mood: str,
    energy: str,
    mode: str = "Surprise Me",
    manual_choice: Optional[str] = None
) -> Dict[str, str]:
    try:
        options = snack_map.get((mood, energy), ["Granola Bar"])
        if mode == "Surprise Me":
            return {"snack": random.choice(options)}
        elif manual_choice in options:
            return {"snack": manual_choice}
        else:
            return {"snack": "Granola Bar"}
    except Exception as e:
        return {"error": str(e)}

@app.task
def log_snack(mood: str, energy: str, snack: str) -> Dict[str, Union[str, Dict]]:
    try:
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mood": mood,
            "energy": energy,
            "snack": snack
        }
        log.append(entry)
        return {"log": entry}
    except Exception as e:
        return {"error": str(e)}

@app.task
def get_snack_stats() -> Dict[str, int]:
    try:
        counts = Counter(entry["snack"] for entry in log)
        return dict(counts)
    except Exception as e:
        return {"error": str(e)}

# You can optionally keep this for CLI test
if __name__ == "__main__":
    mood = "Tired"
    energy = "Low"
    mode = "Surprise Me"
    manual_choice = None

    result = choose_snack(mood, energy, mode, manual_choice)
    print(f"Suggested Snack: {result}")

    log_snack(mood, energy, result["snack"])
    print("Snack Log:")
    for entry in log:
        print(entry)

    stats = get_snack_stats()
    print("\nSnack Popularity:")
    for snack, count in stats.items():
        print(f"{snack}: {count}")
