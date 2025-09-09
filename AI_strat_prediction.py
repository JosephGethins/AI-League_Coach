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
    
    validation_check = rules_strategy == ai_strategy

    # Create log row
    log_row = {
        **game_scenario,
        "rules_strategy": rules_strategy,
        "ai_strategy": ai_strategy,
        "Was_Ai_Correct?": validation_check,
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
    "gold": 1800,
    "health": 45,
    "mana": 30,
    "enemy_nearby": True,
    "enemy_TeamWipe": False,
    "dragon_alive": False,
    "baron_alive": False,
    "game_time": 10,
    "gold_lead": -2000,
    "turrets_down": 1,
    "allies_alive": 3,
    "enemies_dead": 1,
    "jungle_camps_up": 3,
    "tower_pressure": 2,
    "ultimate_ready": False
}

AI_v_rules(example)
