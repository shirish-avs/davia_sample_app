from typing import List, Dict, Tuple, Optional
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
def get_snack_options(mood: str, energy: str) -> List[str]:
    return snack_map.get((mood, energy), ["Granola Bar"])

@app.task
def choose_snack(
    mood: str,
    energy: str,
    mode: str = "Surprise Me",
    manual_choice: Optional[str] = None
) -> str:
    options = get_snack_options(mood, energy)
    if mode == "Surprise Me":
        return random.choice(options)
    elif manual_choice in options:
        return manual_choice
    else:
        return "Granola Bar"

@app.task
def log_snack(mood: str, energy: str, snack: str) -> Dict[str, str]:
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood": mood,
        "energy": energy,
        "snack": snack
    }
    log.append(entry)
    return entry

def show_log() -> None:
    for entry in log:
        print(entry)

@app.task
def get_snack_stats() -> Counter:
    snack_counts = Counter(entry['snack'] for entry in log)
    return snack_counts

# Example usage
if __name__ == "__main__":
    mood = "Tired"
    energy = "Low"
    mode = "Surprise Me"  
    manual_choice = None  

    snack = choose_snack(mood, energy, mode, manual_choice)
    print(f"Suggested Snack: {snack}")

    log_snack(mood, energy, snack)
    show_log()

    stats = get_snack_stats()
    print("\nSnack Popularity:")
    for snack, count in stats.items():
        print(f"{snack}: {count}")
