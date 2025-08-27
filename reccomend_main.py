import datetime
import pandas as pd
import os


def recommend_strategy(gold, health, mana, enemy_nearby, enemy_TeamWipe, dragon_alive, baron_alive, 
                       game_time, gold_lead, turrets_down, allies_alive, enemies_dead):

    scores = {
        "Farm": 0,
        "Fight": 0,
        "Buy Items": 0,
        "Take Dragon": 0,
        "Take Baron": 0,
        "Retreat/Base": 0,
        "Push Lanes": 0
    }

    # --- Core survival rules ---
    if health < 25:
        scores["Retreat/Base"] += 12
    elif health < 50 and enemy_nearby:
        scores["Retreat/Base"] += 8

    if mana < 20:
        scores["Retreat/Base"] += 5

    # --- Economy rules ---
    if gold > 3000:
        scores["Buy Items"] += 12
    elif gold > 2000 and not enemy_nearby:
        scores["Buy Items"] += 6

    # -- Fight rules ---
    if enemy_nearby and health > 60 and mana > 40:
        if allies_alive > enemies_dead:  # numbers advantage
            scores["Fight"] += 12
        else:
            scores["Fight"] += 6

    # --- Objective rules ---
    if dragon_alive and (enemy_TeamWipe or enemies_dead >= 2) and health > 30:
        scores["Take Dragon"] += 15

    if baron_alive and (enemy_TeamWipe or enemies_dead >= 3) and health > 70:
        scores["Take Baron"] += 18

    # --- Map pressure rules ---
    if turrets_down >= 3 and game_time > 20 and enemies_dead >= 2:
        scores["Push Lanes"] += 10

    # --- Farm rules ---
    if gold < 1500 and health > 60 and not enemy_nearby:
        scores["Farm"] += 8

    # --- Scaling by time ---
    if game_time < 15:
        scores["Farm"] += 5  # early game = farming
    elif 15 <= game_time <= 30:
        scores["Fight"] += 3  # mid game = fighting
    else:
        scores["Take Baron"] += 5  # late game = baron is critical

    # --- Team gold lead logic ---
    if gold_lead > 3000:
        scores["Fight"] += 5
    elif gold_lead < -3000:
        scores["Farm"] += 6
        scores["Retreat/Base"] += 3

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


def main():
    print("********** Advanced AI Game Strategy Recommender **********")

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

    strategy = recommend_strategy(
        gold, health, mana, enemy_nearby, enemy_TeamWipe, dragon_alive, baron_alive,
        game_time, gold_lead, turrets_down, allies_alive, enemies_dead
    )

    print("\nRecommended Strategy:", strategy)

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
        "enemies_dead": enemies_dead
    }
    log_strategy(inputs, strategy)


if __name__ == "__main__":
    main()
