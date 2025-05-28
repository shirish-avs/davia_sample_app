from typing import List, Dict, Tuple, Optional
import random
from datetime import datetime
from collections import Counter
from davia import Davia

app = Davia()

# Snack map
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

# Snack log
log: List[Dict[str, str]] = []

@app.task
def get_snack_option(mood: str, energy: str) -> str:
    mood = mood.capitalize()
    energy = energy.capitalize()
    options = snack_map.get((mood, energy), ["Granola Bar"])
    return options[0]

@app.task
def choose_snack(mood: str, energy: str, mode: str = "Surprise Me", manual_choice: Optional[str] = None) -> str:
    mood = mood.capitalize()
    energy = energy.capitalize()
    options = snack_map.get((mood, energy), ["Granola Bar"])
    if mode == "Surprise Me":
        return random.choice(options)
    if manual_choice in options:
        return manual_choice
    return "Granola Bar"

@app.task
def log_snack(mood: str, energy: str, snack: str) -> Dict[str, str]:
    mood = mood.capitalize()
    energy = energy.capitalize()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood": mood,
        "energy": energy,
        "snack": snack
    }
    log.append(entry)
    return entry


@app.task
def get_snack_stats() -> Dict[str, int]:
    """
    Return count of each snack chosen so far.
    """
    return dict(Counter(entry["snack"] for entry in log))

# Optional CLI test
if __name__ == "__main__":
    mood = "Happy"
    energy = "Low"

    print("First snack option:")
    print(get_snack_option(mood, energy))

    print("Surprise snack:")
    chosen = choose_snack(mood, energy)
    print(chosen)

    print("Logging snack...")
    print(log_snack(mood, energy, chosen))

    print("Snack stats:")
    print(get_snack_stats())
