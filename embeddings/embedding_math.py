import numpy as np

def construct_tag_vector(relevance: float, tag_embedding: list[float], polarity: str) -> np.ndarray:
    """
    Positive Tags: weight = relevance, vector = tag_embedding * weight
    Negative Tags: weight = relevance, vector = inverse(tag_embedding) * weight
    Neutral Tags: weight = relevance * 0.5, vector = tag_embedding * weight
    """
    base_vector = np.array(tag_embedding)
    if polarity == 'positive':
        weight = relevance
        return base_vector * weight
    elif polarity == 'negative':
        weight = relevance
        return -base_vector * weight
    else: # neutral
        weight = relevance * 0.5
        return base_vector * weight

def normalize_vector(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def compute_niche_embedding(tag_vectors: list[np.ndarray], neighborhood_vectors: list[np.ndarray]) -> np.ndarray:
    """
    niche_embedding = normalize(sum(all_tag_vectors) + sum(neighborhood_vectors))
    """
    total_sum = sum(tag_vectors) + sum(neighborhood_vectors)
    return normalize_vector(total_sum)

def compute_property_embedding(tag_vectors: list[np.ndarray]) -> np.ndarray:
    """
    property_embedding = normalize(sum(all_tag_vectors))
    """
    if not tag_vectors:
        return np.array([])
    return normalize_vector(sum(tag_vectors))

def compute_neighborhood_embedding(tag_vectors: list[np.ndarray]) -> np.ndarray:
    """
    neighborhood_embedding = normalize(sum(all_tag_vectors))
    """
    if not tag_vectors:
        return np.array([])
    return normalize_vector(sum(tag_vectors))

def update_client_embedding(base_vector: np.ndarray, feedback_adjustments: np.ndarray) -> np.ndarray:
    """
    client_embedding = normalize(base_preferences_vector + feedback_adjustments)
    """
    return normalize_vector(base_vector + feedback_adjustments)
