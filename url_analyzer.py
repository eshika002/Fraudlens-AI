import re
def analyze_urls(text):
    urls = re.findall(r'https?://\S+', text)
    findings = []
    score = 0
    suspicious_keywords = [
        "verify","update", "login",
        "secure","bank","kyc","reward",
        "winner","claim","payment","delivery",
        "parcel","courier","shipment"
    ]

    shorteners = [
        "bit.ly","tinyurl","goo.gl","t.co"
    ]

    for url in urls:
        findings.append(f"URL Found: {url}")
        keyword_count = 0
        for word in suspicious_keywords:
            if word in url.lower():
                keyword_count += 1
        if keyword_count >= 2:
            score += 25
            findings.append("High-risk URL with scam indicators")
        for short in shorteners:
            if short in url.lower():
                score += 20
                findings.append("URL shortener detected")
        if "-" in url:
            score += 10
            findings.append("Hyphenated domain detected")
        if len(url) > 50:
            score += 10
            findings.append("Unusually long URL")
    return score, findings, urls