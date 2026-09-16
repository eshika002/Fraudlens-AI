def detect_extra_scams(text):
    text = text.lower()
    score = 0
    reasons = []
    scam_type = None
    # Delivery Scam
    if ("parcel" in text or "courier" in text
        or "delivery failed" in text or "shipment" in text
        or "package" in text):
        score += 70
        scam_type = "Delivery Scam"
        reasons.append("Fake delivery scam pattern detected")

    # Investment Scam
    elif (
        "double your money" in text or "guaranteed return" in text 
        or "investment plan" in text or "crypto investment" in text
        or "earn daily" in text):
        score += 50
        scam_type = "Investment Scam"
        reasons.append("Investment fraud pattern detected")

    # Tech Support Scam
    elif (
        "microsoft support" in text or "technical support" in text
        or "virus detected" in text or "device infected" in text
        or "call support immediately" in text):
        score += 50
        scam_type = "Tech Support Scam"
        reasons.append("Tech support scam pattern detected")
    return score, reasons, scam_type