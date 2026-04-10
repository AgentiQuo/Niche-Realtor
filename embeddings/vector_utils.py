import numpy as np
from typing import List

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0.0
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
