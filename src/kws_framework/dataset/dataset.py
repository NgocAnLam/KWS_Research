"""
GSCv2 Dataset Loader and Episode Sampler for Few-shot KWS.

Design decisions (v2.0):
- Split: 25 seen / 5 unseen / 5 threshold (+ _background_noise_)
- Episode: 5-way, K-shot (K=1,3,5)
- Support: speaker-dependent (same speaker)
- Query: cross-speaker (any speaker in class)
"""

import os
import re
import random
import numpy as np
import soundfile as sf
from pathlib import Path
from typing import List, Tuple, Dict, Optional


SEEN_CLASSES = [
    "yes", "no", "up", "down", "left", "right",
    "on", "off", "stop", "go",
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "bed", "bird", "cat", "dog", "happy"
]

UNSEEN_CLASSES = ["house", "marvin", "sheila", "tree", "wow"]

THRESHOLD_CLASSES = ["backward", "forward", "visual", "follow", "learn"]


def _speaker_id_from_filename(filename: str) -> str:
    basename = os.path.basename(filename)
    match = re.match(r"([^_]+)_nohash", basename)
    return match.group(1) if match else basename


def _utterance_id_from_filename(filename: str) -> int:
    basename = os.path.basename(filename)
    match = re.search(r"_nohash_(\d+)", basename)
    return int(match.group(1)) if match else 0


class GSCv2Dataset:
    """Google Speech Commands v2 dataset loader."""

    def __init__(self, data_root: str, split: str = "training"):
        self.data_root = Path(data_root)
        self.split = split
        self.classes = sorted(os.listdir(self.data_root))
        self.classes = [c for c in self.classes
                        if os.path.isdir(self.data_root / c) and not c.startswith("_")]
        self._load_file_lists()
        self._build_index()

    def _load_file_lists(self):
        val_path = self.data_root / "validation_list.txt"
        test_path = self.data_root / "testing_list.txt"
        val_files = set(line.strip() for line in open(val_path)) if val_path.exists() else set()
        test_files = set(line.strip() for line in open(test_path)) if test_path.exists() else set()
        all_files = []
        for cls in self.classes:
            cls_dir = self.data_root / cls
            if cls_dir.is_dir():
                for f in os.listdir(cls_dir):
                    if f.endswith(".wav"):
                        all_files.append(f"{cls}/{f}")
        if self.split == "training":
            self.files = [f for f in all_files if f not in val_files and f not in test_files]
        elif self.split == "validation":
            self.files = [f for f in all_files if f in val_files]
        elif self.split == "testing":
            self.files = [f for f in all_files if f in test_files]
        else:
            raise ValueError(f"Unknown split: {self.split}")

    def _build_index(self):
        self.index = []
        for rel_path in self.files:
            cls = rel_path.split("/")[0]
            full_path = self.data_root / rel_path
            speaker = _speaker_id_from_filename(rel_path)
            utt_idx = _utterance_id_from_filename(rel_path)
            self.index.append((cls, str(full_path), speaker, utt_idx))

    def get_files_by_class(self, class_name: str) -> List[Tuple]:
        return [x for x in self.index if x[0] == class_name]

    def get_classes(self, group: str) -> List[str]:
        if group == "seen":
            return [c for c in SEEN_CLASSES if c in self.classes]
        elif group == "unseen":
            return [c for c in UNSEEN_CLASSES if c in self.classes]
        elif group == "threshold":
            return [c for c in THRESHOLD_CLASSES if c in self.classes]
        else:
            raise ValueError(f"Unknown group: {group}")

    @property
    def seen_classes(self):
        return self.get_classes("seen")

    @property
    def unseen_classes(self):
        return self.get_classes("unseen")

    def __len__(self):
        return len(self.index)

    def load_audio(self, filepath: str) -> np.ndarray:
        audio, sr = sf.read(filepath)
        assert sr == 16000, f"Expected 16kHz, got {sr}"
        if len(audio) > 16000:
            audio = audio[:16000]
        elif len(audio) < 16000:
            audio = np.pad(audio, (0, 16000 - len(audio)))
        return audio


class EpisodeSampler:
    """Episode sampler for few-shot evaluation.

    - N-way: number of classes per episode
    - K-shot: number of support samples per class
    - Support: speaker-dependent (same speaker for all support samples)
    - Query: cross-speaker (any speaker in the class, excluding support utterances)
    """

    def __init__(self, dataset: GSCv2Dataset, n_way: int = 5,
                 n_support: int = 1, n_query: int = 5, seed: int = 42):
        self.dataset = dataset
        self.n_way = n_way
        self.n_support = n_support
        self.n_query = n_query
        self.seed = seed
        self.rng = random.Random(seed)

    def sample_episode(self, classes: List[str]) -> Tuple[np.ndarray, np.ndarray,
                                                           np.ndarray, np.ndarray]:
        if len(classes) < self.n_way:
            raise ValueError(f"Not enough classes: need {self.n_way}, got {len(classes)}")
        chosen_classes = self.rng.sample(classes, self.n_way)

        support_data, support_labels = [], []
        query_data, query_labels = [], []

        for label_idx, cls in enumerate(chosen_classes):
            files = self.dataset.get_files_by_class(cls)
            speaker_groups = {}
            for f in files:
                spk = f[2]
                if spk not in speaker_groups:
                    speaker_groups[spk] = []
                speaker_groups[spk].append(f)

            valid_support = {s: sf for s, sf in speaker_groups.items()
                             if len(sf) >= self.n_support}
            if not valid_support:
                continue

            speaker = self.rng.choice(list(valid_support.keys()))
            speaker_files = valid_support[speaker]
            self.rng.shuffle(speaker_files)
            support_files = speaker_files[:self.n_support]

            all_files = files[:]
            self.rng.shuffle(all_files)
            used = {f[1] for f in support_files}
            query_files = [f for f in all_files if f[1] not in used][:self.n_query]

            if len(query_files) < self.n_query:
                continue

            for f in support_files:
                audio = self.dataset.load_audio(f[1])
                support_data.append(audio)
                support_labels.append(label_idx)
            for f in query_files:
                audio = self.dataset.load_audio(f[1])
                query_data.append(audio)
                query_labels.append(label_idx)

        assert len(support_data) > 0, (
            f"No valid episodes. n_support={self.n_support}, "
            f"n_query={self.n_query}, classes={classes}"
        )
        assert len(query_data) > 0, "No query data generated"

        return (np.stack(support_data), np.array(support_labels),
                np.stack(query_data), np.array(query_labels))
