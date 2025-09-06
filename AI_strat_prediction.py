# predict_realtime.py
import pandas as panda
import joblib

from reccomend_main import recommend_strategy 

# --- Load the trained model ---
decision_tree_model = joblib.load("strategy_log.pkl")

def predict_strategy(game_scenario):
    # Convert true or false to 0 and 1 same as before and load the dictionary
    features_df = panda.DataFrame([game_scenario])
    features_df = features_df.astype(int)

    strat = decision_tree_model.predict(features_df)
    
    return strat


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

predicted_strategy = predict_strategy(example)
print("Predicted strategy: ", predicted_strategy)
