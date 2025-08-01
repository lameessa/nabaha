import requests
from urllib.parse import urlparse
import whois
from datetime import datetime

# Your real API keys
GOOGLE_SAFE_BROWSING_KEY = "AIzaSyAqwHLcc8eYDlJC36QBwLEigcAveVanjqk"
VIRUSTOTAL_KEY = "Yfe8b82fdf49aff2e8bc63421aa3a1aedae758080eba14f6b63a4e8ab3e54f4a0"

def check_link_safety(url):
    # Extract clean domain (remove www.)
    domain = urlparse(url).netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]

    result = {"domain": domain, "risk": "safe", "reason": []}

    # 1️⃣ Google Safe Browsing check
    try:
        gsb_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_KEY}"
        payload = {
            "client": {"clientId": "nabaha-app", "clientVersion": "1.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }
        gsb_response = requests.post(gsb_url, json=payload).json()
        if gsb_response.get("matches"):
            result["risk"] = "danger"
            result["reason"].append("Listed in Google Safe Browsing database")
    except Exception:
        result["reason"].append("Google Safe Browsing check failed")

    # 2️⃣ VirusTotal check
    try:
        vt_headers = {"x-apikey": VIRUSTOTAL_KEY}
        vt_resp = requests.get(f"https://www.virustotal.com/api/v3/domains/{domain}", headers=vt_headers).json()
        malicious_count = vt_resp.get("data", {}).get("attributes", {}).get("last_analysis_stats", {}).get("malicious", 0)
        if malicious_count > 0:
            result["risk"] = "danger"
            result["reason"].append(f"{malicious_count} security engines flagged this domain")
    except Exception:
        result["reason"].append("VirusTotal check failed")

    # 3️⃣ Lookalike phishing detection
    trusted_domains = ["paypal.com", "apple.com", "amazon.com", "bank.com"]
    for trusted in trusted_domains:
        trusted_clean = trusted.replace(".", "")
        domain_clean = domain.replace(".", "")
        if trusted_clean in domain_clean and trusted not in domain:
            result["risk"] = "danger"
            result["reason"].append(f"Possible impersonation of {trusted}")

    # 4️⃣ Suspicious keyword detection
    phishing_keywords = ["login", "secure", "verify", "update", "account", "banking", "signin", "password"]
    if any(keyword in domain for keyword in phishing_keywords):
        if result["risk"] != "danger":
            result["risk"] = "suspicious"
        result["reason"].append("Contains suspicious phishing-related keywords")

    # 5️⃣ Domain age check
    try:
        domain_info = whois.whois(domain)
        if domain_info.creation_date:
            creation_date = domain_info.creation_date[0] if isinstance(domain_info.creation_date, list) else domain_info.creation_date
            if (datetime.now() - creation_date).days < 30:
                if result["risk"] != "danger":
                    result["risk"] = "suspicious"
                result["reason"].append("Domain is newly registered (<30 days old)")
    except Exception:
        result["reason"].append("WHOIS check failed")

    return result
