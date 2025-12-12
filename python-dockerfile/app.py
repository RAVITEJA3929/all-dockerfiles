# app.py
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="SkyWings Flight Booking",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
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
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #3B82F6;
    }
    .flight-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .flight-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .price-tag {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 5px;
        font-weight: bold;
        width: 100%;
    }
    .booking-confirmed {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'bookings' not in st.session_state:
    st.session_state.bookings = []
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

# Sample flight data
def generate_flight_data():
    cities = ['New York', 'Los Angeles', 'Chicago', 'Miami', 'London', 'Paris', 
              'Tokyo', 'Dubai', 'Sydney', 'Singapore', 'Delhi', 'Frankfurt']
    
    flights = []
    airlines = ['SkyWings Airlines', 'Global Airways', 'Oceanic Airlines', 'Continental Express']
    
    for i in range(50):
        departure = random.choice(cities)
        arrival = random.choice([c for c in cities if c != departure])
        departure_time = datetime.now() + timedelta(days=random.randint(1, 30), 
                                                   hours=random.randint(0, 23))
        duration = timedelta(hours=random.randint(1, 12))
        arrival_time = departure_time + duration
        
        flight = {
            'flight_number': f'SW{random.randint(1000, 9999)}',
            'airline': random.choice(airlines),
            'departure_city': departure,
            'arrival_city': arrival,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'duration': duration,
            'price': round(random.uniform(150, 1500), 2),
            'available_seats': random.randint(5, 200),
            'aircraft_type': random.choice(['Boeing 737', 'Airbus A320', 'Boeing 787', 'Airbus A350']),
            'class': random.choice(['Economy', 'Premium Economy', 'Business', 'First'])
        }
        flights.append(flight)
    
    return pd.DataFrame(flights)

# Navigation
def navigation():
    st.sidebar.markdown("# ✈️ SkyWings Booking")
    st.sidebar.title("SkyWings Booking")
    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "🔍 Find Flights", "📋 My Bookings", "📊 Analytics", "👤 Profile"]
    )
    return page

