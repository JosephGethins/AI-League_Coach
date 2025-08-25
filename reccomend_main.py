import datetime

def recommend_strategy(gold, health, mana, enemy_nearby, enemy_TeamWipe, dragon_alive, baron_alive):

    scores = {
        "Farm": 0,
        "Fight": 0,
        "Buy Items": 0,
        "Take Dragon": 0,
        "Take Baron": 0,
        "Retreat/Base": 0
    }


    if health < 30:
        scores["Retreat/Base"] += 10
    if mana < 20:
        scores["Retreat/Base"] += 7
    if gold > 2500:
        scores["Buy Items"] += 8
    if enemy_nearby and health > 60 and mana > 40:
        scores["Fight"] += 10
    if dragon_alive and enemy_TeamWipe and health > 70 and not baron_alive:
        scores["Take Dragon"] += 12
    if baron_alive and enemy_TeamWipe and health > 70:
        scores["Take Baron"] += 15

    best_strategy = max(scores, key=scores.get)
    return best_strategy


def log_strategy(inputs, strategy):
    with open("strategy_log.txt", "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{timestamp}] Inputs: {inputs} | Strategy: {strategy}\n")


def main():
    print("********** AI Game Strategy Recommender (Weighted AI Version) **********")

 
    gold = int(input("Enter your gold amount: "))
    health = int(input("Enter your health % (0-100): "))
    mana = int(input("Enter your mana % (0-100): "))
    enemy_nearby = input("Is an enemy nearby? (yes/no): ").lower() == "yes"
    enemy_TeamWipe = input("Has there been an ace for your team (yes/no): ").lower() == "yes"
    dragon_alive = input("Is dragon alive? (yes/no): ").lower() == "yes"
    baron_alive = input("Is baron alive? (yes/no): ").lower() == "yes"

  
    strategy = recommend_strategy(gold, health, mana, enemy_nearby, enemy_TeamWipe, dragon_alive, baron_alive)

    
    print("\nRecommended Strategy:", strategy)

   
    inputs = {
        "gold": gold,
        "health": health,
        "mana": mana,
        "enemy_nearby": enemy_nearby,
        "enemy_TeamWipe": enemy_TeamWipe,
        "dragon_alive": dragon_alive,
        "baron_alive": baron_alive
    }
    log_strategy(inputs, strategy)


if __name__ == "__main__":
    main()
