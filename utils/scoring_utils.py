def calculate_polarity_score(relevance: float, polarity: str) -> float:
    if polarity == 'positive': return relevance
    if polarity == 'negative': return -relevance
    return relevance * 0.5
