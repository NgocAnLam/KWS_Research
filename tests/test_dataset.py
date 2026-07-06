"""Tests for dataset module: GSCv2 loader and EpisodeSampler."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import tempfile
from pathlib import Path
import soundfile as sf
import numpy as np

from kws_framework.dataset.dataset import (
    GSCv2Dataset, EpisodeSampler,
    SEEN_CLASSES, UNSEEN_CLASSES, THRESHOLD_CLASSES,
    _speaker_id_from_filename, _utterance_id_from_filename
)


def _create_dummy_gscv2(root: Path, num_samples_per_class: int = 12):
    """Create a minimal GSCv2-like directory for testing.
    Uses GSCv2 filename convention: {speaker_id}_nohash_{trial}.wav
    """
    all_classes = SEEN_CLASSES[:2] + UNSEEN_CLASSES[:2] + THRESHOLD_CLASSES[:1]
    n_speakers = 3
    samples_per_speaker = num_samples_per_class // n_speakers
    speaker_ids = [f"speaker{i}" for i in range(n_speakers)]
    for cls in all_classes:
        cls_dir = root / cls
        cls_dir.mkdir(parents=True, exist_ok=True)
        for spk_id in speaker_ids:
            for i in range(samples_per_speaker):
                filename = f"{spk_id}_nohash_{i}.wav"
                filepath = cls_dir / filename
                audio = np.random.randn(16000).astype(np.float32) * 0.1
                sf.write(str(filepath), audio, 16000)


def test_speaker_id_extraction():
    assert _speaker_id_from_filename("speaker1_nohash_0.wav") == "speaker1"
    assert _speaker_id_from_filename("path/to/speaker2_nohash_3.wav") == "speaker2"
    assert _utterance_id_from_filename("speaker1_nohash_0.wav") == 0
    assert _utterance_id_from_filename("speaker1_nohash_3.wav") == 3


def test_dataset_initialization():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "speech_commands_v0.02"
        _create_dummy_gscv2(root)

        ds = GSCv2Dataset(str(root), split="training")
        assert len(ds) > 0
        assert len(ds.seen_classes) > 0
        assert len(ds.unseen_classes) > 0


def test_episode_sampler_basic():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "speech_commands_v0.02"
        _create_dummy_gscv2(root)

        ds = GSCv2Dataset(str(root), split="training")
        unseen = ds.unseen_classes
        cls_files = ds.get_files_by_class(unseen[0])
        assert len(cls_files) > 0, \
            f"No files for unseen class '{unseen[0]}'. Classes: {ds.classes}"

        # n_way=2 matches the 2 unseen classes in dummy data
        sampler = EpisodeSampler(ds, n_way=2, n_support=2, n_query=2, seed=42)

        support_data, support_labels, query_data, query_labels = \
            sampler.sample_episode(unseen)

        assert support_data.shape[0] == 4  # 2-way × 2-support
        assert support_labels.shape[0] == 4
        assert query_data.shape[0] == 4    # 2-way × 2-query
        assert query_labels.shape[0] == 4
        assert support_labels.min() >= 0
        assert support_labels.max() < 2
        assert query_labels.min() >= 0
        assert query_labels.max() < 2


def test_episode_sampler_no_overlap():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "speech_commands_v0.02"
        _create_dummy_gscv2(root, num_samples_per_class=12)
        ds = GSCv2Dataset(str(root), split="training")
        sampler = EpisodeSampler(ds, n_way=2, n_support=2, n_query=2, seed=42)

        for c in ds.unseen_classes:
            files = ds.get_files_by_class(c)
            assert len(files) >= 4, f"Need >=4 files for {c}, got {len(files)}"

        sd, sl, qd, ql = sampler.sample_episode(ds.unseen_classes)
        assert sd.shape[0] == 4, f"Expected 4 support, got {sd.shape[0]}"
        assert qd.shape[0] == 4, f"Expected 4 query, got {qd.shape[0]}"


def test_episode_sampler_reproducibility():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "speech_commands_v0.02"
        _create_dummy_gscv2(root)
        ds = GSCv2Dataset(str(root), split="training")

        sampler1 = EpisodeSampler(ds, n_way=2, n_support=2, n_query=2, seed=42)
        sampler2 = EpisodeSampler(ds, n_way=2, n_support=2, n_query=2, seed=42)

        s1, sl1, q1, ql1 = sampler1.sample_episode(ds.unseen_classes)
        s2, sl2, q2, ql2 = sampler2.sample_episode(ds.unseen_classes)

        assert np.array_equal(sl1, sl2), "Support labels should match"
        assert np.array_equal(ql1, ql2), "Query labels should match"
