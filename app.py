import streamlit as st
import easyocr
import numpy as np
from PIL import Image
from io import BytesIO
import re
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

reader = load_reader()

st.set_page_config(
    page_title="FraudLens AI",
    page_icon="🛡️",
    layout="wide"
)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0E1117,#1A1F2E);
}
div[data-testid="metric-container"] {
    background-color:#1E2533;
    border:1px solid #00E5FF;
    padding:15px;
    border-radius:15px;
}
.stButton > button {
    width:100%;
    height:60px;
    font-size:20px;
    font-weight:bold;
    border-radius:15px;
    background:linear-gradient(90deg,#00E5FF,#00FF95);
    color:black;
}
</style>
""", unsafe_allow_html=True)


# Sidebar
st.sidebar.title("🛡️ FraudLens AI")

st.sidebar.info(
    """
    Multi-Modal Cyber Fraud
    Investigation Platform

    Detect:
    • Banking Scams
    • OTP Scams
    • Lottery Scams
    • Fake Job Scams
    • Suspicious link
    """
)

# Title
st.title("FraudLens AI")
st.subheader("Multi-Modal Cyber Fraud Investigation Platform")
# Sample messages
st.write("### Try a Sample Scam")

sample = st.selectbox(
    "Choose an example",
    [
        "None",
        "Bank KYC Scam",
        "Lottery Scam",
        "Fake Internship Scam",
        "Phishing Scam",
        "OTP Scam",
        "Utility Payment Scam"
    ]
)

message = ""

if sample == "Bank KYC Scam":
    message = """
Dear Customer,
Your KYC verification is pending.
Update your details now to continue using UPI and net banking services.
Click here:
https://kyc-update-bankverify.com
Failure to update may result in account restrictions.
"""

elif sample == "Lottery Scam":
    message = """
CONGRATULATIONS!!!
Your mobile number has been selected as the winner of the International Lucky Draw.
Prize Amount: ₹50,00,000.
To process your winnings, submit your Aadhaar details and bank account information.
Claim before midnight.
"""

elif sample == "Fake Internship Scam":
    message = """
Google Internship Offer
Pay ₹999 registration fee immediately
to secure your internship position.
"""
elif sample == "OTP Scam":
    message="""
Dear Customer,
Share your OTP immediately to complete verification.
Failure to do so may result in account suspension.
"""
elif sample == "Utility Payment Scam":
    message = """
URGENT!
Your electricity connection will be disconnected today.
Pay ₹2500 immediately using the link below.
https://power-bill-update.com.
"""

elif sample == "Phishing Scam":
    message = """
URGENT SECURITY ALERT
Your account has been locked.
Verify your account immediately:https://secure-bank-login-update.com
Failure to verify may result in suspension.
"""
# OCR Upload
st.write("### Upload Screenshot")
uploaded_file = st.file_uploader("Upload a suspicious screenshot",type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(
        image,
        caption="Uploaded Screenshot",
        use_container_width=True
    )

    with st.spinner("Extracting text from image..."):
        try:
            reader = easyocr.Reader(['en'])
            image_np = np.array(image)
            result = reader.readtext(image_np, detail=0)
            extracted_text = " ".join(result)
            st.success("Text extracted successfully!")
            st.write("### Extracted Text")
            st.text_area("OCR Output",extracted_text, height=150)
            message = extracted_text

        except Exception as e:
            st.error(f"OCR Error: {e}")

# Text input
message = st.text_area("Paste suspicious content", value=message, height=220 )

# Analyze Button
if st.button("Analyze Scam Risk"):

    if not message.strip():
        st.warning("Please enter a message or upload a screenshot.")

    else:

        score = 0
        reasons = []
        text = message.lower()
        keywords = {
            "winner": 25, "won": 25, "lottery": 30, "lucky draw": 30,
            "prize": 25, "reward": 20, "congratulations": 20, "selected": 15,
            "otp": 30, "password": 30,"aadhaar": 35, 
            "pan": 30, "bank account": 35, "account information": 25,
            "urgent": 20, "immediately": 20, "before midnight": 25,
            "kyc": 25, "bank": 20, "upi": 20, "verify": 15, "verification": 15,
            "account": 10, "restriction": 20, "restricted": 20,"suspended": 25,
            "click here": 20, "update now": 20,
            "job": 20, "internship": 20, "registration fee": 30, "payment": 20,
            "claim": 20, "winnings": 20, "mobile number": 10,
            "recent activity": 10,  "login": 25, "credentials": 30, "locked": 25,
            "confirm your details": 15, "verify account": 20,            
            "suspicious activity": 20, "security alert": 25,
            "share your otp": 40,"account suspension": 25,
            "complete verification": 20,"verification": 15,
            "failure to do so": 15,"secure your position": 20,"offer letter": 20,
            "selected candidate": 20,"limited seats": 20,
            "electricity": 25,"connection": 15,"disconnected": 30,
            "bill": 20,"pay": 20,"payment": 20,"today": 10,"power": 15,
            "electricity bill": 35,"service suspension": 25
        }

        # Keyword Detection

        for word, points in keywords.items():
            if word in text:
                score += points
                reasons.append(f"Detected: {word}")

        # URL Detection

        urls = re.findall(r'https?://\S+',text)
        if urls:
            score += 15
            reasons.append("Suspicious URL detected")
            if("pay" in text or "payment" in text or "electricity" in text or "bank" in text or "verify" in text):
                score +=20
                reasons.append("High-risk URL with scam indicators")

        # Special Rules

        if (("aadhaar" in text or "bank account" in text)
            and ("winner" in text or "prize" in text or "lottery" in text or "lucky draw" in text)):
            score += 40
            reasons.append("Lottery scam requesting sensitive information")
        if ("kyc" in text and ("bank" in text or "upi" in text)):
            score += 20
            reasons.append("KYC scam pattern detected")
        if (("registration fee" in text or "payment" in text) and ("job" in text or "internship" in text)):
            score += 40
            reasons.append("Fake job scam requesting payment")
        if ("login" in text and "bank account" in text):
            score += 25
            reasons.append("Bank login credential request")
        if "credentials" in text:
            score += 30
            reasons.append("Credential theft attempt")
        if ("locked" in text and "account" in text):
            score += 20
            reasons.append("Account lock scare tactic")
        if ("verification" in text and "account" in text):
            score += 15
            reasons.append("Account verification request")
        if ("otp" in text and ("verification" in text or "account suspension" in text or "share" in text)):
            score += 30
            reasons.append("OTP scam pattern detected")
        if (("electricity" in text or "power" in text)
            and ("pay" in text or "payment" in text)):
            score += 35
            reasons.append("Utility payment scam pattern detected")

        # Scam Classification
        scam_type = "Unknown Scam"
        if ("kyc" in text and ("bank" in text or "upi" in text)):
            scam_type = "Banking / KYC Scam"
        elif "otp" in text:
            scam_type = "OTP Scam"
        elif ("winner" in text or "lottery" in text or "lucky draw" in text or "prize" in text ):
            scam_type = "Lottery / Prize Scam"
        elif ("job" in text or "internship" in text):
            scam_type = "Fake Job Scam"
        elif ("login" in text or "credentials" in text or "verify account" in text  or "security alert" in text):
            scam_type = "Phishing Scam"
        elif ("electricity" in text or "power" in text or "bill" in text):
            scam_type = "Utility Payment Scam"

        score = min(int(score * 0.6),95)

        # Dashboard
        col1, col2, col3 = st.columns(3)
        col1.metric("Risk Score", f"{score}%")
        col2.metric("Threat Type",scam_type.replace("Scam",""))
        col3.metric("Evidence Found",len(reasons))

        st.write("## Threat Meter")
        st.progress(score / 100)
        if score >= 70:
            color = "#FF1744"
        elif score >= 40:
            color = "#FF9100"
        else:
            color = "#00C853"
            st.markdown(
                f"""
                <h1 style='text-align:center;color:{color};'>
                {score}% Risk
                </h1>
                """,
                unsafe_allow_html=True
                )
            
        # AI Investigation Report
        if scam_type == "Banking / KYC Scam":
            ai_report = """
This message appears to be a Banking/KYC scam.
The sender creates urgency and attempts to collect sensitive banking information.
Legitimate banks generally do not request KYC verification through unsolicited messages.
"""

        elif scam_type == "Lottery / Prize Scam":
            ai_report = """
This message appears to be a Lottery/Prize scam.
Large rewards are commonly used to trick victims into sharing personal or financial information.
"""

        elif scam_type == "Fake Job Scam":
            ai_report = """
This message appears to be a Fake Job scam.
The sender requests payment before employment, which is a common recruitment fraud tactic.
"""

        elif scam_type == "OTP Scam":
            ai_report = """
This message appears to be an OTP scam.
Attackers use OTP requests to gain unauthorized access to accounts.
"""

        elif scam_type == "Phishing Scam":
            ai_report = """
This message appears to be a phishing attempt.
The sender is attempting to obtain login credentials or account information through deception.
"""

        elif scam_type == "Utility Payment Scam":
            ai_report = """
This message appears to be a Utility Payment Scam.
The sender creates urgency by threatening service disconnection and pressures the recipient to make an immediate payment.
Legitimate utility providers usually communicate through official websites, apps, customer portals, or verified customer support channels rather than suspicious links.
The combination of urgent payment requests, service suspension threats, and external links is a common indicator of utility-bill fraud.
"""
        else:
            ai_report = """
Suspicious indicators were detected.Further verification is recommended.
"""

        st.write("### 🤖 AI Investigation Report")
        st.info(ai_report)
        

        # URL Analysis
        if urls:
            st.write("### 🌐 URL Analysis") 
            suspicious_words = [
                "verify", "update", "kyc","lottery",              
                "bank","winner","reward", "login"                  
            ]
            for url in urls:
                risk = "Low"
                for word in suspicious_words:
                    if word in url.lower():
                        risk = "High"
                st.write(f"URL: {url}")
                st.write( f"Risk Level: {risk}")

        # Evidence
        st.write("### Evidence Found")
        if reasons:
            for reason in reasons:
                st.success(reason)
                # st.write(f"✓ {reason}")

        else:
            st.write("No major scam indicators found.")

        # Recommendation
        st.write("### Recommendation")
        if score >= 70:
            st.error(
                """
Do NOT:
• Click suspicious links
• Share OTPs
• Share Aadhaar/PAN details
• Transfer money
• Reveal banking credentials
"""
            )
        elif score >= 40:
            st.warning("Verify the sender through official channels before taking action.")
        else:
            st.success("No major risk indicators detected.")
    #Download Investigation report
    report = f"""
    SCAMRADAR AI INVESTIGATION REPORT
    ================================
        Risk Score: {score}%
        Threat Type: {scam_type}
        Evidence Found:
        """
    for reason in reasons:
            report += f"\n- {reason}"

    report += f"""
            AI Investigation Report:
            {ai_report}
            Recommendation:
            """
    if score >= 70:
        report += """
                DO NOT:
                - Click suspicious links
                - Share OTPs
                - Share Aadhaar/PAN details
                - Transfer money
                - Reveal banking credentials
                """
    elif score >= 40:
        report += """
                Verify the sender through official channels.
                """
    else:
        report += """
                No major risk indicators detected.
                """
    st.download_button(
                label="📄 Download Investigation Report",
                data=report,
                file_name="ScamRadar_Report.txt",
                mime="text/plain"
                )
                            
st.markdown("---")
st.markdown("""
<center>
🛡️ FraudLens AI v1.0<br>
Built for Snapdragon AI Lab Build & Present Challenge
</center>
""", unsafe_allow_html=True)        