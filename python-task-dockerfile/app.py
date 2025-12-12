import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import os

# Page configuration
st.set_page_config(
    page_title="Colorful Task Manager",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #FFE66D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
    }
    .task-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid;
    }
    .high-priority {
        border-left-color: #FF6B6B !important;
    }
    .medium-priority {
        border-left-color: #FFE66D !important;
    }
    .low-priority {
        border-left-color: #4ECDC4 !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
    }
</style>
""", unsafe_allow_html=True)

class TaskManager:
    def __init__(self):
        self.tasks_file = "tasks.json"
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_tasks(self):
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

# Initialize session state
if 'task_manager' not in st.session_state:
    st.session_state.task_manager = TaskManager()

# Header
st.markdown('<h1 class="main-header">🎨 Colorful Task Manager</h1>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Tasks", "➕ Add Task", "📊 Dashboard", "⚙️ Settings"])

with tab1:
    st.header("Your Tasks")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        filter_status = st.selectbox("Filter by Status", ["All", "Active", "Completed"])
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    
    # Display tasks
    for task in st.session_state.task_manager.tasks:
        if filter_status != "All":
            if filter_status == "Active" and task['completed']:
                continue
            elif filter_status == "Completed" and not task['completed']:
                continue
        
        if filter_priority != "All" and task['priority'] != filter_priority:
            continue
        
        # Determine priority class
        priority_class = {
            "High": "high-priority",
            "Medium": "medium-priority",
            "Low": "low-priority"
        }[task['priority']]
        
        # Create task card
        with st.container():
            st.markdown(f'<div class="task-card {priority_class}">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 3, 2])
            with col1:
                if st.button(f"{'✅' if task['completed'] else '⬜'}", key=f"check_{task['id']}"):
                    task['completed'] = not task['completed']
                    st.session_state.task_manager.save_tasks()
                    st.rerun()
            
            with col2:
                st.subheader(task['title'])
                st.caption(task['description'])
            
            with col3:
                st.markdown(f"**Priority:** {task['priority']}")
                st.markdown(f"**Category:** {task['category']}")
                if st.button("🗑️", key=f"delete_{task['id']}"):
                    st.session_state.task_manager.tasks = [
                        t for t in st.session_state.task_manager.tasks 
                        if t['id'] != task['id']
                    ]
                    st.session_state.task_manager.save_tasks()
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("Add New Task")
    
    with st.form("add_task_form"):
        title = st.text_input("Task Title", placeholder="Enter task title...")
        description = st.text_area("Description", placeholder="Enter task description...", height=100)
        
        col1, col2 = st.columns(2)
        with col1:
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        with col2:
            category = st.selectbox("Category", ["Work", "Personal", "Shopping", "Health", "Learning"])
        
        submitted = st.form_submit_button("➕ Add Task", use_container_width=True)
        
        if submitted and title:
            new_task = {
                "id": len(st.session_state.task_manager.tasks) + 1,
                "title": title,
                "description": description,
                "priority": priority,
                "category": category,
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.task_manager.tasks.append(new_task)
            st.session_state.task_manager.save_tasks()
            st.success("✅ Task added successfully!")
            st.rerun()

with tab3:
    st.header("Dashboard")
    
    if st.session_state.task_manager.tasks:
        # Convert to DataFrame for analysis
        df = pd.DataFrame(st.session_state.task_manager.tasks)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", len(df))
        with col2:
            completed = df['completed'].sum()
            st.metric("Completed", f"{completed}/{len(df)}")
        with col3:
            high_priority = len(df[df['priority'] == 'High'])
            st.metric("High Priority", high_priority)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Priority distribution
            priority_counts = df['priority'].value_counts().reset_index()
            fig1 = px.pie(priority_counts, values='count', names='priority',
                         title="Tasks by Priority",
                         color='priority',
                         color_discrete_map={'High': '#FF6B6B', 
                                           'Medium': '#FFE66D', 
                                           'Low': '#4ECDC4'})
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Completion status
            status_counts = df['completed'].value_counts().reset_index()
            status_counts['status'] = status_counts['completed'].map({True: 'Completed', False: 'Active'})
            fig2 = px.bar(status_counts, x='status', y='count',
                         title="Completion Status",
                         color='status',
                         color_discrete_map={'Completed': '#4ECDC4', 'Active': '#FF6B6B'})
            st.plotly_chart(fig2, use_container_width=True)
        
        # Category breakdown
        category_counts = df['category'].value_counts().reset_index()
        fig3 = px.bar(category_counts, x='category', y='count',
                     title="Tasks by Category",
                     color='category',
                     color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No tasks yet. Add some tasks to see analytics!")

with tab4:
    st.header("Settings")
    
    st.subheader("Theme Settings")
    theme = st.selectbox("Select Theme", ["Light", "Dark", "Colorful"])
    
    st.subheader("Export/Import")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export Tasks to JSON"):
            json_str = json.dumps(st.session_state.task_manager.tasks, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="tasks_backup.json",
                mime="application/json"
            )
    
    with col2:
        uploaded_file = st.file_uploader("Import Tasks from JSON", type="json")
        if uploaded_file:
            try:
                imported_tasks = json.load(uploaded_file)
                st.session_state.task_manager.tasks = imported_tasks
                st.session_state.task_manager.save_tasks()
                st.success("Tasks imported successfully!")
                st.rerun()
            except:
                st.error("Invalid JSON file")

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3067/3067256.png", width=100)
    st.title("Quick Actions")
    
    if st.button("🗑️ Clear All Tasks", use_container_width=True):
        if st.session_state.task_manager.tasks:
            if st.checkbox("Confirm delete all tasks"):
                st.session_state.task_manager.tasks = []
                st.session_state.task_manager.save_tasks()
                st.rerun()
    
    st.divider()
    
    st.subheader("Statistics")
    total_tasks = len(st.session_state.task_manager.tasks)
    completed_tasks = sum(1 for task in st.session_state.task_manager.tasks if task['completed'])
    
    st.metric("📊 Total", total_tasks)
    st.metric("✅ Completed", completed_tasks)
    st.metric("⏳ Pending", total_tasks - completed_tasks)
    
    if total_tasks > 0:
        progress = completed_tasks / total_tasks
        st.progress(progress)
        st.caption(f"Progress: {progress:.0%}")

# Footer
st.divider()
st.caption(f"© 2024 Colorful Task Manager | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
