import pandas as panda
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report

dataset = panda.read_csv("strategy_log.csv")

# Similar to SQL syntax it seems
data = dataset.drop(columns=["strategy", "timestamp"])
labels = dataset["strategy"]

# sk will only work with int it looks like so true/false convert to 1/0, like cosine similarity
data = data.astype(int)
