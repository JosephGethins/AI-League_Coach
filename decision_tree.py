import pandas as panda
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

dataset = panda.read_csv("strategy_log.csv")

# Similar to SQL syntax it seems
data = dataset.drop(columns=["strategy", "timestamp"])
labels = dataset["strategy"]

# sk will only work with int it looks like so true/false convert to 1/0, like cosine similarity
data = data.astype(int)

# Reminds me of data science class with the test size splits with training and temporary, though that was random forests
X_train, X_temp, y_train, y_temp = train_test_split (
    data, labels, test_size = 0.30, random_state = 21, stratify = labels
)
# Splittng the 30 percent into 15 and 15 for tuning, super similar to what we done in R studio in college
X_validation, X_test, y_validation, y_test = train_test_split (
    X_temp, y_temp, test_size = 0.50, random_state = 21, stratify = y_temp
)

# Set max_depth to 8 because it was overfitting and not learning but just memorising it, looked up sk documentation and tutorials and setting a max depth gets around this
decision_tree = DecisionTreeClassifier(
    max_depth = 8,
    min_samples_split = 20,
    min_samples_leaf = 10,
    class_weight = "balanced",
    random_state = 21
)

decision_tree.fit(X_train, y_train)


def evaluate_model(model, features_set, labels_set, set_name):
    predictions = model.predict(features_set)
    correct = sum(predictions == labels_set)
    total = len(labels_set)
    accuracy = correct / total

    print()
    print(set_name)
    print(f"Correct predictions: {correct}/{total}")
    print("Accuracy:", round(accuracy, 2))
    print()
    print("Classification Report:")
    print( classification_report(labels_set, predictions))
    print()

evaluate_model(decision_tree, X_validation, y_validation, "Validation")
evaluate_model(decision_tree, X_test, y_test, "Test")

# Modified a stack overflow snippet of code, this is something called "Feature Importance"
# It gives numerical "weights" to show how important each feature was and then displays them as a table
# I was told to add this buy a peer more familiar with AI because it helps you see if for some reason an important feature is having no impact
print()
print("Feature Importance:")
for feature_name, importance in sorted(
    zip(data.columns, decision_tree.feature_importances_), key=lambda x: -x[1]
):
    print(feature_name, round(importance, 3))


joblib.dump(decision_tree, "League_strategy_coach.pkl")
