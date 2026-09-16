def calculate_confidence(score, evidence_count):
    confidence = 30
    # Increase confidence based on evidence found
    confidence += evidence_count * 5
    # Increase confidence based on risk score
    confidence += score * 0.2    # Cap confidence
    return min(int(confidence),99)