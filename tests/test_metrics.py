"""Tests for evaluation metrics (no torch dependency)."""

import numpy as np
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
from scipy.optimize import brentq
from scipy.interpolate import interp1d


def test_accuracy_perfect():
    y_true = np.array([0, 1, 2, 0, 1, 2])
    y_pred = np.array([0, 1, 2, 0, 1, 2])
    acc = accuracy_score(y_true, y_pred)
    assert acc == 1.0


def test_accuracy_random():
    np.random.seed(42)
    y_true = np.random.randint(0, 5, 1000)
    y_pred = np.random.randint(0, 5, 1000)
    acc = accuracy_score(y_true, y_pred)
    assert 0.15 < acc < 0.35


def test_auc_perfect():
    scores = np.array([0.1, 0.2, 0.3, 0.8, 0.9, 0.95])
    labels = np.array([0, 0, 0, 1, 1, 1])
    auc = roc_auc_score(labels, scores)
    assert auc == 1.0


def test_auc_random():
    np.random.seed(42)
    scores = np.random.rand(1000)
    labels = np.random.randint(0, 2, 1000)
    auc = roc_auc_score(labels, scores)
    assert 0.4 < auc < 0.6


def test_eer_definition():
    np.random.seed(42)
    pos_scores = np.random.randn(1000) * 0.5 + 0.8
    neg_scores = np.random.randn(1000) * 0.5 + 0.2
    scores = np.concatenate([pos_scores, neg_scores])
    labels = np.concatenate([np.ones(1000), np.zeros(1000)])
    fpr, tpr, _ = roc_curve(labels, scores)
    eer = brentq(lambda x: 1.0 - x - interp1d(fpr, tpr)(x), 0.0, 1.0)
    assert 0.1 < eer < 0.4


def test_far_definition():
    y_true = np.array([0, 0, 0, 1, 1, 1])
    y_pred = np.array([1, 1, 0, 1, 1, 0])  # 2 FA, 1 miss
    from sklearn.metrics import confusion_matrix
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    far = fp / (fp + tn)  # False Acceptance Rate
    frr = fn / (fn + tp)  # False Rejection Rate
    assert far == 2/3, f"Expected FAR=2/3, got {far}"
    assert frr == 1/3, f"Expected FRR=1/3, got {frr}"
