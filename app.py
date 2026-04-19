import streamlit as st
from datetime import datetime

# =====================================================
# PAGE CONFIG  — sidebar always expanded
# =====================================================
st.set_page_config(
    page_title="Electricity Management System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION STATE INIT
# =====================================================
for key, val in {
    "page":    "Home",
    "history": [],
    "daily":   13.24,
    "monthly": 397.20,
    "bill":    3177.60,
    "co2":     318.72,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;600;700;800&family=Rajdhani:wght@400;600;700&display=swap');

* { box-sizing: border-box; }

/* ── ELECTRICITY BACKGROUND ── */
.stApp {
    background:
        linear-gradient(180deg,
            rgba(0,4,14,0.82) 0%,
            rgba(1,8,24,0.75) 30%,
            rgba(2,12,34,0.70) 65%,
            rgba(0,4,14,0.88) 100%),
        url("https://images.unsplash.com/photo-1508615039623-a25605d2b022?auto=format&fit=crop&w=1920&q=80");
    background-size: cover;
    background-position: center center;
    background-attachment: fixed;
    font-family: 'Exo 2', sans-serif;
    color: white;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
div[data-testid="stDecoration"] { display: none !important; }

/* ── FORCE SIDEBAR ALWAYS VISIBLE ── */
section[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    width: 260px !important;
    min-width: 260px !important;
    transform: none !important;
    background: linear-gradient(180deg,
        rgba(0,3,12,0.98) 0%,
        rgba(1,8,24,0.98) 50%,
        rgba(2,12,34,0.98) 100%) !important;
    border-right: 1px solid rgba(0,220,80,0.22) !important;
}
section[data-testid="stSidebar"] > div {
    padding: 0 !important;
    overflow-y: auto;
}
section[data-testid="stSidebar"] * { color: white !important; }

/* Hide the sidebar collapse arrow button */
button[data-testid="collapsedControl"],
button[kind="header"] { display: none !important; }

/* ── SIDEBAR NAV RADIO ── */
.stRadio > div { gap: 2px !important; }
.stRadio label {
    border-radius: 10px !important;
    padding: 9px 16px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    transition: background 0.2s !important;
    cursor: pointer !important;
    color: #c0d0e0 !important;
}
.stRadio label:hover {
    background: rgba(0,220,80,0.10) !important;
    color: white !important;
}
.stRadio label[data-checked="true"] {
    background: rgba(0,220,80,0.16) !important;
    border-left: 3px solid #00e676 !important;
    color: white !important;
}

/* ── SIDEBAR QUICK-ACTION BUTTONS ── */
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(0,200,80,0.08) !important;
    border: 1px solid rgba(0,200,80,0.25) !important;
    border-radius: 11px !important;
    color: #00c850 !important;
    font-size: 0.86rem !important;
    font-weight: 600 !important;
    padding: 10px 14px !important;
    text-align: left !important;
    width: 100% !important;
    box-shadow: none !important;
    margin-bottom: 5px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,200,80,0.18) !important;
    box-shadow: none !important;
}

/* ── BLOCK CONTAINER ── */
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── MAIN WRAPPER ── */
.mw { padding: 18px 26px 10px; }

/* ── HEADER BANNER ── */
.hb {
    background: linear-gradient(120deg,
        rgba(0,4,14,0.92) 0%,
        rgba(1,8,24,0.84) 52%,
        rgba(0,25,55,0.60) 100%);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 26px 30px 22px;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
    min-height: 130px;
    backdrop-filter: blur(4px);
}
.hb-bg {
    position: absolute; top:0; right:0; bottom:0; width:44%;
    background: url("https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=800&q=70")
                right center / cover no-repeat;
    opacity: 0.22;
    border-radius: 0 18px 18px 0;
}
.ht {
    font-size: 2.3rem; font-weight: 800; color: white;
    margin-bottom: 5px; position: relative; z-index: 1;
    letter-spacing: 0.3px; text-shadow: 0 2px 18px rgba(0,0,0,0.6);
}
.ht .gr { color: #00e676; }
.hs { font-size: 0.95rem; color: #a0b8cc; position: relative; z-index: 1; margin: 0; }

/* TIME WIDGET */
.tc {
    position: absolute; top: 20px; right: 24px;
    background: rgba(0,0,0,0.55); border: 1px solid rgba(255,255,255,0.15);
    border-radius: 14px; padding: 10px 16px; text-align: right; z-index: 2;
    backdrop-filter: blur(10px);
}
.tc-t { font-size: 1.32rem; font-weight: 700; color: white; line-height:1.1; }
.tc-d { font-size: 0.71rem; color: #90a8bc; margin-bottom: 4px; }
.tc-s { font-size: 0.71rem; color: #00e676; }
.tc-s::before { content: "● "; }

/* FEATURE CARDS ROW */
.fr { display:flex; gap:12px; margin-bottom:18px; }
.fc {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 13px; padding: 12px 16px;
    display: flex; align-items: center; gap: 12px; flex: 1;
    transition: background 0.2s;
}
.fc:hover { background: rgba(255,255,255,0.10); }
.fi { width:36px; height:36px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0; }
.fi-g { background: rgba(0,200,80,0.22); }
.fi-b { background: rgba(0,120,255,0.22); }
.fi-a { background: rgba(255,170,0,0.22); }
.fi-t { background: rgba(0,200,180,0.22); }
.ft { font-size:0.87rem; font-weight:700; color:white; }
.fs { font-size:0.69rem; color:#7a8ea8; }

/* SECTION CARD */
.sc {
    background: rgba(0,4,14,0.80);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px; padding: 20px 22px;
    margin-bottom: 16px; backdrop-filter: blur(14px);
}
.st2 { font-size:1.02rem; font-weight:700; color:white; margin-bottom:16px; display:flex; align-items:center; gap:8px; }

/* APPLIANCE CARD */
.ac2 {
    background: rgba(0,6,18,0.78); border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px; padding: 13px 9px; text-align:center;
    transition: border-color 0.2s; backdrop-filter: blur(8px);
}
.ac2:hover { border-color: rgba(0,220,80,0.38); }
.ae { font-size:1.8rem; margin-bottom:4px; }
.an { font-size:0.79rem; font-weight:600; color:white; margin-bottom:6px; }
.trf { border-color:rgba(255,170,0,0.38) !important; }

/* METRIC GRID */
.mg { display:grid; grid-template-columns:repeat(4,1fr); gap:13px; }
.mc {
    background: rgba(0,6,18,0.78); border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px; padding: 17px; position:relative; overflow:hidden;
    backdrop-filter: blur(8px);
}
.mh { font-size:0.72rem; color:#7a8ea8; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:7px; }
.mv { font-size:1.72rem; font-weight:800; color:white; font-family:'Rajdhani',sans-serif; }
.mu { font-size:0.88rem; font-weight:400; color:#a0b4cc; }
.ml { font-size:0.67rem; color:#3a5060; margin-top:2px; }
.mb { position:absolute; bottom:0; left:0; height:3px; border-radius:0 0 14px 14px; }
.bg2 { background:linear-gradient(90deg,#00c850,#00ff80); width:70%; }
.bb2 { background:linear-gradient(90deg,#0078ff,#00aaff); width:80%; }
.ba2 { background:linear-gradient(90deg,#ffa000,#ffcc00); width:75%; }
.bt2 { background:linear-gradient(90deg,#00bfa5,#00e5cc); width:60%; }

/* TIPS CARD */
.tpc {
    background: rgba(0,4,14,0.80); border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px; padding: 20px; backdrop-filter: blur(14px); height:100%;
}
.ti { display:flex; align-items:flex-start; gap:11px; padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.05); }
.ti:last-child { border-bottom:none; }
.tic { width:32px; height:32px; border-radius:9px; background:rgba(0,200,80,0.10); display:flex; align-items:center; justify-content:center; font-size:14px; flex-shrink:0; }
.tit { font-size:0.84rem; font-weight:600; color:white; }
.tis { font-size:0.69rem; color:#3a5060; }

/* HISTORY TABLE */
.htbl { width:100%; border-collapse:collapse; font-size:0.84rem; }
.htbl th { background:rgba(0,200,80,0.10); color:#00e676; font-weight:600; padding:10px 14px; text-align:left; border-bottom:1px solid rgba(0,200,80,0.20); }
.htbl td { padding:9px 14px; border-bottom:1px solid rgba(255,255,255,0.05); color:#d0e0f0; }
.htbl tr:hover td { background:rgba(255,255,255,0.03); }
.no-hist { text-align:center; color:#3a5060; padding:32px 0; font-size:0.9rem; }

/* SIDEBAR HTML ELEMENTS */
.sbl { padding:22px 18px 15px; border-bottom:1px solid rgba(255,255,255,0.07); margin-bottom:8px; }
.sbi { width:42px; height:42px; background:rgba(0,200,80,0.16); border:1.5px solid rgba(0,200,80,0.45); border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:20px; margin-bottom:8px; }
.sbt  { font-size:0.98rem; font-weight:700; color:white; }
.sbst { font-size:0.70rem; color:#3a5060; }
.nl   { font-size:0.65rem; font-weight:700; letter-spacing:1.5px; color:#1e3040; text-transform:uppercase; padding:12px 18px 4px; }
.esb  { margin:12px 14px 20px; background:rgba(0,200,80,0.08); border:1px solid rgba(0,200,80,0.20); border-radius:13px; padding:13px; }
.esl  { font-size:0.72rem; color:#5a7a70; margin-bottom:3px; }
.esv  { font-size:0.92rem; font-weight:700; color:#00e676; }
.ess  { font-size:0.68rem; color:#3a5050; margin-top:3px; }

/* MAIN CALCULATE BUTTON */
.stButton > button {
    background: linear-gradient(135deg,#5f2dff,#7d42ff) !important;
    color: white !important; font-size:1rem !important; font-weight:700 !important;
    border: none !important; border-radius:14px !important;
    padding:14px 28px !important; width:100% !important;
    box-shadow: 0 4px 20px rgba(95,45,255,0.35) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg,#7040ff,#9060ff) !important;
    box-shadow: 0 6px 26px rgba(95,45,255,0.5) !important;
}

/* INPUTS */
div[data-baseweb="input"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.13) !important;
    border-radius: 10px !important;
}
input[type="number"] { color:white !important; font-weight:600 !important; font-size:1.05rem !important; background:transparent !important; }

/* ALERTS */
.stSuccess > div { background:rgba(0,200,80,0.10) !important; border:1px solid rgba(0,200,80,0.28) !important; color:#00e676 !important; border-radius:12px !important; }
.stInfo    > div { background:rgba(0,100,255,0.10) !important; border:1px solid rgba(0,100,255,0.25) !important; border-radius:12px !important; }

/* FOOTER */
.ftr { text-align:center; font-size:0.77rem; color:#1e3040; padding:18px 0 10px; }

h1,h2,h3,h4,p,label,span { color:white !important; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
now = datetime.now()

# Logo block
st.sidebar.markdown("""
<div class="sbl">
  <div class="sbi">&#9889;</div>
  <div class="sbt">Electricity</div>
  <div class="sbst">Management System</div>
</div>
<div class="nl">Navigation</div>
""", unsafe_allow_html=True)

# Navigation radio — native Streamlit widget (keeps sidebar open)
NAV_OPTIONS = ["Home", "Dashboard", "Prediction", "Recommendation", "History"]
NAV_ICONS   = ["🏠", "📊", "🔮", "🌿", "📋"]
NAV_DISPLAY = [f"{icon}  {label}" for icon, label in zip(NAV_ICONS, NAV_OPTIONS)]

current_idx = NAV_OPTIONS.index(st.session_state["page"]) if st.session_state["page"] in NAV_OPTIONS else 0
nav_choice  = st.sidebar.radio("nav", NAV_DISPLAY, index=current_idx, label_visibility="collapsed", key="nav_radio")
page = nav_choice.split("  ")[1]
st.session_state["page"] = page

# Quick Actions
st.sidebar.markdown('<div class="nl">Quick Actions</div>', unsafe_allow_html=True)

col_a, col_b = st.sidebar.columns([1, 1])
with col_a:
    if st.sidebar.button("🧮  Calculate Bill", key="qa_calc"):
        st.session_state["page"] = "Prediction"
        st.rerun()

with col_b:
    if st.sidebar.button("📋  Usage History", key="qa_hist"):
        st.session_state["page"] = "History"
        st.rerun()

# Energy Status
st.sidebar.markdown("""
<div class="esb">
  <div class="esl">Energy Status</div>
  <div class="esv">&#10022; Normal Usage</div>
  <div class="ess">You are using power efficiently!</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SUBTITLES
# =====================================================
subtitles = {
    "Home":           "Monitor, predict and optimize your electricity usage.",
    "Dashboard":      "Estimated Summary",
    "Prediction":     "Enter Appliance Usage (Average Daily Usage in Hours)",
    "Recommendation": "Energy Saving Tips",
    "History":        "Your Past Bill Calculations",
}

# =====================================================
# HEADER BANNER  — string concat avoids f-string escaping
# =====================================================
d_str = now.strftime("%d %b %Y, %A")
t_str = now.strftime("%I:%M %p")
s_str = subtitles.get(page, "")

st.markdown(
    '<div class="mw">'
    '<div class="hb">'
    '<div class="hb-bg"></div>'
    '<div class="tc">'
    '<div class="tc-d">' + d_str + '</div>'
    '<div class="tc-t">' + t_str + '</div>'
    '<div class="tc-s">System Online</div>'
    '</div>'
    '<div class="ht">&#9889; Electricity <span class="gr">Management</span> System</div>'
    '<div class="hs">' + s_str + '</div>'
    '</div>',
    unsafe_allow_html=True
)

# Feature cards — only on Home, separate call
if page == "Home":
    st.markdown("""
<div class="fr">
  <div class="fc">
    <div class="fi fi-g">&#128101;</div>
    <div><div class="ft">Monitor</div><div class="fs">Track real-time usage</div></div>
  </div>
  <div class="fc">
    <div class="fi fi-b">&#128200;</div>
    <div><div class="ft">Predict</div><div class="fs">Predict future bills</div></div>
  </div>
  <div class="fc">
    <div class="fi fi-a">&#9881;</div>
    <div><div class="ft">Optimize</div><div class="fs">Get smart recommendations</div></div>
  </div>
  <div class="fc">
    <div class="fi fi-t">&#127807;</div>
    <div><div class="ft">Save</div><div class="fs">Save energy &amp; money</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# HOME
# =====================================================
if page == "Home":
    st.markdown("""
<div class="sc">
  <div class="st2">&#127968; Welcome to Electricity Management System</div>
  <p style="color:#8090a8;font-size:0.9rem;line-height:1.8;margin:0;">
    Monitor your appliance usage, predict monthly electricity bills, and get smart
    recommendations to save energy and reduce costs.<br>
    Use the sidebar or quick-action buttons to navigate all features.
  </p>
</div>
""", unsafe_allow_html=True)
    st.info("💡 Use the **Prediction** page for appliance-wise electricity bill calculation.")

# =====================================================
# PREDICTION
# =====================================================
elif page == "Prediction":

    appliances = [
        ("❄️",  "AC",            1.500, "ac",      6),
        ("📺",  "TV",            0.080, "tv",      3),
        ("🌀",  "Fan",           0.075, "fan",    10),
        ("🧊",  "Fridge",        0.200, "fridge", 10),
        ("🫧",  "Wash. Machine", 0.500, "wm",      1),
        ("💡",  "Light",         0.020, "light",   6),
    ]

    st.markdown('<div class="sc"><div class="st2">&#9889; Appliance Usage Input</div>', unsafe_allow_html=True)

    cols = st.columns(7)
    inputs = {}

    for i, (emoji, name, power, key, default) in enumerate(appliances):
        with cols[i]:
            st.markdown(
                '<div class="ac2">'
                '<div class="ae">' + emoji + '</div>'
                '<div class="an">' + name + '</div>'
                '</div>',
                unsafe_allow_html=True
            )
            val = st.number_input("hrs", 0, 24, default, key=key, label_visibility="collapsed")
            st.markdown(
                '<div style="text-align:center;font-size:0.67rem;color:#00c850;margin-top:-4px;">Power: '
                + str(power) + ' kW</div>',
                unsafe_allow_html=True
            )
            inputs[key] = (val, power)

    with cols[6]:
        st.markdown("""
<div class="ac2 trf">
  <div class="ae">&#128176;</div>
  <div class="an">Tariff Rate</div>
</div>""", unsafe_allow_html=True)
        tariff = st.number_input("Rs/unit", 0.0, 20.0, 8.0, key="tariff", label_visibility="collapsed")
        st.markdown('<div style="text-align:center;font-size:0.67rem;color:#ffa000;margin-top:-4px;">Rs / unit</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.write("")

    if st.button("🧮  Calculate Bill"):
        daily_units   = sum(v * p for v, p in inputs.values())
        monthly_units = daily_units * 30
        bill          = monthly_units * tariff
        co2           = monthly_units * 0.82

        st.session_state["daily"]   = daily_units
        st.session_state["monthly"] = monthly_units
        st.session_state["bill"]    = bill
        st.session_state["co2"]     = co2

        record = {
            "time":    now.strftime("%d %b %Y  %I:%M %p"),
            "daily":   f"{daily_units:.2f} kWh",
            "monthly": f"{monthly_units:.2f} kWh",
            "bill":    f"Rs {bill:,.2f}",
            "tariff":  f"Rs {tariff}/unit",
            "co2":     f"{co2:.2f} kg",
        }
        st.session_state["history"].insert(0, record)
        st.success("✅ Calculation done! Open Dashboard to view your summary.")

# =====================================================
# DASHBOARD
# =====================================================
elif page == "Dashboard":

    daily   = st.session_state["daily"]
    monthly = st.session_state["monthly"]
    bill    = st.session_state["bill"]
    co2     = st.session_state["co2"]

    left, right = st.columns([2.8, 1])

    with left:
        st.markdown(
            '<div class="sc">'
            '<div class="st2">&#128202; Estimated Summary</div>'
            '<div class="mg">'

            '<div class="mc"><div class="mh">&#9889; Daily Units</div>'
            '<div class="mv">' + f"{daily:.2f}" + ' <span class="mu">kWh</span></div>'
            '<div class="ml">Total Daily Consumption</div><div class="mb bg2"></div></div>'

            '<div class="mc"><div class="mh">&#128197; Monthly Units</div>'
            '<div class="mv">' + f"{monthly:.2f}" + ' <span class="mu">kWh</span></div>'
            '<div class="ml">Total Monthly Consumption</div><div class="mb bb2"></div></div>'

            '<div class="mc"><div class="mh">&#128176; Estimated Bill</div>'
            '<div class="mv">Rs ' + f"{bill:,.2f}" + '</div>'
            '<div class="ml">Monthly Bill Amount</div><div class="mb ba2"></div></div>'

            '<div class="mc"><div class="mh">&#127807; CO2 Saved</div>'
            '<div class="mv">' + f"{co2:.2f}" + ' <span class="mu">kg</span></div>'
            '<div class="ml">Monthly CO2 Reduction</div><div class="mb bt2"></div></div>'

            '</div></div>',
            unsafe_allow_html=True
        )

    with right:
        st.markdown("""
<div class="tpc">
  <div class="st2">&#128161; Energy Saving Tips</div>
  <div class="ti"><div class="tic">&#10052;</div><div><div class="tit">Set AC to 24&deg;C</div><div class="tis">Save up to 10% on cooling</div></div></div>
  <div class="ti"><div class="tic">&#128161;</div><div><div class="tit">Use LED lights</div><div class="tis">Consumes 80% less energy</div></div></div>
  <div class="ti"><div class="tic">&#128268;</div><div><div class="tit">Unplug appliances</div><div class="tis">Avoid standby power loss</div></div></div>
  <div class="ti"><div class="tic">&#128336;</div><div><div class="tit">Use off-peak hours</div><div class="tis">Save more on electricity bills</div></div></div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# USAGE HISTORY
# =====================================================
elif page == "History":

    history = st.session_state.get("history", [])
    st.markdown('<div class="sc"><div class="st2">&#128203; Usage History</div>', unsafe_allow_html=True)

    if not history:
        st.markdown("""
<div class="no-hist">
  No calculations yet.<br>
  Go to <b style="color:#00e676;">Prediction</b> and click
  <b style="color:#00e676;">Calculate Bill</b> to record your first entry.
</div>
""", unsafe_allow_html=True)
    else:
        rows = ""
        for r in history:
            rows += (
                "<tr><td>" + r['time'] + "</td><td>" + r['daily'] + "</td><td>"
                + r['monthly'] + '</td><td style="color:#ffa000;font-weight:600;">'
                + r['bill'] + "</td><td>" + r['tariff']
                + '</td><td style="color:#00c850;">' + r['co2'] + "</td></tr>"
            )
        st.markdown(
            '<table class="htbl"><thead><tr>'
            '<th>Date &amp; Time</th><th>Daily (kWh)</th><th>Monthly (kWh)</th>'
            '<th>Bill (Rs)</th><th>Tariff</th><th>CO2 (kg)</th>'
            '</tr></thead><tbody>' + rows + '</tbody></table>',
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if history:
        st.write("")
        if st.button("🗑️  Clear History"):
            st.session_state["history"] = []
            st.rerun()

# =====================================================
# RECOMMENDATION
# =====================================================
elif page == "Recommendation":
    st.markdown("""
<div class="sc">
  <div class="st2">&#127807; Energy Saving Tips</div>
  <div class="ti"><div class="tic">&#128161;</div><div><div class="tit">Use LED lights instead of old bulbs</div><div class="tis">LEDs consume up to 80% less energy and last 25x longer</div></div></div>
  <div class="ti"><div class="tic">&#10052;</div><div><div class="tit">Set AC temperature to 24&deg;C</div><div class="tis">Every degree lower increases energy consumption by 6%</div></div></div>
  <div class="ti"><div class="tic">&#128268;</div><div><div class="tit">Turn off appliances when not in use</div><div class="tis">Standby power accounts for up to 10% of your bill</div></div></div>
  <div class="ti"><div class="tic">&#129529;</div><div><div class="tit">Use washing machine with full load</div><div class="tis">Full loads use the same energy as half loads</div></div></div>
  <div class="ti"><div class="tic">&#128336;</div><div><div class="tit">Use off-peak hours for heavy appliances</div><div class="tis">Schedule laundry and dishwashers for nights or weekends</div></div></div>
  <div class="ti"><div class="tic">&#127777;</div><div><div class="tit">Service your AC regularly</div><div class="tis">Clean filters improve efficiency by up to 15%</div></div></div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================
st.markdown(
    '<div class="ftr">Smart Energy Today, Sustainable Tomorrow &#127807;</div></div>',
    unsafe_allow_html=True
)