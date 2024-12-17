# ruff: noqa: F401

import re
from pathlib import Path
from sdv.single_table import GaussianCopulaSynthesizer
import pandas as pd
import os
import random

filename = "syn_model_3.0.0.pkl"
BASE_DIR = Path(__file__).resolve(strict=True).parent
# __version__ = re.search(r'\d+\.\d+\.\d+', filename).group(0)
__version__ = "3.0.0"


def synthesize():
    synthesizer = GaussianCopulaSynthesizer.load(filepath=f"{BASE_DIR}/{filename}")
    synthesizer._set_random_state(random.randint(0, 1000000))
    return synthesizer.sample(num_rows=1).drop("Count", axis=1)
    # return pd.read_pickle(f"{BASE_DIR}/test.pkl")


if __name__ == "__main__":
    df = synthesize()
    print(df)
