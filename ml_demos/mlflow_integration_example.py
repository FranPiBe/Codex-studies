"""MLflow integration example."""
import mlflow
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_model(n_estimators=100):
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, random_state=42)
    with mlflow.start_run():
        mlflow.log_param("n_estimators", n_estimators)
        model = RandomForestClassifier(n_estimators=n_estimators)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")
    return acc

if __name__ == "__main__":
    mlflow.set_experiment("mlflow_demo")
    score = train_model()
    print("Logged run with accuracy", score)
