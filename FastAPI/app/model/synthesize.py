# ruff: noqa: F401

import re
from pathlib import Path
from sdv.single_table import GaussianCopulaSynthesizer

filename = "syn_model_3.0.0.pkl"
BASE_DIR = Path(__file__).resolve(strict=True).parent
__version__ = re.search(r'\d+\.\d+\.\d+', filename).group(0)

def synthesize():
    synthesizer = GaussianCopulaSynthesizer.load(filepath=f"{BASE_DIR}/{filename}")
    return synthesizer.sample(num_rows=1)


if __name__ == "__main__":
    df = synthesize()
    print(df)