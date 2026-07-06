"""
Evaluator for few-shot KWS with comprehensive metrics.
Metrics: Accuracy, Precision, Recall, F1, AUC, EER, acc@1%FAR, acc@5%FAR.
"""

import numpy as np
import torch
from sklearn.metrics import accuracy_score, precision_score, recall_score, \
    f1_score, roc_auc_score, roc_curve, confusion_matrix
from scipy.optimize import brentq
from scipy.interpolate import interp1d


class Evaluator:

    def __init__(self, model, feature_extractor, config, device=None):
        self.model = model
        self.feature_extractor = feature_extractor
        self.config = config
        self.device = device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.feature_extractor.to(self.device)

    @torch.no_grad()
    def evaluate_full(self, episode_sampler, n_episodes=600):
        self.model.eval()
        self.feature_extractor.eval()
        all_preds, all_labels = [], []
        pos_scores, neg_scores = [], []

        for _ in range(n_episodes):
            support_data, support_labels, query_data, query_labels = \
                episode_sampler.sample_episode(
                    episode_sampler.dataset.unseen_classes)
            sd = torch.FloatTensor(support_data).to(self.device)
            qd = torch.FloatTensor(query_data).to(self.device)
            sl = torch.LongTensor(support_labels).to(self.device)
            ql = torch.LongTensor(query_labels).to(self.device)

            sup_feat = self.feature_extractor(sd)
            que_feat = self.feature_extractor(qd)
            sup_emb = self.model(sup_feat)
            que_emb = self.model(que_feat)

            n_cls = len(torch.unique(sl))
            if n_cls < 2:
                continue
            protos = torch.zeros(n_cls, sup_emb.size(-1), device=self.device)
            for i, c in enumerate(torch.unique(sl)):
                protos[i] = sup_emb[sl == c].mean(0)

            protos = torch.nn.functional.normalize(protos, p=2, dim=1)
            que_emb = torch.nn.functional.normalize(que_emb, p=2, dim=1)
            sim = torch.mm(que_emb, protos.t())

            label_map = {orig.item(): i for i, orig in enumerate(torch.unique(sl))}
            preds = sim.argmax(dim=1)
            mapped_labels = torch.tensor([label_map[l.item()] for l in ql],
                                         device=self.device)
            all_preds.extend(preds.cpu().tolist())
            all_labels.extend(mapped_labels.cpu().tolist())

            for i in range(len(ql)):
                correct_idx = label_map[ql[i].item()]
                pos = sim[i, correct_idx].item()
                if sim.size(1) > 1:
                    neg_mask = torch.ones(sim.size(1), dtype=torch.bool,
                                          device=self.device)
                    neg_mask[correct_idx] = False
                    neg = sim[i, neg_mask].max().item()
                else:
                    neg = -1.0
                pos_scores.append(pos)
                neg_scores.append(neg)

        # Classification metrics
        acc = accuracy_score(all_labels, all_preds)
        prec = precision_score(all_labels, all_preds, average="macro",
                               zero_division=0)
        rec = recall_score(all_labels, all_preds, average="macro", zero_division=0)
        f1 = f1_score(all_labels, all_preds, average="macro", zero_division=0)
        cm = confusion_matrix(all_labels, all_preds).tolist()

        # ROC-based metrics
        scores = np.array(pos_scores + neg_scores)
        labels = np.array([1] * len(pos_scores) + [0] * len(neg_scores))
        fpr = np.array([0, 1])
        tpr = np.array([0, 1])
        auc = 0.0
        eer = 0.5
        try:
            auc = roc_auc_score(labels, scores)
            fpr, tpr, thr = roc_curve(labels, scores)
            eer = float(brentq(lambda x: 1 - x - interp1d(fpr, tpr)(x), 0.0, 1.0))
        except Exception:
            pass

        acc_1pct = float(tpr[np.argmin(np.abs(fpr - 0.01))]) if len(fpr) > 1 else 0.0
        acc_5pct = float(tpr[np.argmin(np.abs(fpr - 0.05))]) if len(fpr) > 1 else 0.0

        return {
            "accuracy": float(acc),
            "accuracy_std": 0.0,
            "precision": float(prec),
            "recall": float(rec),
            "f1": float(f1),
            "auc": float(auc),
            "eer": float(eer),
            "acc_at_1pct_far": acc_1pct,
            "acc_at_5pct_far": acc_5pct,
            "far": float(fpr[1] if len(fpr) > 1 and len(tpr) > 1 else 0),
            "frr": float(1 - tpr[1] if len(tpr) > 1 else 0),
            "confusion_matrix": cm,
        }

    @torch.no_grad()
    def compute_prototypes(self, support_data, support_labels):
        self.model.eval()
        sup_feat = self.feature_extractor(support_data.to(self.device))
        sup_emb = self.model(sup_feat)
        n_cls = len(torch.unique(support_labels))
        protos = torch.zeros(n_cls, sup_emb.size(-1), device=self.device)
        for c in range(n_cls):
            protos[c] = sup_emb[support_labels.to(self.device) == c].mean(0)
        return torch.nn.functional.normalize(protos, p=2, dim=1)
