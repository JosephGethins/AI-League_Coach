import datetime
import pandas as pd
import os
import random

def recommend_strategy(gold, health, mana, 
                       enemy_nearby, enemy_TeamWipe, 
                       dragon_alive, baron_alive,
                       game_time, gold_lead, turrets_down, 
                       allies_alive, enemies_dead,
                       jungle_camps_up, tower_pressure, ultimate_ready):

    scores = {
        "Farm": 0,
        "Fight": 0,
        "Buy Items": 0,
        "Take Dragon": 0,
        "Take Baron": 0,
        "Retreat/Base": 0,
        "Push Lanes": 0,
        "Invade Jungle": 0
    }

    # --- Core survival rules ---
    if health < 25:
        scores["Retreat/Base"] += 12 + random.randint(-2,2)
    elif health < 50 and enemy_nearby:
        scores["Retreat/Base"] += 8 + random.randint(-2,2)

    if mana < 20:
        scores["Retreat/Base"] += 5 + random.randint(-1,1)

    # --- Economy rules ---
    if gold > 3000:
        scores["Buy Items"] += 12 + random.randint(-2,2)
    elif gold > 2000 and not enemy_nearby:
        scores["Buy Items"] += 6 + random.randint(-1,1)

    # --- Fight rules ---
    if enemy_nearby and health > 60 and mana > 40:
        fight_score = 12 if allies_alive > enemies_dead else 6
        scores["Fight"] += fight_score + random.randint(-2,2)
        if ultimate_ready:
            scores["Fight"] += 3  # bonus for ultimate availability

    # --- Objective rules ---
    if dragon_alive and (enemy_TeamWipe or enemies_dead >= 3) and health > 60:
        scores["Take Dragon"] += 15 + random.randint(-3,3)

    if baron_alive and (enemy_TeamWipe or enemies_dead >= 4) and health > 70:
        scores["Take Baron"] += 18 + random.randint(-3,3)

    # --- Map pressure rules ---
    if turrets_down >= 3 and game_time > 20 and enemies_dead >= 2:
        scores["Push Lanes"] += 10 + random.randint(-2,2)

    # --- Farm rules ---
    if gold < 1500 and health > 60 and not enemy_nearby:
        scores["Farm"] += 8 + random.randint(-2,2)

    if game_time < 15:
        scores["Farm"] += 5 + random.randint(-1,1)

    # --- Team gold lead logic ---
    if gold_lead > 3000:
        scores["Fight"] += 5 + random.randint(-1,1)
    elif gold_lead < -3000:
        scores["Farm"] += 6 + random.randint(-1,1)
        scores["Retreat/Base"] += 3 + random.randint(-1,1)

    # --- Jungle / tower pressure rules ---
    if jungle_camps_up >= 2 and not enemy_nearby:
        scores["Invade Jungle"] += 8 + random.randint(-2,2)
    if tower_pressure > 0 and health > 50:
        scores["Push Lanes"] += tower_pressure + random.randint(-1,1)

    best_strategy = max(scores, key=scores.get)
    return best_strategy


def log_strategy(inputs, strategy, filename="strategy_log.csv"):
    row = {
        **inputs,
        "strategy": strategy,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    df = pd.DataFrame([row])

    if os.path.exists(filename):
        df.to_csv(filename, mode="a", header=False, index=False)
    else:
        df.to_csv(filename, mode="w", header=True, index=False)


def generate_random_scenarios(n=100000, filename="strategy_log.csv"):
    for _ in range(n):
        inputs = {
            "gold": random.randint(0, 6000),
            "health": random.randint(0, 100),
            "mana": random.randint(0, 100),
            "enemy_nearby": random.choice([True, False]),
            "enemy_TeamWipe": random.choice([True, False]),
            "dragon_alive": random.choice([True, False]),
            "baron_alive": random.choice([True, False]),
            "game_time": random.randint(0, 40),
            "gold_lead": random.randint(-8000, 8000),
            "turrets_down": random.randint(0, 11),
            "allies_alive": random.randint(0, 5),
            "enemies_dead": random.randint(0, 5),
            "jungle_camps_up": random.randint(0, 5),
            "tower_pressure": random.randint(0, 5),
            "ultimate_ready": random.choice([True, False])
        }

        strategy = recommend_strategy(**inputs)
        log_strategy(inputs, strategy, filename)

    print(f"✅ Generated {n} enhanced random scenarios into {filename}")
    
def manual_input_mode():
    print("********** Manual Input Mode **********")

    gold = int(input("Enter your gold amount: "))
    health = int(input("Enter your health % (0-100): "))
    mana = int(input("Enter your mana % (0-100): "))
    enemy_nearby = input("Is an enemy nearby? (yes/no): ").lower() == "yes"
    enemy_TeamWipe = input("Has there been an ace for your team? (yes/no): ").lower() == "yes"
    dragon_alive = input("Is dragon alive? (yes/no): ").lower() == "yes"
    baron_alive = input("Is baron alive? (yes/no): ").lower() == "yes"
    game_time = int(input("Enter game time in minutes: "))
    gold_lead = int(input("Enter team gold lead (positive if ahead, negative if behind): "))
    turrets_down = int(input("How many enemy turrets are destroyed? "))
    allies_alive = int(input("How many allies are alive? "))
    enemies_dead = int(input("How many enemies are currently dead? "))
    jungle_camps_up = int(input("How many jungle camps are up? "))
    tower_pressure = int(input("How much tower pressure? (0-5) "))
    ultimate_ready = input("Is your ultimate ready? (yes/no): ").lower() == "yes"

    inputs = {
        "gold": gold,
        "health": health,
        "mana": mana,
        "enemy_nearby": enemy_nearby,
        "enemy_TeamWipe": enemy_TeamWipe,
        "dragon_alive": dragon_alive,
        "baron_alive": baron_alive,
        "game_time": game_time,
        "gold_lead": gold_lead,
        "turrets_down": turrets_down,
        "allies_alive": allies_alive,
        "enemies_dead": enemies_dead,
        "jungle_camps_up": jungle_camps_up,
        "tower_pressure": tower_pressure,
        "ultimate_ready": ultimate_ready
    }

    strategy = recommend_strategy(**inputs)
    print("\nRecommended Strategy:", strategy)
    log_strategy(inputs, strategy)

def main():
    print("********** Enhanced AI Game Strategy Recommender **********")
    mode = input("Choose mode: (1) Manual Input  (2) Generate Random Dataset: ")

    if mode == "2":
        n = int(input("How many random scenarios would you like to generate: "))
        generate_random_scenarios(n)
    else:
        manual_input_mode()


if __name__ == "__main__":
    main()
