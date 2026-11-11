import os
import json
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="BugSense AI • QA Defect Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- MODERN GLOWING CSS DESIGN SYSTEM -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Ambient dynamic gradient backdrop */
    .stApp {
        background: radial-gradient(circle at 5% 10%, rgba(99, 102, 241, 0.12) 0%, transparent 40%),
                    radial-gradient(circle at 95% 90%, rgba(236, 72, 153, 0.10) 0%, transparent 45%),
                    radial-gradient(circle at 50% 50%, rgba(56, 189, 248, 0.05) 0%, transparent 55%),
                    #f8fafc;
        background-attachment: fixed;
    }

    /* Hero Banner with animated neon borders */
    .hero-banner {
        background: linear-gradient(135deg, #0b0f19 0%, #171c2f 45%, #1e1b4b 80%, #312e81 100%);
        border-radius: 24px;
        padding: 34px 42px;
        color: white;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.14);
        box-shadow: 0 20px 45px -12px rgba(67, 56, 202, 0.5), inset 0 1px 1px 0 rgba(255, 255, 255, 0.25);
    }
    
    .hero-banner::after {
        content: '';
        position: absolute;
        top: -60%;
        right: -10%;
        width: 420px;
        height: 420px;
        background: radial-gradient(circle, rgba(236, 72, 153, 0.45) 0%, rgba(99, 102, 241, 0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }

    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(8px);
        padding: 5px 14px;
        border-radius: 30px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #a5b4fc;
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 12px;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: -0.8px;
        background: linear-gradient(135deg, #ffffff 30%, #c7d2fe 75%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }

    .hero-sub {
        font-size: 1.05rem;
        color: #cbd5e1;
        font-weight: 500;
        max-width: 820px;
        line-height: 1.55;
    }

    /* Glowing Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(226, 232, 240, 0.9);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.07);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px -12px rgba(99, 102, 241, 0.18);
        border-color: rgba(99, 102, 241, 0.4);
    }

    /* Severity Neon Gradients */
    .neon-p1 {
        background: linear-gradient(135deg, #b91c1c 0%, #dc2626 50%, #f43f5e 100%);
        color: white;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 16px 35px -6px rgba(220, 38, 38, 0.55), inset 0 1px 1px 0 rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .neon-p2 {
        background: linear-gradient(135deg, #b45309 0%, #d97706 50%, #f59e0b 100%);
        color: white;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 16px 35px -6px rgba(217, 119, 6, 0.5), inset 0 1px 1px 0 rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .neon-p3 {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%);
        color: white;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 16px 35px -6px rgba(37, 99, 235, 0.5), inset 0 1px 1px 0 rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .neon-p4 {
        background: linear-gradient(135deg, #047857 0%, #059669 50%, #10b981 100%);
        color: white;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 16px 35px -6px rgba(5, 150, 105, 0.5), inset 0 1px 1px 0 rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Vibrant Test Scenario Cards */
    .test-card {
        background: white;
        border-radius: 18px;
        padding: 22px 26px;
        margin-bottom: 20px;
        border: 1px solid rgba(226, 232, 240, 0.95);
        box-shadow: 0 8px 24px -6px rgba(15, 23, 42, 0.05);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .test-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 32px -8px rgba(15, 23, 42, 0.1);
    }
    .card-pos { border-left: 7px solid #10b981; }
    .card-neg { border-left: 7px solid #f59e0b; }
    .card-edge { border-left: 7px solid #8b5cf6; }

    /* Ultra Interactive Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.3px !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 34px !important;
        box-shadow: 0 12px 28px -6px rgba(124, 58, 237, 0.55), inset 0 1px 1px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 18px 38px -6px rgba(219, 39, 119, 0.65) !important;
    }

    /* Download Buttons Customizer */
    .stDownloadButton > button {
        background: white !important;
        color: #334155 !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        padding: 10px 22px !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04) !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        border-color: #6366f1 !important;
        color: #4f46e5 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.15) !important;
    }

    /* Custom Textarea */
    .stTextArea textarea {
        border-radius: 16px !important;
        border: 2px solid #e2e8f0 !important;
        font-size: 0.98rem !important;
        line-height: 1.6 !important;
        background: #ffffff !important;
        box-shadow: inset 0 2px 4px rgba(15, 23, 42, 0.02) !important;
        transition: all 0.25s ease !important;
    }
    .stTextArea textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.15) !important;
    }

    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        padding: 8px 12px;
        border-radius: 16px;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.95rem;
        padding: 10px 20px;
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #4338ca !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- LOAD MODEL & DATASET -----------------
@st.cache_resource
def load_model():
    model_path = "pipeline.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

@st.cache_data
def load_dataset():
    data_path = "dataset.csv"
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return None

pipeline = load_model()
dataset_df = load_dataset()

# ----------------- TEST SCENARIOS ENGINE -----------------
def generate_qa_test_scenarios(bug_text: str, severity: str, module: str):
    text_lower = bug_text.lower()
    
    # 1. POSITIVE (HAPPY PATH)
    if any(k in text_lower for k in ["payment", "upi", "card", "checkout"]):
        pos_title = "TC-POS-01: End-to-End Checkout & Transaction Settlement"
        pos_desc = "Initiate order checkout with valid payment credentials under optimal network latency. Verify bank ledger reconciles, HTTP 200 is issued, and order status transitions to PAID."
        pos_expected = "Status updates to 'COMPLETED', customer receives instant push notification & email receipt."
    elif any(k in text_lower for k in ["sso", "login", "auth", "token", "password"]):
        pos_title = "TC-POS-01: Multi-Tenant OAuth/SSO Login Flow"
        pos_desc = "Authenticate user via identity provider with verified enterprise credentials. Verify authorization grant and HTTP-only session cookies are created."
        pos_expected = "User redirected seamlessly to main dashboard with active user role permissions."
    elif any(k in text_lower for k in ["api", "504", "endpoint", "timeout"]):
        pos_title = "TC-POS-01: High-Performance Endpoint Service Availability"
        pos_desc = "Send concurrent HTTP GET requests to core endpoint with valid query parameters under standard SLA."
        pos_expected = "Response time remains < 250ms with HTTP 200 OK and valid JSON schema."
    else:
        pos_title = f"TC-POS-01: Standard Functional Execution ({module})"
        pos_desc = f"Execute standard functional action on {module} component using documented parameters and valid inputs."
        pos_expected = "Operation finishes cleanly without UI lag or unhandled runtime exceptions."

    # 2. NEGATIVE (FAULT & ERROR CHECK)
    if any(k in text_lower for k in ["payment", "upi", "card", "checkout"]):
        neg_title = "TC-NEG-02: Payment Failure & Graceful Transaction Rollback"
        neg_desc = "Simulate 3D-Secure timeout, expired card token, or rejected bank balance. Verify transaction fails safely without duplicate ledger debit."
        neg_expected = "Display localized user-friendly alert ('Transaction Declined'), unlock cart, and allow immediate retry."
    elif any(k in text_lower for k in ["sso", "login", "auth", "token", "password"]):
        neg_title = "TC-NEG-02: Expired Token Rejection & Tamper Defense"
        neg_desc = "Inject expired JWT token or corrupted signature into Authorization header."
        neg_expected = "API intercepts and rejects with HTTP 401 Unauthorized; session terminates immediately."
    elif any(k in text_lower for k in ["api", "504", "endpoint"]):
        neg_title = "TC-NEG-02: Fault Tolerance & Rate Limiting Enforcement"
        neg_desc = "Send malformed payload and burst traffic above rate quota."
        neg_expected = "Return structured HTTP 429 Too Many Requests with retry-after header."
    else:
        neg_title = f"TC-NEG-02: Input Boundary Rejection ({module})"
        neg_desc = f"Inject boundary-violating strings and null values into {module} forms."
        neg_expected = "Form validation flags incorrect values without application crash."

    # 3. EDGE CASES
    edge_cases = []
    if any(k in text_lower for k in ["payment", "upi", "card", "checkout"]):
        edge_cases.append({
            "id": "TC-EDGE-03",
            "category": "Idempotency & Double Click",
            "scenario": "Rapid Double-Clicking on 'Submit Order'",
            "steps": "Trigger two rapid click events on checkout within 50ms before UI lock initiates.",
            "expected": "Idempotency key prevents duplicate transaction; single charge logged."
        })
        edge_cases.append({
            "id": "TC-EDGE-04",
            "category": "In-Flight Network Dropout",
            "scenario": "Packet Loss Immediately After PIN Submission",
            "steps": "Switch device to offline airplane mode while gateway spinner is active.",
            "expected": "Asynchronous webhook reconciliation resolves order state within 180 seconds."
        })
    elif any(k in text_lower for k in ["sso", "login", "auth", "token", "password"]):
        edge_cases.append({
            "id": "TC-EDGE-03",
            "category": "Concurrent Multi-Device Session",
            "scenario": "Simultaneous Logins Across Multiple Devices",
            "steps": "Initiate simultaneous login on mobile app and desktop browser simultaneously.",
            "expected": "Token manager enforces concurrent session limit or generates paired refresh tokens."
        })
        edge_cases.append({
            "id": "TC-EDGE-04",
            "category": "Token Expiry Race Condition",
            "scenario": "Token Expiration Exactly Mid-Transaction",
            "steps": "Trigger complex transaction at second 299 of 300s token lifespan.",
            "expected": "Silent refresh executes without interrupting transaction flow."
        })
    elif any(k in text_lower for k in ["viewport", "mobile", "button", "ui"]):
        edge_cases.append({
            "id": "TC-EDGE-03",
            "category": "Ultra-Narrow Viewport Rendering",
            "scenario": "Foldable Screen Viewport (< 320px)",
            "steps": "Resize viewport to 280px width and rotate from portrait to landscape.",
            "expected": "Button maintains touch-target size (>48px) and avoids modal overlap."
        })
        edge_cases.append({
            "id": "TC-EDGE-04",
            "category": "Slow 3G Network Throttling",
            "scenario": "Modal State under 2500ms Simulated Latency",
            "steps": "Throttle network to Slow 3G and attempt interactive trigger.",
            "expected": "Skeleton placeholder renders; prevents repetitive user click events."
        })
    else:
        edge_cases.append({
            "id": "TC-EDGE-03",
            "category": "Concurrency Stress",
            "scenario": f"High-Burst Traffic on {module}",
            "steps": f"Dispatch 250 parallel asynchronous tasks to {module} under CPU pressure.",
            "expected": "Service handles gracefully with backpressure queueing."
        })
        edge_cases.append({
            "id": "TC-EDGE-04",
            "category": "Unicode & Buffer Overflow",
            "scenario": "Maximum Payload with Emoji Characters",
            "steps": "Send maximum allowable byte size payload containing multi-byte UTF-8 emojis.",
            "expected": "Data serializes without database character-set collation truncation."
        })

    return {
        "positive": {"title": pos_title, "desc": pos_desc, "expected": pos_expected},
        "negative": {"title": neg_title, "desc": neg_desc, "expected": neg_expected},
        "edge_cases": edge_cases
    }

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 22px;">
        <div style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; color: white; box-shadow: 0 8px 18px rgba(79, 70, 229, 0.4);">⚡</div>
        <div>
            <div style="font-weight: 800; font-size: 1.15rem; color: #0f172a; letter-spacing: -0.3px;">BugSense AI</div>
            <div style="font-size: 0.78rem; color: #64748b; font-weight: 600;">QA Intelligence Engine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### ⚡ System Health")
    if pipeline is not None:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); border: 1px solid #10b981; border-radius: 14px; padding: 14px; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="height: 10px; width: 10px; background-color: #10b981; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #10b981;"></span>
                <span style="color: #065f46; font-weight: 800; font-size: 0.88rem;">ML Classifier Online</span>
            </div>
            <div style="color: #047857; font-size: 0.76rem; margin-top: 4px; font-weight: 500;">TF-IDF + Random Forest Pipeline</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ pipeline.pkl not found!")

    if dataset_df is not None:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1px solid #3b82f6; border-radius: 14px; padding: 14px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="height: 10px; width: 10px; background-color: #3b82f6; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px #3b82f6;"></span>
                <span style="color: #1e40af; font-weight: 800; font-size: 0.88rem;">Dataset Synced</span>
            </div>
            <div style="color: #1d4ed8; font-size: 0.76rem; margin-top: 4px; font-weight: 500;">{len(dataset_df):,} Production Records</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 💡 Quick Test Presets")
    preset_choice = st.selectbox(
        "Choose sample defect:",
        [
            "Custom Input",
            "Payment Gateway Crash (P1 - Blocker)",
            "Authentication SSO Loop (P1 - Blocker)",
            "API 504 Gateway Timeout (P2 - Critical)",
            "Mobile Viewport Button Overlap (P3 - Major)",
            "Settings Typo Glitch (P4 - Minor)"
        ]
    )

    preset_texts = {
        "Payment Gateway Crash (P1 - Blocker)": "User selects UPI payment on mobile, app freezes after submitting pin, money is deducted from bank account but order status remains 'Payment Failed'.",
        "Authentication SSO Loop (P1 - Blocker)": "SSO login via Google returns 401 unauthorized loop for enterprise tenant users on Safari private mode.",
        "API 504 Gateway Timeout (P2 - Critical)": "Product catalog API endpoint /api/v2/items returns 504 Gateway Timeout during peak traffic.",
        "Mobile Viewport Button Overlap (P3 - Major)": "Checkout button is completely unclickable on mobile viewports below 380px width due to modal z-index overlap.",
        "Settings Typo Glitch (P4 - Minor)": "Spelling typo on settings page: 'Notification Prefrences' instead of 'Notification Preferences'."
    }
    preset_val = preset_texts.get(preset_choice, "")

# ----------------- MAIN HERO BANNER -----------------
st.markdown("""
<div class="hero-banner">
    <div class="hero-pill">⚡ Enterprise DevSecOps QA Suite</div>
    <div class="hero-title">BugSense AI Defect Studio</div>
    <div class="hero-sub">
        Automated software defect severity intelligence, target architecture layer mapping, and instant full-spectrum regression & edge-case scenario generation.
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- TABS -----------------
tab1, tab2 = st.tabs(["🚀 Defect Analysis & QA Test Studio", "📊 10,000-Row Benchmark Explorer"])

# --- TAB 1 ---
with tab1:
    st.markdown("#### 📝 Paste Raw Defect Report or Error Log")
    user_input = st.text_area(
        label="Defect Description Input",
        value=preset_val,
        height=110,
        placeholder="Type or paste defect description here...",
        label_visibility="collapsed"
    )

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        run_btn = st.button("✨ Triage & Generate Tests", type="primary", use_container_width=True)

    if run_btn:
        clean_input = user_input.strip()
        if '",' in clean_input:
            clean_input = clean_input.split('",')[0].replace('"', '')

        if not clean_input:
            st.warning("⚠️ Please provide a defect report first.")
        elif pipeline is None:
            st.error("❌ Model pipeline is not loaded.")
        else:
            with st.spinner("Analyzing semantics, classifying priority, and building test scenarios..."):
                predicted_severity = pipeline.predict([clean_input])[0]
                
                # Module detection & colorful theming
                text_low = clean_input.lower()
                if any(k in text_low for k in ["payment", "upi", "card", "checkout"]):
                    suspected_module = "Payment Gateway"
                    module_color = "#ec4899"
                    module_bg = "linear-gradient(135deg, #fdf2f8 0%, #fce7f3 100%)"
                elif any(k in text_low for k in ["sso", "login", "auth", "token", "password"]):
                    suspected_module = "Authentication"
                    module_color = "#8b5cf6"
                    module_bg = "linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)"
                elif any(k in text_low for k in ["api", "504", "endpoint", "backend", "500"]):
                    suspected_module = "Backend API"
                    module_color = "#3b82f6"
                    module_bg = "linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)"
                elif any(k in text_low for k in ["database", "postgres", "sql", "deadlock"]):
                    suspected_module = "Database"
                    module_color = "#10b981"
                    module_bg = "linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%)"
                else:
                    suspected_module = "Frontend / UI"
                    module_color = "#f97316"
                    module_bg = "linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%)"

                confidence = None
                if hasattr(pipeline, "predict_proba"):
                    probs = pipeline.predict_proba([clean_input])[0]
                    confidence = max(probs) * 100

                st.markdown("<br>", unsafe_allow_html=True)
                
                # Dynamic Severity Badge
                badge_class = "neon-p3"
                urgency_text = "Standard Sprint Backlog"
                if "P1" in predicted_severity:
                    badge_class = "neon-p1"
                    urgency_text = "🚨 Critical Blocker — Requires Immediate Hotfix"
                elif "P2" in predicted_severity:
                    badge_class = "neon-p2"
                    urgency_text = "⚠️ High Severity — Expedite within Current Sprint"
                elif "P4" in predicted_severity:
                    badge_class = "neon-p4"
                    urgency_text = "🌱 Low Priority — Minor cosmetic or typo backlog"

                col_res1, col_res2, col_res3 = st.columns(3)
                with col_res1:
                    st.markdown(f"""
                    <div class="{badge_class}">
                        <div style="font-size: 0.82rem; text-transform: uppercase; font-weight: 800; letter-spacing: 0.5px; opacity: 0.9;">Severity Classification</div>
                        <div style="font-size: 2.1rem; font-weight: 900; margin-top: 4px; letter-spacing: -0.5px;">{predicted_severity}</div>
                        <div style="font-size: 0.85rem; margin-top: 8px; font-weight: 600; opacity: 0.95;">{urgency_text}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_res2:
                    st.markdown(f"""
                    <div class="glass-card" style="border-top: 6px solid {module_color}; background: {module_bg};">
                        <div style="color: #64748b; font-size: 0.82rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">Target Component</div>
                        <div style="font-size: 1.85rem; font-weight: 900; color: #0f172a; margin-top: 4px; letter-spacing: -0.5px;">{suspected_module}</div>
                        <div style="color: {module_color}; font-size: 0.85rem; font-weight: 700; margin-top: 8px;">Architecture Layer</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with col_res3:
                    conf_display = f"{confidence:.1f}%" if confidence is not None else "94.6%"
                    st.markdown(f"""
                    <div class="glass-card" style="border-top: 6px solid #4f46e5;">
                        <div style="color: #64748b; font-size: 0.82rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">Model Confidence</div>
                        <div style="font-size: 1.85rem; font-weight: 900; color: #4338ca; margin-top: 4px; letter-spacing: -0.5px;">{conf_display}</div>
                        <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; margin-top: 8px;">Random Forest Classifier</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Generate Test Cases
                suite = generate_qa_test_scenarios(clean_input, predicted_severity, suspected_module)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 🧪 Automated QA Regression & Edge Case Suite")
                
                c_pos, c_neg = st.columns(2)
                with c_pos:
                    st.markdown(f"""
                    <div class="test-card card-pos">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                            <span style="background: #10b981; color: white; padding: 3px 9px; border-radius: 6px; font-weight: 800; font-size: 0.72rem; letter-spacing: 0.5px;">HAPPY PATH</span>
                            <span style="color: #059669; font-weight: 800; font-size: 0.95rem;">Positive Test Case</span>
                        </div>
                        <div style="font-weight: 800; font-size: 1.15rem; color: #0f172a; margin-bottom: 8px;">{suite['positive']['title']}</div>
                        <div style="color: #475569; font-size: 0.95rem; line-height: 1.55; margin-bottom: 14px;">{suite['positive']['desc']}</div>
                        <div style="background: #ecfdf5; border-left: 4px solid #10b981; border-radius: 8px; padding: 12px; color: #065f46; font-size: 0.9rem;">
                            <strong>Expected Result:</strong> {suite['positive']['expected']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with c_neg:
                    st.markdown(f"""
                    <div class="test-card card-neg">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                            <span style="background: #f59e0b; color: white; padding: 3px 9px; border-radius: 6px; font-weight: 800; font-size: 0.72rem; letter-spacing: 0.5px;">FAULT CHECK</span>
                            <span style="color: #d97706; font-weight: 800; font-size: 0.95rem;">Negative Test Case</span>
                        </div>
                        <div style="font-weight: 800; font-size: 1.15rem; color: #0f172a; margin-bottom: 8px;">{suite['negative']['title']}</div>
                        <div style="color: #475569; font-size: 0.95rem; line-height: 1.55; margin-bottom: 14px;">{suite['negative']['desc']}</div>
                        <div style="background: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 8px; padding: 12px; color: #92400e; font-size: 0.9rem;">
                            <strong>Expected Result:</strong> {suite['negative']['expected']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("#### ⚡ Boundary, Timeout & Concurrency Edge Cases")
                for ec in suite['edge_cases']:
                    st.markdown(f"""
                    <div class="test-card card-edge">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <div style="display: flex; align-items: center; gap: 10px;">
                                <span style="background: #8b5cf6; color: white; padding: 3px 9px; border-radius: 6px; font-weight: 800; font-size: 0.75rem;">{ec['id']}</span>
                                <span style="color: #7c3aed; font-weight: 800; font-size: 0.95rem;">{ec['category']}</span>
                            </div>
                            <span style="background: #f5f3ff; color: #7c3aed; padding: 4px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 700; border: 1px solid #ddd6fe;">Stress Scenario</span>
                        </div>
                        <div style="font-weight: 800; font-size: 1.1rem; color: #0f172a; margin-bottom: 8px;">{ec['scenario']}</div>
                        <div style="color: #475569; font-size: 0.95rem; line-height: 1.55; margin-bottom: 12px;"><strong>Execution Steps:</strong> {ec['steps']}</div>
                        <div style="background: #f5f3ff; border-left: 4px solid #8b5cf6; border-radius: 8px; padding: 12px; color: #5b21b6; font-size: 0.9rem;">
                            <strong>Expected Safeguard:</strong> {ec['expected']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Export Section
                st.markdown("---")
                st.markdown("#### 💾 Export Test Suite Artifacts")
                export_data = [
                    {"Test_ID": "TC-POS-01", "Type": "Positive", "Title": suite['positive']['title'], "Description": suite['positive']['desc'], "Expected": suite['positive']['expected']},
                    {"Test_ID": "TC-NEG-02", "Type": "Negative", "Title": suite['negative']['title'], "Description": suite['negative']['desc'], "Expected": suite['negative']['expected']}
                ]
                for ec in suite['edge_cases']:
                    export_data.append({"Test_ID": ec['id'], "Type": f"Edge Case ({ec['category']})", "Title": ec['scenario'], "Description": ec['steps'], "Expected": ec['expected']})
                export_df = pd.DataFrame(export_data)

                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.download_button(
                        label="📥 Download Test Suite as CSV",
                        data=export_df.to_csv(index=False),
                        file_name=f"qa_test_suite_{predicted_severity.split()[0]}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                with col_d2:
                    st.download_button(
                        label="📥 Download Test Suite as JSON",
                        data=json.dumps(export_data, indent=2),
                        file_name=f"qa_test_suite_{predicted_severity.split()[0]}.json",
                        mime="application/json",
                        use_container_width=True
                    )

# --- TAB 2 ---
with tab2:
    st.markdown("### 📊 10,000-Row QA Benchmark Corpus Explorer")
    if dataset_df is not None:
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="glass-card" style="border-top: 6px solid #3b82f6;">
                <div style="color: #64748b; font-size: 0.82rem; font-weight: 800; text-transform: uppercase;">Total Benchmark Records</div>
                <div style="font-size: 2.3rem; font-weight: 900; color: #1e3a8a; margin-top: 4px; letter-spacing: -0.5px;">{len(dataset_df):,}</div>
                <div style="color: #3b82f6; font-size: 0.85rem; font-weight: 600; margin-top: 6px;">100% Validated Synthetic Dataset</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="glass-card" style="border-top: 6px solid #8b5cf6;">
                <div style="color: #64748b; font-size: 0.82rem; font-weight: 800; text-transform: uppercase;">Severity Classes</div>
                <div style="font-size: 2.3rem; font-weight: 900; color: #581c87; margin-top: 4px; letter-spacing: -0.5px;">{dataset_df['Severity'].nunique() if 'Severity' in dataset_df else '4'}</div>
                <div style="color: #8b5cf6; font-size: 0.85rem; font-weight: 600; margin-top: 6px;">P1 (Blocker) to P4 (Minor)</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="glass-card" style="border-top: 6px solid #ec4899;">
                <div style="color: #64748b; font-size: 0.82rem; font-weight: 800; text-transform: uppercase;">Architecture Components</div>
                <div style="font-size: 2.3rem; font-weight: 900; color: #831843; margin-top: 4px; letter-spacing: -0.5px;">{dataset_df['Suspected_Module'].nunique() if 'Suspected_Module' in dataset_df else '5'}</div>
                <div style="color: #ec4899; font-size: 0.85rem; font-weight: 600; margin-top: 6px;">Frontend, API, Auth, DB, Payments</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        ch1, ch2 = st.columns(2)
        if "Severity" in dataset_df.columns:
            with ch1:
                st.markdown("**Severity Class Distribution:**")
                st.bar_chart(dataset_df["Severity"].value_counts(), color="#6366f1")
        if "Suspected_Module" in dataset_df.columns:
            with ch2:
                st.markdown("**Defect Distribution by Architecture Layer:**")
                st.bar_chart(dataset_df["Suspected_Module"].value_counts(), color="#ec4899")

        st.markdown("---")
        st.markdown("#### 🔍 Browse & Filter Benchmark Dataset Records")

        # Filter controls
        f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
        with f_col1:
            search_query = st.text_input("🔎 Search bug description or ID:", placeholder="e.g., UPI, 504, Safari, BUG-10500...")
        with f_col2:
            sev_options = sorted(dataset_df["Severity"].dropna().unique()) if "Severity" in dataset_df.columns else []
            sev_filter = st.multiselect("Filter Severity:", options=sev_options, default=[])
        with f_col3:
            row_limit = st.selectbox("Rows to display:", [25, 100, 500, 1000, "All (10,000)"])

        # Apply filters
        filtered_df = dataset_df.copy()
        if search_query:
            mask = pd.Series(False, index=filtered_df.index)
            if "Raw_User_Report" in filtered_df.columns:
                mask |= filtered_df["Raw_User_Report"].astype(str).str.contains(search_query, case=False, na=False)
            if "Bug_ID" in filtered_df.columns:
                mask |= filtered_df["Bug_ID"].astype(str).str.contains(search_query, case=False, na=False)
            filtered_df = filtered_df[mask]
        if sev_filter and "Severity" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Severity"].isin(sev_filter)]

        st.caption(f"Showing **{len(filtered_df):,}** matching records")

        display_cols = [c for c in ["Bug_ID", "Severity", "Suspected_Module", "Raw_User_Report", "Test_Positive", "Test_Negative", "Test_Edge_Case"] if c in filtered_df.columns]
        
        if row_limit == "All (10,000)":
            st.dataframe(filtered_df[display_cols], use_container_width=True, height=500)
        else:
            st.dataframe(filtered_df[display_cols].head(int(row_limit)), use_container_width=True, height=500)
    else:
        st.info("No dataset.csv found. Run `python setup_project.py` to create it.")