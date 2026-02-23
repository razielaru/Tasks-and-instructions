import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from io import BytesIO
import json

# Load environment variables
load_dotenv()

# ====== Supabase Configuration ======
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("❌ משתני הסביבה של Supabase לא מוגדרים!")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ====== Page Config ======
st.set_page_config(
    page_title="Command Center - אוגדה",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== Hebrew CSS & Auto-Refresh ======
st.markdown("""
<style>
    * {
        font-family: 'Heebo', 'Segoe UI', sans-serif;
        direction: rtl;
    }
    
    .main {
        direction: rtl;
    }
    
    .header-main {
        background: linear-gradient(135deg, #4E5A37 0%, #7B8A62 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .brigade-card {
        border-left: 5px solid;
        padding: 15px;
        border-radius: 8px;
        background: white;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .status-critical {
        border-left-color: #ff4444;
        background-color: #fff0f0;
    }
    
    .status-warning {
        border-left-color: #ff9800;
        background-color: #fff8f0;
    }
    
    .status-good {
        border-left-color: #4CAF50;
        background-color: #f0fff0;
    }
    
    .task-critical {
        background: #ffebee;
        border-right: 3px solid #ff4444;
    }
    
    .task-high {
        background: #fff3e0;
        border-right: 3px solid #ff9800;
    }
    
    .task-normal {
        background: #f5f5f5;
        border-right: 3px solid #2196F3;
    }
    
    .metric-box {
        text-align: center;
        padding: 15px;
        border-radius: 8px;
        background: linear-gradient(135deg, #4E5A37 0%, #7B8A62 100%);
        color: white;
        margin: 5px;
    }
    
    .urgent-banner {
        background: #ff4444;
        color: white;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 1.2em;
        font-weight: bold;
    }
</style>

<meta http-equiv="refresh" content="60">
""", unsafe_allow_html=True)

# ====== Brigade Names ======
BRIGADES = [
    "חטמ״ר בנימין",
    "חטמ״ר שומרון",
    "חטמ״ר אפרים",
    "חטמ״ר עציון",
    "חטמ״ר יהודה",
    "חטמ״ר מנשה"
]

# ====== Database Functions ======
def get_all_tasks():
    """Get all tasks from Supabase"""
    try:
        response = supabase.table("tasks").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"❌ שגיאה בטעינת משימות: {str(e)}")
        return []

def get_brigade_tasks(brigade: str):
    """Get tasks for specific brigade"""
    try:
        response = supabase.table("tasks").select("*").eq("brigade", brigade).execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"❌ שגיאה: {str(e)}")
        return []

def add_task(title: str, description: str, brigade: str, deadline: str, priority: str):
    """Add new task"""
    try:
        task_data = {
            "title": title,
            "description": description,
            "brigade": brigade,
            "deadline": deadline,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat(),
        }
        
        response = supabase.table("tasks").insert(task_data).execute()
        
        if response.data:
            st.success(f"✅ משימה '{title}' נוספה!")
            st.rerun()
            return True
        else:
            st.error("❌ שגיאה בהוספת משימה")
            return False
            
    except Exception as e:
        st.error(f"❌ שגיאה: {str(e)}")
        return False

def update_task(task_id: int, **kwargs):
    """Update task"""
    try:
        response = supabase.table("tasks").update(kwargs).eq("id", task_id).execute()
        if response.data:
            st.rerun()
            return True
        else:
            st.error("❌ שגיאה בעדכון")
            return False
    except Exception as e:
        st.error(f"❌ שגיאה: {str(e)}")
        return False

def delete_task(task_id: int):
    """Delete task"""
    try:
        response = supabase.table("tasks").delete().eq("id", task_id).execute()
        st.success("✅ משימה נמחקה!")
        st.rerun()
        return True
    except Exception as e:
        st.error(f"❌ שגיאה: {str(e)}")
        return False

def toggle_task(task_id: int, current_status: bool):
    """Toggle task completion"""
    new_status = not current_status
    completed_at = datetime.now().isoformat() if new_status else None
    return update_task(task_id, completed=new_status, completed_at=completed_at)

