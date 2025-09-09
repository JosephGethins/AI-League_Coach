# predict_realtime.py
import pandas as panda
import joblib
import os
import datetime

from reccomend_main import recommend_strategy 

# --- Load the trained model ---
decision_tree_model = joblib.load("League_strategy_coach.pkl")

def AI_v_rules(game_scenario, filename="Data_logs_and_csv/ai_vs_rules_log.csv"):
    # AI 
    features_df = panda.DataFrame([game_scenario]).astype(int)
    ai_strategy = decision_tree_model.predict(features_df)[0]

    # Rules 
    rules_strategy = recommend_strategy(**game_scenario)

    # Create log row
    log_row = {
        **game_scenario,
        "rules_strategy": rules_strategy,
        "ai_strategy": ai_strategy,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    #  CSV creation
    df = panda.DataFrame([log_row])
    if os.path.exists(filename):
        df.to_csv(filename, mode="a", header=False, index=False)
    else:
        df.to_csv(filename, mode="w", header=True, index=False)

    print(f"Logged scenario. Rules: {rules_strategy}, AI: {ai_strategy}")

example = {
    "gold": 3200,
    "health": 80,
    "mana": 60,
    "enemy_nearby": True,
    "enemy_TeamWipe": False,
    "dragon_alive": True,
    "baron_alive": False,
    "game_time": 22,
    "gold_lead": 1500,
    "turrets_down": 3,
    "allies_alive": 4,
    "enemies_dead": 2,
    "jungle_camps_up": 2,
    "tower_pressure": 3,
    "ultimate_ready": True
}

AI_v_rules(example)
