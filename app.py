import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Emily's Wellness Dashboard", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .metric-card { background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 10px; }
    .metric-title { color: #94a3b8; font-size: 14px; font-weight: bold; text-transform: uppercase; }
    .metric-value { color: #f8fafc; font-size: 24px; font-weight: bold; }
    .coach-card { background-color: #334155; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #10b981;}
    .recommendation-box { background-color: #0f172a; padding: 20px; border-radius: 8px; border: 1px solid #334155; margin-bottom: 20px;}
    .chart-insight { background-color: #1e293b; padding: 12px; border-radius: 6px; border-left: 3px solid #64748b; font-size: 13px; color: #cbd5e1; margin-top: 8px; font-style: italic; }
    
    /* Horizontal navigation bar styling */
    div.row-widget.stRadio > div{
        flex-direction:row;
        justify-content: center;
        background-color: #1e293b;
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. DATA LOADING & GLOBAL CALCULATIONS
# ==========================================
data_path = Path("sic_wellness_emily_park.csv")

if not data_path.exists():
    st.error(f"🚨 File '{data_path.name}' not found.")
    st.stop()

# Load dataset
df_full = pd.read_csv(data_path)
df_full['date'] = pd.to_datetime(df_full['date'])

# Numeric column cleaning
numeric_cols = ['sleep_hours', 'stress_level', 'daily_steps', 'activity_duration_min', 
                'target_sleep_hours', 'target_daily_steps', 'target_activity_duration', 
                'caloric_balance', 'activity_avg_heart_rate', 'resting_heart_rate',
                'age', 'weight_kg', 'height_cm']

for col in numeric_cols:
    if col in df_full.columns:
        if df_full[col].dtype == object:
            df_full[col] = df_full[col].astype(str).str.replace(',', '.')
        df_full[col] = pd.to_numeric(df_full[col], errors='coerce')

# Extract Personal Profile Data
emily_age = int(df_full['age'].dropna().iloc[0]) if 'age' in df_full.columns and not df_full['age'].dropna().empty else "N/A"
emily_weight = df_full['weight_kg'].dropna().iloc[0] if 'weight_kg' in df_full.columns and not df_full['weight_kg'].dropna().empty else "N/A"
emily_height = df_full['height_cm'].dropna().iloc[0] if 'height_cm' in df_full.columns and not df_full['height_cm'].dropna().empty else "N/A"

latest_date = df_full['date'].max()
start_date = latest_date - pd.Timedelta(days=6)
last_7days = df_full[(df_full['date'] >= start_date) & (df_full['date'] <= latest_date)].sort_values('date')

# 7-Day Metric Aggregations
avg_sleep = last_7days['sleep_hours'].mean() if 'sleep_hours' in last_7days.columns else 0
avg_stress = last_7days['stress_level'].mean() if 'stress_level' in last_7days.columns else 0
avg_steps = last_7days['daily_steps'].mean() if 'daily_steps' in last_7days.columns else 0
avg_activity = last_7days['activity_duration_min'].mean() if 'activity_duration_min' in last_7days.columns else 0
total_balance = last_7days['caloric_balance'].sum() if 'caloric_balance' in last_7days.columns else 0

if 'mood' in last_7days.columns:
    if last_7days['mood'].dtype == object or pd.api.types.is_string_dtype(last_7days['mood']):
        mood_mode = last_7days['mood'].mode()
        avg_mood_label = mood_mode.iloc[0] if not mood_mode.empty else "N/A"
    else:
        avg_mood_label = f"{last_7days['mood'].mean():.1f} / 10"
else:
    avg_mood_label = "N/A"

target_sleep = last_7days['target_sleep_hours'].iloc[0] if 'target_sleep_hours' in last_7days.columns else 8
target_steps = last_7days['target_daily_steps'].iloc[0] if 'target_daily_steps' in last_7days.columns else 10000
target_activity = last_7days['target_activity_duration'].iloc[0] if 'target_activity_duration' in last_7days.columns else 30

# Stress Status Mapping
if avg_stress <= 3:
    stress_label, stress_color = "Low 🟢", "#10b981"
elif avg_stress <= 6:
    stress_label, stress_color = "Moderate 🟡", "#f59e0b"
elif avg_stress <= 8:
    stress_label, stress_color = "High 🟠", "#f97316"
else:
    stress_label, stress_color = "Very High 🔴", "#ef4444"

# ==========================================
# NAVIGATION HEADER
# ==========================================
st.title("⚡ Emily's Wellness Dashboard")

# Personal Data Banner
st.markdown(f"""
<div style='color: #cbd5e1; font-size: 16px; margin-top: -10px; margin-bottom: 20px; padding-left: 5px;'>
    <b>👤 Age:</b> {emily_age} years &nbsp;&nbsp;|&nbsp;&nbsp; <b>⚖️ Weight:</b> {emily_weight} kg &nbsp;&nbsp;|&nbsp;&nbsp; <b>📏 Height:</b> {emily_height} cm
</div>
""", unsafe_allow_html=True)

menu = st.radio(
    "Navigation",
    ["Overview", "Workout Routine", "Nutrition", "Sleep", "Stress", "History"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

# ==========================================
# VIEW 1: OVERVIEW (PÁGINA PRINCIPAL)
# ==========================================
if menu == "Overview":
    st.subheader("📊 Weekly Summary Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""<div class="metric-card" style="border-left-color: #3b82f6;"><div class="metric-title">😴 Avg Sleep</div><div class="metric-value">{avg_sleep:.1f} hrs</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card" style="border-left-color: {stress_color};"><div class="metric-title">🧠 Avg Stress</div><div class="metric-value">{avg_stress:.1f} <span style="font-size:12px">({stress_label})</span></div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-card" style="border-left-color: #a855f7;"><div class="metric-title">👣 Avg Steps</div><div class="metric-value">{avg_steps:,.0f}</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="metric-card" style="border-left-color: #ec4899;"><div class="metric-title">⏳ Avg Exercise</div><div class="metric-value">{avg_activity:.0f} mins</div></div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f"""<div class="metric-card" style="border-left-color: #14b8a6;"><div class="metric-title">🎭 Average Mood</div><div class="metric-value" style="font-size: 20px;">{avg_mood_label}</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    c_col1, c_col2 = st.columns(2)

    with c_col1:
        st.subheader("🎯 Coaching & Insights")
        st.markdown("""<div class="coach-card">1. Short-term (Sleep/Stress): Try disconnecting from screens 30 minutes before bed.</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="coach-card">2. Short-term (Activity): Excellent daily step volume recorded this week!</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="coach-card" style="border-left-color:#8b5cf6;">3. Long-term (Trend): Your habits show steady consistency compared to your historical baseline.</div>""", unsafe_allow_html=True)

    with c_col2:
        st.subheader("🇺🇸 National Trend Benchmarks")
        benchmark_data = {
            "Health Metric": ["Daily Steps", "Sleep Hours", "Net Balance"],
            "Your Metrics (7D)": [f"{avg_steps:,.0f}", f"{avg_sleep:.1f} hrs", f"{total_balance:+,.0f} kcal"],
            "US 75th Percentile": ["8,500", "7.2 hrs", "+200 kcal"],
            "Status": ["Target Exceeded 🚀", "Below Average ⚠️", "Controlled Deficit 🎯"]
        }
        st.table(pd.DataFrame(benchmark_data).set_index("Health Metric"))

    st.markdown("---")
    st.subheader("📈 Weekly Charts & Insights")

    row1_col1, row1_col2 = st.columns(2)
    x_labels = last_7days['date'].dt.strftime('%m/%d')
    
    with row1_col1:
        st.markdown("**1. Top 3 Exercise Activities**")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        if 'activity_type' in last_7days.columns:
            top3 = last_7days.groupby('activity_type')['activity_duration_min'].sum().nlargest(3).sort_values()
            bars = ax1.barh(top3.index, top3.values, color=['#a78bfa', '#8b5cf6', '#6d28d9'])
            ax1.bar_label(bars, padding=3)
        ax1.set_xlabel("Total Minutes")
        st.pyplot(fig1)
        
        # Chart 1 Insight
        if not top3.empty:
            principal_activity = top3.index[-1]
            st.markdown(f"""<div class="chart-insight">📋 <b>Analysis:</b> Your dominant workout activity this week was <b>{principal_activity}</b>. This reflects a clear focus in your current routine. Consider mixing in active recovery sessions as suggested.</div>""", unsafe_allow_html=True)

    with row1_col2:
        st.markdown("**2. Recent Sleep Patterns**")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.bar(x_labels, last_7days['sleep_hours'], color='#3b82f6', alpha=0.8)
        ax2.axhline(avg_sleep, color='red', linestyle='--', label=f"Avg ({avg_sleep:.1f}h)")
        ax2.set_ylabel("Hours")
        ax2.legend()
        st.pyplot(fig2)
        
        # Chart 2 Insight
        sleep_shortfall = target_sleep - avg_sleep
        if sleep_shortfall > 0:
            msg_sleep = f"You are sleeping an average of <b>{sleep_shortfall:.1f} hours less</b> than your target ({target_sleep}h). Prioritize bedtime consistency to boost cellular recovery."
        else:
            msg_sleep = "Excellent! Your average sleep duration meets or exceeds your set target. Your body is successfully cycling through deep recovery phases."
        st.markdown(f"""<div class="chart-insight">😴 <b>Analysis:</b> {msg_sleep}</div>""", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)

    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.markdown("**3. Daily Steps vs Mood**")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        ax3.bar(x_labels, last_7days['daily_steps'], color='#a855f7', alpha=0.7, label='Steps')
        ax3.set_ylabel("Steps")
        
        if 'mood' in last_7days.columns:
            mood_nums = pd.to_numeric(last_7days['mood'].astype(str).str.extract(r'(\d+)')[0], errors='coerce')
            ax3_twin = ax3.twinx()
            ax3_twin.plot(x_labels, mood_nums, color='#14b8a6', marker='o', linewidth=2, label='Mood')
            ax3_twin.set_ylabel("Mood Score")
            
        fig3.legend(loc="upper center", bbox_to_anchor=(0.5, 0.95), ncol=2, frameon=False)
        st.pyplot(fig3)
        
        # Chart 3 Insight
        st.markdown(f"""<div class="chart-insight">🎭 <b>Analysis:</b> Spikes in daily step counts consistently align with or precede higher mood scores (endorphins at work). Maintaining a high baseline activity stabilizes baseline psychological well-being.</div>""", unsafe_allow_html=True)

    with row2_col2:
        st.markdown("**4. Activity Minutes vs Target**")
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        ax4.plot(x_labels, last_7days['activity_duration_min'], color='#ec4899', marker='o', linewidth=2, label='Actual Minutes')
        ax4.axhline(target_activity, color='red', linestyle='--', label=f'Target ({target_activity} min)')
        ax4.set_ylabel("Minutes")
        ax4.legend(loc="upper left")
        ax4.grid(alpha=0.2)
        st.pyplot(fig4)
        
        # Chart 4 Insight
        days_met = (last_7days['activity_duration_min'] >= target_activity).sum()
        st.markdown(f"""<div class="chart-insight">⏳ <b>Analysis:</b> You achieved your {target_activity}-minute exercise target on <b>{days_met} out of the last 7 days</b>. Keeping active even on low-energy days will help sustain an elevated metabolic rate.</div>""", unsafe_allow_html=True)


# ==========================================
# VIEW 2: WORKOUT ROUTINE
# ==========================================
elif menu == "Workout Routine":
    st.header("🏋️‍♀️ Weekly Training Schedule")
    st.markdown("Based on your physical fatigue indicators and step volume, this is your optimal routine split:")
    
    routine_data = {
        "Day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "Focus Area": ["Strength (Upper Body)", "Light Cardio / Zone 2", "Strength (Lower Body)", "Active Recovery / Yoga", "Full Body HIIT", "Outdoor Walk / Hike", "Full Rest Day"],
        "Duration": ["45 min", "30 min", "45 min", "20 min", "30 min", "60+ min", "0 min"]
    }
    st.table(pd.DataFrame(routine_data).set_index("Day"))

# ==========================================
# VIEW 3: NUTRITION
# ==========================================
elif menu == "Nutrition":
    st.header("🥗 Nutritional Analysis")
    balance_color = "#10b981" if total_balance <= 0 else "#ef4444"
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {balance_color}; width: 50%;">
        <div class="metric-title">Cumulative Weekly Caloric Balance</div>
        <div class="metric-value">{total_balance:+,.0f} kcal</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="recommendation-box">
        <h4>💡 Key Dietary Strategies:</h4>
        <ul>
            <li><b>Prioritize lean protein:</b> Essential for cellular structure and muscle tissue synthesis.</li>
            <li><b>Hydrate ahead of demand:</b> Increase fluid intake on high-intensity and long walking days.</li>
            <li><b>The 80/20 framework:</b> Aim for clean, whole foods 80% of the time, letting you enjoy the remaining 20% stress-free.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# VIEW 4: SLEEP
# ==========================================
elif menu == "Sleep":
    st.header("💤 Sleep Hygiene & Recovery Architecture")
    sleep_color = "#10b981" if avg_sleep >= target_sleep else "#f59e0b"
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {sleep_color}; width: 50%;">
        <div class="metric-title">Average vs Target Duration</div>
        <div class="metric-value">{avg_sleep:.1f} / {target_sleep} hrs</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="recommendation-box">
        <h4>🛠️ Golden Rules for High-Quality Sleep:</h4>
        <ul>
            <li><b>The 3-2-1 Digital Wind-down:</b> No work 3h before bed, no heavy meals 2h before, no screens 1h before.</li>
            <li><b>Thermal Environment:</b> Keep your bedroom ambient temperature between 65°F - 68°F (18°C - 20°C).</li>
            <li><b>Early Morning Sunlight Exposure:</b> Get 15-20 minutes of natural light shortly after waking to set your circadian rhythm.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# VIEW 5: STRESS (TODOS LOS GRÁFICOS DEL MISMO TAMAÑO)
# ==========================================
elif menu == "Stress":
    st.header("🧘‍♀️ Advanced Stress Analytics & Management")
    
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {stress_color}; width: 30%;">
        <div class="metric-title">Average Stress Level (7D)</div>
        <div class="metric-value">{avg_stress:.1f} / 10 <span style="font-size:16px">({stress_label})</span></div>
    </div>
    """, unsafe_allow_html=True)

    dias_recientes = last_7days['date'].dt.strftime('%m/%d')

    st.markdown("### 📊 Weekly Correlation Matrix")
    sc_col1, sc_col2 = st.columns(2)

    with sc_col1:
        st.markdown("**1. Physical Strain Impact: Sleep vs Stress**")
        fig_stress, ax_s1 = plt.subplots(figsize=(6, 3.5))  # Uniform size (6, 3.5)
        ax_s1.plot(dias_recientes, last_7days['sleep_hours'], color='#3b82f6', label='Sleep', marker='o')
        ax_s1.set_ylabel('Sleep Hours', color='#3b82f6')
        
        if 'stress_level' in last_7days.columns:
            ax_s1_twin = ax_s1.twinx()
            ax_s1_twin.plot(dias_recientes, last_7days['stress_level'], color='#f59e0b', label='Stress', marker='x', linestyle='--')
            ax_s1_twin.set_ylabel('Stress Level', color='#f59e0b')
            
        fig_stress.legend(loc="upper right", bbox_to_anchor=(0.95, 0.95), bbox_transform=ax_s1.transAxes)
        ax_s1.grid(alpha=0.1)
        st.pyplot(fig_stress)
        
        # Stress Insight 1
        st.markdown(f"""<div class="chart-insight">🧠 <b>Sleep & Mental Load Analysis:</b> A distinct inverse correlation is present. Sharp drops in sleep duration ({last_7days['sleep_hours'].min():.1f}h) impair frontal lobe executive control, noticeably amplifying perceived daily stress.</div>""", unsafe_allow_html=True)

    with sc_col2:
        st.markdown("**2. Psychological Feedback: Stress vs Mood**")
        if 'stress_level' in last_7days.columns and 'mood' in last_7days.columns:
            fig_sc1, ax_sc1 = plt.subplots(figsize=(6, 3.5))  # Uniform size (6, 3.5)
            ax_sc1.plot(dias_recientes, last_7days['stress_level'], color='#f59e0b', marker='s', label='Stress')
            ax_sc1.set_ylabel('Stress Level', color='#f59e0b')
            
            mood_clean = pd.to_numeric(last_7days['mood'].astype(str).str.extract(r'(\d+)')[0], errors='coerce')
            
            ax_sc1_twin = ax_sc1.twinx()
            ax_sc1_twin.plot(dias_recientes, mood_clean, color='#14b8a6', marker='o', linestyle=':', label='Mood')
            ax_sc1_twin.set_ylabel('Mood Score', color='#14b8a6')
            
            fig_sc1.legend(loc="upper left", bbox_to_anchor=(0.05, 0.95), bbox_transform=ax_sc1.transAxes)
            ax_sc1.grid(alpha=0.1)
            st.pyplot(fig_sc1)
            
            # Stress Insight 2
            st.markdown(f"""<div class="chart-insight">🧠 <b>Emotional Impact Analysis:</b> This chart highlights how emotional stability reacts to strain. When these curves behave like mirror images, it confirms your mental outlook is heavily dependent on maintaining a manageable schedule.</div>""", unsafe_allow_html=True)
        else:
            st.info("Missing Stress or Mood data required for this visual.")

    st.markdown("<br>", unsafe_allow_html=True)
    sc_col3, sc_col4 = st.columns(2)
    
    with sc_col3:
        st.markdown("**3. Stress Buffering: Stress vs Workout Duration**")
        if 'stress_level' in last_7days.columns and 'activity_duration_min' in last_7days.columns:
            fig_sc2, ax_sc2 = plt.subplots(figsize=(6, 3.5))  # Uniform size (6, 3.5)
            ax_sc2.bar(dias_recientes, last_7days['activity_duration_min'], color='#ec4899', alpha=0.4, label='Exercise Mins')
            ax_sc2.set_ylabel('Activity Duration (Min)', color='#ec4899')
            
            ax_sc2_twin = ax_sc2.twinx()
            ax_sc2_twin.plot(dias_recientes, last_7days['stress_level'], color='#f59e0b', marker='x', linewidth=2, label='Stress')
            ax_sc2_twin.set_ylabel('Stress Level', color='#f59e0b')
            
            fig_sc2.legend(loc="upper right", bbox_to_anchor=(0.95, 0.95), bbox_transform=ax_sc2.transAxes)
            ax_sc2.grid(alpha=0.1)
            st.pyplot(fig_sc2)
            
            # Stress Insight 3
            st.markdown(f"""<div class="chart-insight">🏃‍♀️ <b>Cortisol Clearance Analysis:</b> Pay close attention to whether sessions extending past 45 minutes lead to lower stress trends over the following 24 hours. Physical activity acts as an excellent flush for systemic stress hormones.</div>""", unsafe_allow_html=True)

    with sc_col4:
        st.markdown("**4. Autonomic Biomarker: Stress vs Resting Heart Rate (RHR)**")
        if 'stress_level' in last_7days.columns and 'resting_heart_rate' in last_7days.columns:
            fig_sc3, ax_sc3 = plt.subplots(figsize=(6, 3.5))  # Uniform size (6, 3.5)
            ax_sc3.plot(dias_recientes, last_7days['resting_heart_rate'], color='#10b981', marker='v', label='RHR')
            ax_sc3.set_ylabel('Resting Heart Rate (BPM)', color='#10b981')
            
            ax_sc3_twin = ax_sc3.twinx()
            ax_sc3_twin.plot(dias_recientes, last_7days['stress_level'], color='#f59e0b', marker='o', linestyle='-.', label='Stress')
            ax_sc3_twin.set_ylabel('Stress Level', color='#f59e0b')
            
            fig_sc3.legend(loc="upper center", bbox_to_anchor=(0.5, 0.95), bbox_transform=ax_sc3.transAxes, ncol=2)
            ax_sc3.grid(alpha=0.1)
            st.pyplot(fig_sc3)
            
            # Stress Insight 4
            avg_rhr = last_7days['resting_heart_rate'].mean()
            st.markdown(f"""<div class="chart-insight">💓 <b>Nervous System Analysis:</b> Your baseline RHR is averaging <b>{avg_rhr:.0f} BPM</b>. Concurrent climbs in both heart rate and subjective stress signify sympathetic (fight-or-flight) dominance. Prioritize low-intensity walks if this occurs.</div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div class="recommendation-box">
        <h4>🔍 Interpreting These Correlations:</h4>
        <ul>
            <li><b>Stress vs Mood:</b> Elevated strain usually dampens your mood score. A strong mirror pattern across these indicators is perfectly typical.</li>
            <li><b>Stress vs Exercise:</b> Training functions as a powerful adaptive buffer. Verify if higher exertion days effectively damp down subsequent stress spikes.</li>
            <li><b>Stress vs Resting Heart Rate (RHR):</b> If your resting pulse rises alongside your stress metrics, your nervous system is signaling a need for active recovery.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# VIEW 6: MONTHLY HISTORY (HISTORIAL)
# ==========================================
elif menu == "History":
    st.header("📚 Monthly Historical Data Records")
    st.markdown("Select a target month to audit granular trends and metrics across past tracking cycles.")
    
    df_full['Month'] = df_full['date'].dt.strftime('%Y-%m')
    available_months = sorted(df_full['Month'].unique(), reverse=True)
    selected_month = st.selectbox("📅 Choose Month:", available_months)
    
    df_mes = df_full[df_full['Month'] == selected_month].sort_values('date').copy()
    
    history_cols = ['activity_avg_heart_rate', 'resting_heart_rate', 'sleep_hours', 'stress_level', 'daily_steps', 'caloric_balance']
    for h_col in history_cols:
        if h_col in df_mes.columns:
            if df_mes[h_col].dtype == object:
                df_mes[h_col] = df_mes[h_col].astype(str).str.replace(',', '.')
            df_mes[h_col] = pd.to_numeric(df_mes[h_col], errors='coerce')
    
    target_columns = ['date', 'sleep_hours', 'activity_type', 'activity_avg_heart_rate', 
                      'resting_heart_rate', 'stress_level', 'daily_steps', 'caloric_balance']
    
    display_columns = [col for col in target_columns if col in df_mes.columns]
    
    df_history = df_mes[display_columns].copy()
    df_history.columns = [col.replace('_', ' ').title() for col in df_history.columns]
    
    st.dataframe(df_history.set_index('Date'), use_container_width=True)
    
    st.markdown("---")
    st.subheader(f"📈 Segregated Trends for {selected_month}")
    
    h_col1, h_col2 = st.columns(2)
    with h_col1:
        st.markdown("**Sleep Hours**")
        fig_m1, ax_m1 = plt.subplots(figsize=(6, 3))
        valid_data = df_mes[['date', 'sleep_hours']].dropna()
        if not valid_data.empty:
            ax_m1.plot(valid_data['date'].dt.strftime('%d'), valid_data['sleep_hours'], color='#3b82f6', marker='o', markersize=4)
        ax_m1.set_ylabel("Hours")
        ax_m1.grid(alpha=0.2)
        st.pyplot(fig_m1)
        
        # History Insight 1
        m_sleep = valid_data['sleep_hours'].mean() if not valid_data.empty else 0
        st.markdown(f"""<div class="chart-insight">😴 <b>Monthly Sleep Summary:</b> Your baseline average is <b>{m_sleep:.1f}h</b> per night. Cross-reference severe valleys to evaluate if certain recurring days of the week introduce sleep deprivation.</div>""", unsafe_allow_html=True)
        
    with h_col2:
        st.markdown("**Stress Level**")
        if 'stress_level' in df_mes.columns:
            fig_m2, ax_m2 = plt.subplots(figsize=(6, 3))
            valid_data = df_mes[['date', 'stress_level']].dropna()
            if not valid_data.empty:
                ax_m2.plot(valid_data['date'].dt.strftime('%d'), valid_data['stress_level'], color='#f59e0b', marker='x', markersize=4)
            ax_m2.set_ylabel("Score (1-10)")
            ax_m2.grid(alpha=0.2)
            st.pyplot(fig_m2)
            
            # History Insight 2
            m_stress = valid_data['stress_level'].mean() if not valid_data.empty else 0
            st.markdown(f"""<div class="chart-insight">🧠 <b>Monthly Stress Summary:</b> Average psychological load sat at <b>{m_stress:.1f}/10</b>. Highly cyclical spikes often point to heavy recurring project deliverables or scheduling friction.</div>""", unsafe_allow_html=True)

    h_col3, h_col4 = st.columns(2)
    with h_col3:
        st.markdown("**Resting Heart Rate (RHR)**")
        if 'resting_heart_rate' in df_mes.columns:
            fig_m3, ax_m3 = plt.subplots(figsize=(6, 3))
            valid_data = df_mes[['date', 'resting_heart_rate']].dropna()
            if not valid_data.empty:
                ax_m3.plot(valid_data['date'].dt.strftime('%d'), valid_data['resting_heart_rate'], color='#10b981', marker='v', markersize=4)
            else:
                ax_m3.text(0.5, 0.5, 'No data logs found', ha='center', va='center', color='gray')
            ax_m3.set_ylabel("BPM")
            ax_m3.grid(alpha=0.2)
            st.pyplot(fig_m3)
            
            # History Insight 3
            m_rhr = valid_data['resting_heart_rate'].mean() if not valid_data.empty else 0
            st.markdown(f"""<div class="chart-insight">💓 <b>Monthly Biometric Summary:</b> RHR averaged <b>{m_rhr:.0f} BPM</b>. A stable or descending baseline trend over multi-month blocks serves as direct confirmation of enhanced cardiovascular conditioning.</div>""", unsafe_allow_html=True)
            
    with h_col4:
        st.markdown("**Workout Heart Rate (Active)**")
        if 'activity_avg_heart_rate' in df_mes.columns:
            fig_m4, ax_m4 = plt.subplots(figsize=(6, 3))
            valid_data_hr = df_mes[['date', 'activity_avg_heart_rate']].dropna()
            valid_data_hr = valid_data_hr[valid_data_hr['activity_avg_heart_rate'] > 0]
            
            if not valid_data_hr.empty:
                ax_m4.scatter(valid_data_hr['date'].dt.strftime('%d'), valid_data_hr['activity_avg_heart_rate'], color='#ef4444', s=50, marker='o', zorder=3)
                ax_m4.plot(valid_data_hr['date'].dt.strftime('%d'), valid_data_hr['activity_avg_heart_rate'], color='#ef4444', linestyle='--', alpha=0.5, zorder=2)
                ax_m4.set_ylim(valid_data_hr['activity_avg_heart_rate'].min() - 5, valid_data_hr['activity_avg_heart_rate'].max() + 5)
            else:
                ax_m4.text(0.5, 0.5, 'No active entries logged this month', ha='center', va='center', color='gray')
            ax_m4.set_ylabel("BPM")
            ax_m4.grid(alpha=0.2)
            st.pyplot(fig_m4)
            
            # History Insight 4
            m_ahr = valid_data_hr['activity_avg_heart_rate'].mean() if not valid_data_hr.empty else 0
            st.markdown(f"""<div class="chart-insight">🔥 <b>Monthly Intensity Summary:</b> Mean training pulse registered at <b>{m_ahr:.0f} BPM</b>. This anchors most sessions neatly inside your aerobic training zone, ideal for sustaining stamina and fat oxidation.</div>""", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Column 'activity_avg_heart_rate' not discovered in dataset.")

    h_col5, h_col6 = st.columns(2)
    with h_col5:
        st.markdown("**Daily Step Volume**")
        fig_m5, ax_m5 = plt.subplots(figsize=(6, 3))
        valid_data = df_mes[['date', 'daily_steps']].dropna()
        if not valid_data.empty:
            ax_m5.bar(valid_data['date'].dt.strftime('%d'), valid_data['daily_steps'], color='#a855f7', alpha=0.7)
        ax_m5.set_ylabel("Steps")
        ax_m5.grid(alpha=0.2, axis='y')
        st.pyplot(fig_m5)
        
        # History Insight 5
        m_steps = valid_data['daily_steps'].mean() if not valid_data.empty else 0
        st.markdown(f"""<div class="chart-insight">👣 <b>Monthly Step Summary:</b> Moving at an average of <b>{m_steps:,.0f} steps per day</b>. Avoiding drastic step valles protects your base metabolic output and non-exercise movement targets.</div>""", unsafe_allow_html=True)
        
    with h_col6:
        st.markdown("**Net Caloric Balance**")
        if 'caloric_balance' in df_mes.columns:
            fig_m6, ax_m6 = plt.subplots(figsize=(6, 3))
            valid_data = df_mes[['date', 'caloric_balance']].dropna()
            if not valid_data.empty:
                colors = ['#10b981' if x >= 0 else '#ef4444' for x in valid_data['caloric_balance']]
                ax_m6.bar(valid_data['date'].dt.strftime('%d'), valid_data['caloric_balance'], color=colors, alpha=0.8)
                ax_m6.axhline(0, color='black', linewidth=0.8)
            ax_m6.set_ylabel("Kcal")
            ax_m6.grid(alpha=0.2, axis='y')
            st.pyplot(fig_m6)
            
            # History Insight 6
            m_cal = valid_data['caloric_balance'].sum() if not valid_data.empty else 0
            st.markdown(f"""<div class="chart-insight">🥗 <b>Monthly Caloric Summary:</b> Net balance closed at <b>{m_cal:+,.0f} kcal</b>. Red bars indicate negative energetic balances, aligning perfectly with standard recomposition or cutting protocol phases.</div>""", unsafe_allow_html=True)