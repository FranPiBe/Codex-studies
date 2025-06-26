# ML Demos

This folder contains small notebooks demonstrating common machine learning workflows. All datasets come from open sources such as scikit-learn or `torchvision`.

## Notebooks

- **random_forest_example.ipynb** – Minimal iris classifier using a random forest.
- **random_forest_regression.ipynb** – Predict California housing prices with `RandomForestRegressor`, showing feature importances and optional SHAP analysis.
- **decision_tree_classifier.ipynb** – Classify iris flowers with a decision tree and visualize the tree. Briefly discusses overfitting.
- **linear_regression_demo.ipynb** – Linear regression on the diabetes dataset with residual plots and coefficient interpretation.
- **logistic_regression_classifier.ipynb** – Breast cancer classification using logistic regression, ROC curve, AUC, and confusion matrix.
- **kmeans_clustering_demo.ipynb** – Unsupervised clustering example with KMeans including inertia and silhouette score.
- **cnn_with_optuna.ipynb** – Train a simple CNN on MNIST, tune hyperparameters with Optuna, and save the best model (can be tracked with MLflow).
- **shap_analysis_demo.ipynb** – Demonstrates computing SHAP values to explain a model's predictions.

## Script

- **mlflow_integration_example.py** – Utility script showing how to log parameters, metrics and a model to MLflow.

## References

- [scikit-learn documentation](https://scikit-learn.org/stable/)
- [Optuna documentation](https://optuna.org/)
- [MLflow documentation](https://mlflow.org/)
- [SHAP documentation](https://shap.readthedocs.io/)

Each notebook is self-contained and can be run independently once the required packages are installed.