# Home Page
def home_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="main-header">✈️ SkyWings Flight Booking</h1>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick booking form
    st.subheader("🎯 Quick Flight Search")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        departure = st.selectbox("From", ['New York', 'Los Angeles', 'Chicago', 'Miami', 'London', 
                                         'Paris', 'Tokyo', 'Dubai', 'Select City'], index=8)
    with col2:
        arrival = st.selectbox("To", ['New York', 'Los Angeles', 'Chicago', 'Miami', 'London', 
                                     'Paris', 'Tokyo', 'Dubai', 'Select City'], index=8)
    with col3:
        departure_date = st.date_input("Departure Date", 
                                      datetime.now() + timedelta(days=7))
    with col4:
        passengers = st.selectbox("Passengers", [1, 2, 3, 4, 5, 6])
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔍 Search Flights", use_container_width=True):
            st.session_state.page = "🔍 Find Flights"
            st.rerun()
    
    st.markdown("---")
    
    # Features section
    st.subheader("🌟 Why Choose SkyWings?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h4>🚀 Best Prices</h4>
            <p>Guaranteed lowest fares on all flights with price match promise.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h4>🛡️ Flexible Booking</h4>
            <p>Free cancellation and easy date changes on most flights.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h4>⭐ Premium Service</h4>
            <p>24/7 customer support and premium in-flight experience.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Popular destinations
    st.subheader("🌍 Popular Destinations")
    
    destinations = [
        {"city": "Paris", "price": "$499", "image": "🇫🇷"},
        {"city": "Tokyo", "price": "$899", "image": "🇯🇵"},
        {"city": "Dubai", "price": "$699", "image": "🇦🇪"},
        {"city": "Sydney", "price": "$1299", "image": "🇦🇺"},
    ]
    
    cols = st.columns(4)
    for idx, dest in enumerate(destinations):
        with cols[idx]:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; border-radius: 10px; 
                        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
                <h1>{dest['image']}</h1>
                <h4>{dest['city']}</h4>
                <p style="color: #3B82F6; font-weight: bold;">From {dest['price']}</p>
            </div>
            """, unsafe_allow_html=True)

# Flight Search Page
def search_flights():
    st.title("🔍 Find & Book Flights")
    
    # Search filters
    with st.expander("🔧 Advanced Filters", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            departure = st.selectbox("Departure City", 
                                   ['Any', 'New York', 'Los Angeles', 'Chicago', 'Miami', 
                                    'London', 'Paris', 'Tokyo', 'Dubai', 'Sydney'])
            airline = st.multiselect("Airlines", 
                                   ['SkyWings Airlines', 'Global Airways', 
                                    'Oceanic Airlines', 'Continental Express'],
                                   default=['SkyWings Airlines', 'Global Airways'])
        
        with col2:
            arrival = st.selectbox("Arrival City", 
                                 ['Any', 'New York', 'Los Angeles', 'Chicago', 'Miami', 
                                  'London', 'Paris', 'Tokyo', 'Dubai', 'Sydney'])
            flight_class = st.selectbox("Class", 
                                      ['Any', 'Economy', 'Premium Economy', 'Business', 'First'])
        
        with col3:
            price_range = st.slider("Price Range ($)", 100, 2000, (200, 1000))
            sort_by = st.selectbox("Sort by", 
                                 ['Price: Low to High', 'Price: High to Low', 
                                  'Duration', 'Departure Time'])
    
    # Generate sample flights
    flights_df = generate_flight_data()
    
    # Apply filters
    if departure != 'Any':
        flights_df = flights_df[flights_df['departure_city'] == departure]
    if arrival != 'Any':
        flights_df = flights_df[flights_df['arrival_city'] == arrival]
    if airline:
        flights_df = flights_df[flights_df['airline'].isin(airline)]
    if flight_class != 'Any':
        flights_df = flights_df[flights_df['class'] == flight_class]
    
    flights_df = flights_df[(flights_df['price'] >= price_range[0]) & 
                           (flights_df['price'] <= price_range[1])]
    
    # Sort results
    if sort_by == 'Price: Low to High':
        flights_df = flights_df.sort_values('price')
    elif sort_by == 'Price: High to Low':
        flights_df = flights_df.sort_values('price', ascending=False)
    elif sort_by == 'Duration':
        flights_df = flights_df.sort_values('duration')
    else:
        flights_df = flights_df.sort_values('departure_time')
    
    st.session_state.search_results = flights_df.to_dict('records')
    
    # Display results
    st.subheader(f"📋 Found {len(flights_df)} Flights")
    
    if not flights_df.empty:
        for idx, flight in flights_df.iterrows():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="flight-card">
                    <h4>{flight['departure_city']} → {flight['arrival_city']}</h4>
                    <p><strong>{flight['airline']}</strong> • {flight['flight_number']}</p>
                    <p>🛫 {flight['departure_time'].strftime('%b %d, %Y %H:%M')}</p>
                    <p>🛬 {flight['arrival_time'].strftime('%b %d, %Y %H:%M')}</p>
                    <p>⏱️ {str(flight['duration'])[:4]} hours • {flight['class']} Class</p>
                    <p>✈️ {flight['aircraft_type']} • 🪑 {flight['available_seats']} seats left</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Flight path visualization
                fig = go.Figure(go.Scattergeo(
                    lon = [random.randint(-180, 180), random.randint(-180, 180)],
                    lat = [random.randint(-90, 90), random.randint(-90, 90)],
                    mode = 'lines+markers',
                    line = dict(width=2, color='blue'),
                    marker = dict(size=8, color=['green', 'red']),
                    text = [flight['departure_city'], flight['arrival_city']],
                ))
                
                fig.update_layout(
                    geo=dict(
                        showland=True,
                        landcolor="rgb(243, 243, 243)",
                        countrycolor="rgb(204, 204, 204)",
                    ),
                    height=150,
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col3:
                st.markdown(f"""
                <div style="text-align: center;">
                    <h2 style="color: #3B82F6;">${flight['price']}</h2>
                    <p style="font-size: 0.8em;">per passenger</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Book Now", key=f"book_{idx}"):
                    st.session_state.selected_flight = flight.to_dict()
                    st.session_state.page = "booking_form"
                    st.rerun()
            
            st.markdown("---")
    else:
        st.warning("No flights found matching your criteria. Try adjusting your filters.")

# Booking Form
def booking_form():
    if 'selected_flight' not in st.session_state:
        st.error("No flight selected!")
        return
    
    flight = st.session_state.selected_flight
    
    st.title("📝 Complete Your Booking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Flight Details")
        st.markdown(f"""
        <div class="card">
            <h4>{flight['departure_city']} → {flight['arrival_city']}</h4>
            <p><strong>{flight['airline']}</strong> • {flight['flight_number']}</p>
            <p>🛫 {flight['departure_time'].strftime('%b %d, %Y %H:%M')}</p>
            <p>🛬 {flight['arrival_time'].strftime('%b %d, %Y %H:%M')}</p>
            <p>⏱️ {str(flight['duration'])[:4]} hours • {flight['class']} Class</p>
            <p>✈️ {flight['aircraft_type']}</p>
            <h3 style="color: #3B82F6;">Total: ${flight['price']}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Passenger Information")
        
        with st.form("booking_form"):
            st.write("Primary Passenger")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            
            st.write("Additional Information")
            passport = st.text_input("Passport Number")
            dob = st.date_input("Date of Birth", datetime.now() - timedelta(days=365*30))
            
            # Seat selection
            st.write("Seat Preference")
            seat_pref = st.radio("Seat", ["Aisle", "Window", "No Preference"])
            
            # Meal preference
            meal = st.selectbox("Meal Preference", 
                              ["Standard", "Vegetarian", "Vegan", "Kosher", "Halal", "No Meal"])
            
            # Payment
            st.write("Payment Method")
            payment = st.selectbox("Payment Method", 
                                 ["Credit Card", "Debit Card", "PayPal", "Apple Pay"])
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Confirm Booking", type="primary")
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.page = "🔍 Find Flights"
                    st.rerun()
            
            if submit:
                if all([first_name, last_name, email, phone]):
                    # Create booking record
                    booking = {
                        'booking_id': f'BK{random.randint(100000, 999999)}',
                        'flight': flight,
                        'passenger': {
                            'first_name': first_name,
                            'last_name': last_name,
                            'email': email,
                            'phone': phone,
                            'passport': passport,
                            'dob': dob,
                            'seat_preference': seat_pref,
                            'meal_preference': meal
                        },
                        'payment_method': payment,
                        'booking_date': datetime.now(),
                        'status': 'Confirmed'
                    }
                    
                    st.session_state.bookings.append(booking)
                    st.session_state.user_info = booking['passenger']
                    
                    # Show confirmation
                    st.balloons()
                    st.success("🎉 Booking Confirmed!")
                    
                    st.markdown(f"""
                    <div class="card booking-confirmed">
                        <h3>Booking Confirmation: {booking['booking_id']}</h3>
                        <p>An email confirmation has been sent to {email}</p>
                        <p>You can view your booking in the "My Bookings" section</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add delay before redirecting
                    import time
                    time.sleep(3)
                    st.session_state.page = "📋 My Bookings"
                    st.rerun()
                else:
                    st.error("Please fill in all required fields")

# My Bookings Page
def my_bookings():
    st.title("📋 My Bookings")
    
    if not st.session_state.bookings:
        st.info("You have no bookings yet. Search for flights to get started!")
        if st.button("🔍 Search Flights"):
            st.session_state.page = "🔍 Find Flights"
            st.rerun()
        return
    
    for booking in st.session_state.bookings:
        flight = booking['flight']
        passenger = booking['passenger']
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div class="flight-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4>{flight['departure_city']} → {flight['arrival_city']}</h4>
                        <p><strong>Booking ID:</strong> {booking['booking_id']}</p>
                        <p><strong>Status:</strong> <span style="color: green;">{booking['status']}</span></p>
                    </div>
                    <div style="text-align: right;">
                        <h3 style="color: #3B82F6;">${flight['price']}</h3>
                        <p>Booked on {booking['booking_date'].strftime('%b %d, %Y')}</p>
                    </div>
                </div>
                <p><strong>Passenger:</strong> {passenger['first_name']} {passenger['last_name']}</p>
                <p><strong>Flight:</strong> {flight['airline']} • {flight['flight_number']}</p>
                <p><strong>Departure:</strong> {flight['departure_time'].strftime('%b %d, %Y %H:%M')}</p>
                <p><strong>Class:</strong> {flight['class']} • <strong>Seat:</strong> {passenger['seat_preference']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Modify", key=f"modify_{booking['booking_id']}"):
                    st.info("Modification feature coming soon!")
            with col2:
                if st.button("❌ Cancel", key=f"cancel_{booking['booking_id']}"):
                    booking['status'] = 'Cancelled'
                    st.success("Booking cancelled successfully!")
                    st.rerun()
        
        st.markdown("---")

# Analytics Page
def analytics_page():
    st.title("📊 Travel Analytics")
    
    # Generate analytics data
    flights_df = generate_flight_data()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_price = flights_df['price'].mean()
        st.metric("Average Flight Price", f"${avg_price:.2f}")
    
    with col2:
        total_flights = len(flights_df)
        st.metric("Available Flights", total_flights)
    
    with col3:
        popular_dest = flights_df['arrival_city'].mode()[0]
        st.metric("Most Popular Destination", popular_dest)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Price distribution
        fig = px.histogram(flights_df, x='price', nbins=20,
                          title="Flight Price Distribution",
                          labels={'price': 'Price ($)'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Popular destinations
        dest_counts = flights_df['arrival_city'].value_counts().head(10)
        fig = px.bar(x=dest_counts.index, y=dest_counts.values,
                    title="Top 10 Destinations",
                    labels={'x': 'City', 'y': 'Number of Flights'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Flight duration analysis
    flights_df['duration_hours'] = flights_df['duration'].dt.total_seconds() / 3600
    
    fig = px.scatter(flights_df, x='duration_hours', y='price',
                    color='class', hover_data=['departure_city', 'arrival_city'],
                    title="Flight Duration vs Price by Class")
    st.plotly_chart(fig, use_container_width=True)

# Profile Page
def profile_page():
    st.title("👤 My Profile")
    
    if st.session_state.user_info:
        user = st.session_state.user_info
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("""
            <div style="text-align: center;">
                <div style="font-size: 4rem; margin: 20px;">👤</div>
                <h3>{first_name} {last_name}</h3>
                <p>✈️ SkyWings Member</p>
            </div>
            """.format(**user), unsafe_allow_html=True)
        
        with col2:
            st.subheader("Personal Information")
            st.markdown(f"""
            <div class="card">
                <p><strong>Full Name:</strong> {user.get('first_name', '')} {user.get('last_name', '')}</p>
                <p><strong>Email:</strong> {user.get('email', 'Not provided')}</p>
                <p><strong>Phone:</strong> {user.get('phone', 'Not provided')}</p>
                <p><strong>Date of Birth:</strong> {user.get('dob', 'Not provided')}</p>
                <p><strong>Passport:</strong> {user.get('passport', 'Not provided')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.subheader("Preferences")
            st.markdown(f"""
            <div class="card">
                <p><strong>Seat Preference:</strong> {user.get('seat_preference', 'Not set')}</p>
                <p><strong>Meal Preference:</strong> {user.get('meal_preference', 'Not set')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.info("Complete a booking to create your profile!")
        
        with st.form("profile_form"):
            st.subheader("Create Your Profile")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            
            if st.form_submit_button("Save Profile"):
                if all([first_name, last_name, email]):
                    st.session_state.user_info = {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'phone': phone
                    }
                    st.success("Profile saved successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields")

# Main App
def main():
    # Initialize page in session state
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 Home"
    
    # Navigation
    page = navigation()
    
    # Page routing
    if page == "🏠 Home":
        home_page()
    elif page == "🔍 Find Flights":
        search_flights()
    elif page == "📋 My Bookings":
        my_bookings()
    elif page == "📊 Analytics":
        analytics_page()
    elif page == "👤 Profile":
        profile_page()
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**SkyWings Booking**")
        st.markdown("© 2024 All rights reserved")
    with col2:
        st.markdown("**Contact Us**")
        st.markdown("📞 +1 (800) FLY-SKYWING")
        st.markdown("✉️ support@skywings.com")
    with col3:
        st.markdown("**Follow Us**")
        st.markdown("🐦 Twitter • 📘 Facebook • 📸 Instagram")

if __name__ == "__main__":
    main()
