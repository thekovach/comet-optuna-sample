"""
Optuna example that optimizes a classifier configuration for Iris dataset using sklearn.

In this example, we optimize a classifier configuration for Iris dataset. Classifiers are from
scikit-learn. We optimize both the choice of classifier (among SVC and RandomForest) and their
hyperparameters.

"""

# import comet_ml at the top of your file
from comet_ml import API, APIExperiment, Experiment
import comet_ml

import optuna
from optuna.integration.comet import CometCallback

import sklearn.datasets
import sklearn.ensemble
import sklearn.model_selection
import sklearn.svm

# FYI: Objective functions can take additional arguments
# (https://optuna.readthedocs.io/en/stable/faq.html#objective-func-additional-args).
def objective(trial):
    iris = sklearn.datasets.load_iris()
    x, y = iris.data, iris.target

    classifier_name = trial.suggest_categorical("classifier", ["SVC", "RandomForest"])
    if classifier_name == "SVC":
        svc_c = trial.suggest_float("svc_c", 1e-10, 1e10, log=True)
        classifier_obj = sklearn.svm.SVC(C=svc_c, gamma="auto")
    else:
        rf_max_depth = trial.suggest_int("rf_max_depth", 2, 32, log=True)
        classifier_obj = sklearn.ensemble.RandomForestClassifier(
            max_depth=rf_max_depth, n_estimators=10
        )

    score = sklearn.model_selection.cross_val_score(classifier_obj, x, y, n_jobs=-1, cv=3)
    accuracy = score.mean()

    return accuracy


if __name__ == "__main__":
    comet_kwargs = {"project_name": "optuna-comet"}
    cometc = CometCallback(comet_kwargs=comet_kwargs)
    
    study = optuna.create_study(direction="maximize", study_name="sklearn_simple")
    study.optimize(objective, n_trials=2, n_jobs=1, callbacks=[cometc])


