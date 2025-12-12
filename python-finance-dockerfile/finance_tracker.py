# finance_tracker.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #3B82F6;
    }
    .expense-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'budget' not in st.session_state:
    st.session_state.budget = {'monthly_limit': 5000}
if 'categories' not in st.session_state:
    st.session_state.categories = ['Food', 'Transport', 'Shopping', 
                                   'Entertainment', 'Bills', 'Health', 'Other']

# Sidebar Navigation
def sidebar_nav():
    st.sidebar.markdown("## 💰")
    st.sidebar.title("Finance Tracker")
    page = st.sidebar.radio(
        "Navigation",
        ["📊 Dashboard", "➕ Add Transaction", "📈 Analytics", "💳 Budget", "📋 History"]
    )
    
    # Quick Stats in Sidebar
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)
        total_income = df[df['type'] == 'Income']['amount'].sum()
        total_expense = df[df['type'] == 'Expense']['amount'].sum()
        balance = total_income - total_expense
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Quick Stats")
        st.sidebar.metric("Balance", f"${balance:,.2f}")
        st.sidebar.metric("Income", f"${total_income:,.2f}")
        st.sidebar.metric("Expenses", f"${total_expense:,.2f}")
    
    return page

# Dashboard Page
def dashboard():
    st.markdown('<h1 class="main-header">💰 Personal Finance Dashboard</h1>', 
                unsafe_allow_html=True)
    
    if not st.session_state.transactions:
        st.info("No transactions yet. Add your first transaction to get started!")
        return
    
    df = pd.DataFrame(st.session_state.transactions)
    df['date'] = pd.to_datetime(df['date'])
    
    # Calculate metrics
    total_income = df[df['type'] == 'Income']['amount'].sum()
    total_expense = df[df['type'] == 'Expense']['amount'].sum()
    balance = total_income - total_expense
    monthly_budget = st.session_state.budget['monthly_limit']
    budget_used = (total_expense / monthly_budget * 100) if monthly_budget > 0 else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💵 Balance", f"${balance:,.2f}", 
                 delta=f"${balance - total_expense:,.2f}")
    with col2:
        st.metric("📈 Total Income", f"${total_income:,.2f}")
    with col3:
        st.metric("📉 Total Expenses", f"${total_expense:,.2f}")
    with col4:
        st.metric("📊 Budget Used", f"{budget_used:.1f}%",
                 delta=f"${monthly_budget - total_expense:,.2f} left")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Expense by Category
        expense_df = df[df['type'] == 'Expense']
        if not expense_df.empty:
            category_sum = expense_df.groupby('category')['amount'].sum().reset_index()
            fig = px.pie(category_sum, values='amount', names='category',
                        title='Expenses by Category',
                        hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Income vs Expense
        type_sum = df.groupby('type')['amount'].sum().reset_index()
        fig = px.bar(type_sum, x='type', y='amount',
                    title='Income vs Expenses',
                    color='type',
                    color_discrete_map={'Income': '#10B981', 'Expense': '#EF4444'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Spending Trend
    st.subheader("📅 Spending Trend")
    daily_expense = df[df['type'] == 'Expense'].groupby(
        df['date'].dt.date)['amount'].sum().reset_index()
    daily_expense.columns = ['date', 'amount']
    
    fig = px.line(daily_expense, x='date', y='amount',
                 title='Daily Expenses Over Time')
    st.plotly_chart(fig, use_container_width=True)
    
    # Recent Transactions
    st.subheader("🕒 Recent Transactions")
    recent = df.sort_values('date', ascending=False).head(5)
    st.dataframe(recent[['date', 'type', 'category', 'amount', 'description']], 
                use_container_width=True, hide_index=True)

# Add Transaction Page
def add_transaction():
    st.title("➕ Add New Transaction")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("transaction_form"):
            transaction_type = st.selectbox("Type", ["Expense", "Income"])
            
            col_a, col_b = st.columns(2)
            with col_a:
                amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
                date = st.date_input("Date", datetime.now())
            
            with col_b:
                if transaction_type == "Expense":
                    category = st.selectbox("Category", st.session_state.categories)
                else:
                    category = st.selectbox("Category", ["Salary", "Freelance", 
                                                        "Investment", "Gift", "Other"])
                payment_method = st.selectbox("Payment Method", 
                                            ["Cash", "Credit Card", "Debit Card", 
                                             "Bank Transfer", "Digital Wallet"])
            
            description = st.text_area("Description (optional)")
            
            submitted = st.form_submit_button("Add Transaction", type="primary")
            
            if submitted and amount > 0:
                transaction = {
                    'date': date.strftime('%Y-%m-%d'),
                    'type': transaction_type,
                    'category': category,
                    'amount': amount,
                    'description': description,
                    'payment_method': payment_method,
                    'timestamp': datetime.now().isoformat()
                }
                st.session_state.transactions.append(transaction)
                st.success(f"✅ {transaction_type} of ${amount:,.2f} added successfully!")
                st.balloons()
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>💡 Tips</h4>
            <ul>
                <li>Track all expenses daily</li>
                <li>Categorize accurately</li>
                <li>Add descriptions for clarity</li>
                <li>Review weekly spending</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Analytics Page
def analytics():
    st.title("📈 Financial Analytics")
    
    if not st.session_state.transactions:
        st.warning("No data available for analysis. Add transactions first.")
        return
    
    df = pd.DataFrame(st.session_state.transactions)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.to_period('M').astype(str)
    
    # Monthly Analysis
    st.subheader("📆 Monthly Analysis")
    
    monthly_data = df.groupby(['month', 'type'])['amount'].sum().reset_index()
    fig = px.bar(monthly_data, x='month', y='amount', color='type',
                title='Monthly Income vs Expenses',
                barmode='group',
                color_discrete_map={'Income': '#10B981', 'Expense': '#EF4444'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Category-wise Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Top Expense Categories")
        expense_df = df[df['type'] == 'Expense']
        if not expense_df.empty:
            top_categories = expense_df.groupby('category')['amount'].sum().sort_values(
                ascending=False).head(5)
            fig = px.bar(x=top_categories.values, y=top_categories.index,
                        orientation='h',
                        labels={'x': 'Amount ($)', 'y': 'Category'})
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💳 Payment Methods")
        payment_dist = df.groupby('payment_method')['amount'].sum()
        fig = px.pie(values=payment_dist.values, names=payment_dist.index,
                    hole=0.3)
        st.plotly_chart(fig, use_container_width=True)
    
    # Spending Pattern
    st.subheader("📉 Spending Pattern")
    df['day_of_week'] = df['date'].dt.day_name()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                 'Friday', 'Saturday', 'Sunday']
    expense_by_day = df[df['type'] == 'Expense'].groupby(
        'day_of_week')['amount'].mean().reindex(day_order)
    
    fig = px.bar(x=expense_by_day.index, y=expense_by_day.values,
                labels={'x': 'Day', 'y': 'Average Expense ($)'},
                title='Average Daily Spending by Weekday')
    st.plotly_chart(fig, use_container_width=True)

# Budget Page
def budget_page():
    st.title("💳 Budget Management")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Set Monthly Budget")
        new_budget = st.number_input("Monthly Budget Limit ($)", 
                                     value=st.session_state.budget['monthly_limit'],
                                     min_value=0, step=100)
        
        if st.button("Update Budget"):
            st.session_state.budget['monthly_limit'] = new_budget
            st.success(f"Budget updated to ${new_budget:,.2f}")
    
    with col2:
        if st.session_state.transactions:
            df = pd.DataFrame(st.session_state.transactions)
            total_expense = df[df['type'] == 'Expense']['amount'].sum()
            budget_limit = st.session_state.budget['monthly_limit']
            remaining = budget_limit - total_expense
            percentage = (total_expense / budget_limit * 100) if budget_limit > 0 else 0
            
            st.subheader("Budget Status")
            st.metric("Budget Limit", f"${budget_limit:,.2f}")
            st.metric("Spent", f"${total_expense:,.2f}")
            st.metric("Remaining", f"${remaining:,.2f}", 
                     delta=f"{percentage:.1f}% used")
            
            # Progress bar
            if percentage <= 50:
                color = "green"
            elif percentage <= 80:
                color = "orange"
            else:
                color = "red"
            
            st.markdown(f"""
            <div style="background-color: #f0f0f0; border-radius: 10px; height: 30px;">
                <div style="background-color: {color}; width: {min(percentage, 100)}%; 
                     height: 30px; border-radius: 10px; text-align: center; 
                     line-height: 30px; color: white; font-weight: bold;">
                    {percentage:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

# History Page
def history():
    st.title("📋 Transaction History")
    
    if not st.session_state.transactions:
        st.info("No transaction history available.")
        return
    
    df = pd.DataFrame(st.session_state.transactions)
    df['date'] = pd.to_datetime(df['date'])
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_type = st.multiselect("Filter by Type", 
                                    ["Income", "Expense"],
                                    default=["Income", "Expense"])
    with col2:
        categories = df['category'].unique().tolist()
        filter_category = st.multiselect("Filter by Category", 
                                        categories,
                                        default=categories)
    with col3:
        date_range = st.date_input("Date Range", 
                                  value=(df['date'].min(), df['date'].max()),
                                  key="date_range")
    
    # Apply filters
    filtered_df = df[
        (df['type'].isin(filter_type)) &
        (df['category'].isin(filter_category)) &
        (df['date'] >= pd.to_datetime(date_range[0])) &
        (df['date'] <= pd.to_datetime(date_range[1]))
    ]
    
    st.subheader(f"Showing {len(filtered_df)} transactions")
    
    # Display table
    st.dataframe(
        filtered_df.sort_values('date', ascending=False)[
            ['date', 'type', 'category', 'amount', 'payment_method', 'description']
        ],
        use_container_width=True,
        hide_index=True
    )
    
    # Export option
    if st.button("📥 Export to CSV"):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"transactions_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

# Main App
def main():
    page = sidebar_nav()
    
    if page == "📊 Dashboard":
        dashboard()
    elif page == "➕ Add Transaction":
        add_transaction()
    elif page == "📈 Analytics":
        analytics()
    elif page == "💳 Budget":
        budget_page()
    elif page == "📋 History":
        history()
    
    # Footer
    st.markdown("---")
    st.markdown("**Personal Finance Tracker** © 2024 | Built with Streamlit")

if __name__ == "__main__":
    main()

