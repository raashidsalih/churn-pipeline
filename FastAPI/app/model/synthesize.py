# ruff: noqa: F401

import pickle
from pathlib import Path
from sdv.single_table import GaussianCopulaSynthesizer

__version__ = "2.1.0"

BASE_DIR = Path(__file__).resolve(strict=True).parent

# with open(f"{BASE_DIR}/model-{__version__}.pkl", "rb") as f:
synthesizer = GaussianCopulaSynthesizer.load(
filepath=f"{BASE_DIR}/syn_model_2.1.0.pkl"
)


def synthesize():
    return synthesizer.sample(
    num_rows=1
    )

# if __name__ == "__main__":
#     df = synthesize()