# ====== Analytics Functions ======
def calculate_stats(tasks):
    """Calculate overall statistics"""
    total = len(tasks)
    completed = len([t for t in tasks if t.get("completed")])
    pending = total - completed
    overdue = len([t for t in tasks 
                   if not t.get("completed") and t.get("deadline") and 
                   datetime.fromisoformat(t["deadline"]).date() < datetime.now().date()])
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue,
        "percentage": round((completed / total * 100) if total > 0 else 0, 1)
    }

def get_brigade_stats(tasks):
    """Get stats by brigade"""
    stats = {}
    
    for brigade in BRIGADES:
        brigade_tasks = [t for t in tasks if t.get("brigade") == brigade]
        completed = len([t for t in brigade_tasks if t.get("completed")])
        total = len(brigade_tasks)
        overdue = len([t for t in brigade_tasks 
                      if not t.get("completed") and t.get("deadline") and 
                      datetime.fromisoformat(t["deadline"]).date() < datetime.now().date()])
        
        stats[brigade] = {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "overdue": overdue,
            "percentage": round((completed / total * 100) if total > 0 else 0, 1)
        }
    
    return stats

def get_critical_tasks(tasks):
    """Get critical/overdue tasks"""
    critical = []
    
    for task in tasks:
        if task.get("completed"):
            continue
        
        # High priority + overdue = CRITICAL
        if task.get("priority") == "critical":
            critical.append(("critical", task))
        elif task.get("priority") == "high" and task.get("deadline"):
            if datetime.fromisoformat(task["deadline"]).date() < datetime.now().date():
                critical.append(("critical", task))
        # Overdue = WARNING
        elif task.get("deadline"):
            if datetime.fromisoformat(task["deadline"]).date() < datetime.now().date():
                critical.append(("warning", task))
    
    return sorted(critical, key=lambda x: x[1].get("deadline", "9999-12-31"))

# ====== Export Functions ======
def export_to_excel(tasks):
    """Export tasks to Excel"""
    df = pd.DataFrame(tasks)
    
    # Format for Excel
    if not df.empty:
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d')
        df['deadline'] = pd.to_datetime(df['deadline']).dt.strftime('%Y-%m-%d')
        df['completed'] = df['completed'].map({True: 'כן', False: 'לא'})
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='משימות')
    
    output.seek(0)
    return output.getvalue()

def export_to_csv(tasks):
    """Export tasks to CSV"""
    df = pd.DataFrame(tasks)
    
    if not df.empty:
        df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d')
        df['deadline'] = pd.to_datetime(df['deadline']).dt.strftime('%Y-%m-%d')
        df['completed'] = df['completed'].map({True: 'כן', False: 'לא'})
    
    return df.to_csv(index=False).encode('utf-8-sig')

def generate_whatsapp_report(tasks, brigade_stats):
    """Generate WhatsApp-friendly report"""
    report = f"""
🎖️ דוח שבועי - אוגדה {datetime.now().strftime('%d.%m.%Y')}

📊 תמונת מצב כללית:
───────────────────
סך הכל משימות: {len(tasks)}
הושלמו: {len([t for t in tasks if t.get('completed')])}
בתהליך: {len([t for t in tasks if not t.get('completed')])}
באיחור: {len([t for t in tasks if not t.get('completed') and t.get('deadline') and datetime.fromisoformat(t['deadline']).date() < datetime.now().date()])}

📈 פירוט לפי חטמ"ר:
───────────────────
"""
    
    for brigade, stats in brigade_stats.items():
        brigade_short = brigade.replace("חטמ״ר ", "")
        report += f"\n{brigade_short}:"
        report += f"\n  הושלמו: {stats['completed']}/{stats['total']} ({stats['percentage']}%)"
        if stats['overdue'] > 0:
            report += f"\n  ⚠️ באיחור: {stats['overdue']}"
    
    report += f"\n\n✅ דוח זה נוצר ב-{datetime.now().strftime('%H:%M')} ביום {datetime.now().strftime('%d.%m.%Y')}"
    
    return report

