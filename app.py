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
def get_snack_option(mood: str, energy: str) -> Dict[str, str]:
    """
    Return the first available snack based on mood and energy.
    """
    options = snack_map.get((mood.capitalize(), energy.capitalize()), ["Granola Bar"])
    return {"snack": options[0]}

@app.task
def choose_snack(mood: str, energy: str, mode: str = "Surprise Me", manual_choice: Optional[str] = None) -> Dict[str, str]:
    """
    Return a chosen snack either randomly or manually if valid.
    """
    options = snack_map.get((mood.capitalize(), energy.capitalize()), ["Granola Bar"])
    if mode == "Surprise Me":
        return {"snack": random.choice(options)}
    if manual_choice in options:
        return {"snack": manual_choice}
    return {"snack": "Granola Bar"}

@app.task
def log_snack(mood: str, energy: str, snack: str) -> Dict[str, str]:
    """
    Log a snack with timestamp and return the entry.
    """
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