# ====== Main App ======
def main():
    # Header
    st.markdown("""
    <div class="header-main">
        <h1>🎖️ Command Center - מערכת בקרה אוגדתית</h1>
        <p>עקוב אחרי משימות בזמן אמת | עדכונים אוטומטיים כל 60 שניות</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all tasks
    all_tasks = get_all_tasks()
    overall_stats = calculate_stats(all_tasks)
    brigade_stats = get_brigade_stats(all_tasks)
    critical_tasks = get_critical_tasks(all_tasks)
    
    # ====== CRITICAL ALERTS ======
    if critical_tasks:
        st.markdown('<div class="urgent-banner">⚠️ יש משימות קריטיות באיחור!</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("🔴 קריטיות", len([t for t, s in critical_tasks if s == "critical"]))
        with col2:
            for severity, task in critical_tasks[:3]:  # Show top 3
                emoji = "🔴" if severity == "critical" else "🟠"
                st.warning(f"{emoji} **{task['title']}** ({task['brigade']})")
    
    # ====== DASHBOARD METRICS ======
    st.markdown("## 📊 תמונת מצב כללית")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-box">
            <h3>סך הכל</h3>
            <h2>{overall_stats['total']}</h2>
            משימות
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #4CAF50 0%, #66BB6A 100%);">
            <h3>✅ הושלמו</h3>
            <h2>{overall_stats['completed']}</h2>
            {overall_stats['percentage']}%
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #2196F3 0%, #42A5F5 100%);">
            <h3>⏳ בתהליך</h3>
            <h2>{overall_stats['pending']}</h2>
            משימות
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #FF9800 0%, #FFB74D 100%);">
            <h3>⚠️ קרוב לדדליין</h3>
            <h2>{len([t for t in all_tasks if not t.get('completed') and t.get('deadline') and (datetime.fromisoformat(t['deadline']).date() - datetime.now().date()).days <= 3])}</h2>
            משימות
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-box" style="background: linear-gradient(135deg, #F44336 0%, #EF5350 100%);">
            <h3>❌ באיחור</h3>
            <h2>{overall_stats['overdue']}</h2>
            משימות
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ====== PROGRESS VISUALIZATION ======
    st.markdown("## 📈 אחוז השלמה כללי")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = go.Figure(data=[go.Pie(
            labels=["הושלמו", "בתהליך"],
            values=[overall_stats["completed"], overall_stats["pending"]],
            hole=0.6,
            marker=dict(colors=["#4CAF50", "#e5e7eb"]),
            textinfo="label+percent"
        )])
        
        fig.update_layout(height=400, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 40px 20px;">
            <h1 style="color: #4E5A37; font-size: 3em;">{overall_stats['percentage']}%</h1>
            <p style="color: #666; font-size: 1.1em;">השלמה כללית</p>
            <p style="color: #999;">{overall_stats['completed']} מתוך {overall_stats['total']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ====== BRIGADE BREAKDOWN ======
    st.markdown("## 🏘️ מצב לפי חטמ״ר")
    
    # Create 2 columns for brigades
    cols = st.columns(2)
    
    for idx, (brigade, stats) in enumerate(brigade_stats.items()):
        with cols[idx % 2]:
            # Determine status color
            if stats['overdue'] > 0:
                status_class = "status-critical"
                status_emoji = "🔴"
            elif stats['percentage'] < 50:
                status_class = "status-warning"
                status_emoji = "🟠"
            else:
                status_class = "status-good"
                status_emoji = "🟢"
            
            brigade_short = brigade.replace("חטמ״ר ", "")
            
            st.markdown(f"""
            <div class="brigade-card {status_class}">
                <h3>{status_emoji} {brigade}</h3>
                <p><strong>הושלמו:</strong> {stats['completed']}/{stats['total']} ({stats['percentage']}%)</p>
                <p><strong>בתהליך:</strong> {stats['pending']}</p>
                {"<p style='color: red;'><strong>⚠️ באיחור:</strong> " + str(stats['overdue']) + "</p>" if stats['overdue'] > 0 else ""}
                <div style="background: #e0e0e0; height: 8px; border-radius: 5px; margin-top: 10px;">
                    <div style="background: #4E5A37; height: 100%; width: {stats['percentage']}%; border-radius: 5px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # ====== TASKS BY BRIGADE ======
    st.markdown("## 📝 משימות פעילות")
    
    selected_brigade = st.selectbox("בחר חטמ״ר לצפייה בפרטים", ["הכל"] + BRIGADES)
    
    if selected_brigade == "הכל":
        display_tasks = [t for t in all_tasks if not t.get("completed")]
    else:
        display_tasks = [t for t in all_tasks if t.get("brigade") == selected_brigade and not t.get("completed")]
    
    # Sort by priority and deadline
    priority_order = {"critical": 0, "high": 1, "normal": 2}
    display_tasks.sort(key=lambda x: (
        priority_order.get(x.get("priority", "normal"), 2),
        x.get("deadline", "9999-12-31")
    ))
    
    if not display_tasks:
        st.info("✅ אין משימות פעילות!")
    else:
        for task in display_tasks:
            priority_class = f"task-{task.get('priority', 'normal')}"
            priority_emoji = {"critical": "🔴", "high": "🟠", "normal": "⚪"}.get(task.get("priority", "normal"), "⚪")
            
            col1, col2, col3, col4, col5 = st.columns([0.5, 3, 1.5, 1, 0.5])
            
            with col1:
                if st.checkbox("✓", value=False, key=f"check_{task['id']}"):
                    toggle_task(task['id'], False)
            
            with col2:
                st.markdown(f"**{task['title']}** {priority_emoji}")
                if task.get("description"):
                    st.caption(task['description'])
            
            with col3:
                if task.get("deadline"):
                    deadline_date = datetime.fromisoformat(task["deadline"]).date()
                    days_left = (deadline_date - datetime.now().date()).days
                    if days_left < 0:
                        st.caption(f"📅 באיחור {abs(days_left)} ימים")
                    else:
                        st.caption(f"📅 {days_left} ימים")
            
            with col4:
                st.caption(f"{task['brigade'].replace('חטמ״ר ', '')}")
            
            with col5:
                if st.button("🗑️", key=f"del_{task['id']}"):
                    delete_task(task['id'])
    
    st.divider()
    
    # ====== ADD TASK SECTION ======
    st.markdown("## ➕ הוסף משימה חדשה")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_brigade = st.selectbox("בחר חטמ״ר", BRIGADES, key="add_brigade")
    
    with col2:
        new_title = st.text_input("כותרת משימה", key="add_title")
    
    with col3:
        new_priority = st.selectbox("עדיפות", ["normal", "high", "critical"], 
                                    format_func=lambda x: {"normal": "🔵 רגילה", "high": "🟠 גבוהה", "critical": "🔴 קריטית"}[x],
                                    key="add_priority")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_deadline = st.date_input("דדליין", key="add_deadline")
    
    with col2:
        new_desc = st.text_input("תיאור קצר", key="add_desc")
    
    with col3:
        if st.button("➕ הוסף משימה", use_container_width=True):
            if new_title:
                add_task(new_title, new_desc, new_brigade, new_deadline.isoformat(), new_priority)
            else:
                st.error("❌ נא להזין כותרת!")
    
    st.divider()
    
    # ====== EXPORT SECTION ======
    st.markdown("## 📤 ייצוא דוחות")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        excel_data = export_to_excel(all_tasks)
        st.download_button(
            label="📊 הורד Excel",
            data=excel_data,
            file_name=f"tasks_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col2:
        csv_data = export_to_csv(all_tasks)
        st.download_button(
            label="📋 הורד CSV",
            data=csv_data,
            file_name=f"tasks_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col3:
        whatsapp_report = generate_whatsapp_report(all_tasks, brigade_stats)
        st.download_button(
            label="💬 דוח WhatsApp",
            data=whatsapp_report,
            file_name=f"report_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
    
    with col4:
        if st.button("📤 העתק דוח"):
            st.info("📌 העתק ידנית מהתיבה מתחת:")
            st.text_area("דוח השבוע", value=whatsapp_report, height=200, disabled=True)
    
    st.divider()
    
    # ====== INFO FOOTER ======
    st.markdown("""
    ---
    
    📌 **עידכונים אוטומטיים:** הדף מתרענן כל 60 שניות  
    🔄 **רענן ידני:** לחץ F5 או כפתור הרענן בדפדפן  
    💾 **גיבוי נתונים:** כל הנתונים שמורים ב-Supabase  
    
    **Command Center עבור רבנות אוגדה**
    """)

if __name__ == "__main__":
    main()
