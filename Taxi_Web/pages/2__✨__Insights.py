import streamlit as st
import pandas as pd
import numpy  as np
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("""
    <div style="text-align: center; font-size: 50px; font-weight: bold; color: white;">
        NYC <span style="color: #F7C300;">Insights</span>
    </div>
    <div style="display: flex; justify-content: center;">
        <img src="https://plus.unsplash.com/premium_photo-1682309586073-902b5c4905b8?q=80&w=2112&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Taxi GIF" style="width: 80%; max-width: 900px;">
    </div>
""", unsafe_allow_html=True)


st.divider()

df = pd.read_csv('sampled_data.csv')
locations = pd.read_csv('taxi_zone_lookup.csv')

col1,col2,col3 = st.columns([6,1,6])
# Divider

with col1:
    fig = px.pie(df['vendorid'].map({1: 'Creative Mobile Technologies', 2: 'VeriFone Inc.'}),
        names='vendorid', title='Vendor ID Distribution', template='plotly_dark',
        color_discrete_sequence= px.colors.sequential.Plasma_r)
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0.1], textfont_size=10)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)
    
    st.write('''
    🌟 **Vendor Distribution Breakdown** 🌟

    The pie chart shows the distribution of trips between the vendors:

    🟠 **Creative Mobile Technologies**: Slightly behind in market share.

    🟡 **VeriFone Inc.**: Leads with a larger share of trips.

    **Key Insights**:
    - **VeriFone Inc.** has a larger market share, indicating higher usage.
    - **Creative Mobile Technologies** follows closely, highlighting a competitive market.

    This distribution reveals preferences and performance trends among the vendors.
    ''')
    

# Content for the Vendor Fare Breakdown tab
with col3:
    # Filter the data to calculate the average fare amount per vendorid
    data_group = df.groupby('vendorid')['fare_amount'].mean().reset_index()

    # Map vendor IDs to names
    data_group['vendorid'] = data_group['vendorid'].map({1: 'Creative Mobile Technologies', 2: 'VeriFone Inc.'})

    # Create the bar chart
    fig = px.bar(data_group, x='vendorid', y='fare_amount',
                title='Average Fare Amount per Vendor',
                template='plotly_dark',
                color_discrete_sequence= px.colors.sequential.Plasma_r,
                text_auto=True,
                labels={'vendorid': 'Vendor Name', 'fare_amount': 'Average Fare Amount'})

    # Update bar chart layout
    fig.update_xaxes(title='Vendor Name')
    fig.update_yaxes(title='Average Fare Amount')
    fig.update_layout(title_text='Average Fare Amount Distribution by Vendor')

    # Display the bar chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Insights
    st.write('''
    🌟 **Vendor Fare Comparison** 🌟

    The bar chart displays average fares by vendor:

    🟠 **Creative Mobile Technologies**: Slightly lower average fares.

    🟡 **VeriFone Inc.**: Higher average fares.

    **Key Takeaways:**

    - **VeriFone Inc.** has higher fares, suggesting a premium service.
    - **Creative Mobile Technologies** offers more competitive pricing.
    ''')

st.divider()

col1,col2,col3 = st.columns([6,1,6])

# Assuming `passengers` is your DataFrame containing 'passenger_count' and 'percentage' columns
passengers = df.groupby('passenger_count').size().reset_index(name='count')
passengers['percentage'] = (passengers['count'] / passengers['count'].sum()) * 100

with col1:
    fig = px.pie(passengers, names='passenger_count', values='percentage', template='plotly_dark',
                 color_discrete_sequence= px.colors.sequential.Plasma_r, title='Passenger Count Distribution')
    fig.update_traces(textinfo='percent+label', pull=[0.1] * len(passengers), textfont_size=10)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

    st.write('''
    🌟 **Passenger Count Distribution** 🌟

    The pie chart shows the distribution of trips by passenger count:

    🔵 **1 Passenger**: Represents the largest proportion of trips.

    🔴 **2-6 Passengers**: Comprise a smaller, yet significant, portion of the total trips.

    **Key Insights**:
    - **1 Passenger trips** dominate the distribution, indicating frequent solo travel.
    - **2-6 Passenger trips** highlight a pattern of group travel, though less common.

    This distribution reveals travel preferences and trends among passengers.
    ''')
with col3:
    fig = px.pie(
        df['payment_type']
        .value_counts(normalize=True)
        .mul(100)
        .round(3)
        .rename_axis('Payment Type')
        .reset_index(name='Percentage')
        .replace({'Payment Type': {1: 'Credit Card', 2: 'Cash'}}),
        names='Payment Type',
        values='Percentage',
        template='plotly_dark',
        color_discrete_sequence=px.colors.sequential.Plasma_r,
        title='Payment Type Distribution'
    )
    fig.update_traces(textinfo='percent+label', pull=[0.1] * len(df['payment_type'].value_counts()), textfont_size=10)
    fig.update_layout(showlegend=False)

    # Display the chart
    st.plotly_chart(fig)

    # Description
    st.write('''
    🌟 **Payment Type Distribution** 🌟

    The pie chart illustrates the distribution of trips by payment method:

    🔵 **Credit Card**: Represents the majority of trips.

    🔴 **Cash**: Accounts for a smaller, yet significant, portion of trips.

    **Key Insights**:
    - **Credit Card** payments are predominant, indicating a strong preference for cashless transactions.
    - **Cash** payments, while less frequent, still hold a notable share.

    This distribution highlights the payment preferences and trends among passengers.
    ''')
st.divider()

col1, col2, col3 = st.columns([6, 1, 6])

# Calculate the frequency of pickup locations
pi_locations_freq = df['pulocationid'].value_counts().reset_index().rename(columns={'index': 'PULocationID', 'pulocationid': 'Frequency'}).sort_values(by='Frequency', ascending=True)

# Ensure column names match
pickup_locations = locations.rename(columns={'LocationID': 'PULocationID'})[['PULocationID', 'Zone']]



# Merge data with error handling
try:
    pi_locations_freq = pi_locations_freq.merge(pickup_locations, on='PULocationID', how='left')
except KeyError as e:
    st.error(f"KeyError: {e}")
    st.stop()

with col1:
    # Create the bar chart for the top 10 pickup locations
    fig = px.bar(pi_locations_freq.tail(10), y='Zone', x='Frequency', text_auto=True,
                 title='Top 10 Pickup Locations', template='plotly_dark', color='Frequency')
    fig.update_xaxes(title='Frequency')
    fig.update_yaxes(title='Zone')
    st.plotly_chart(fig)

    # Add insights
    st.write('''
    🌟 **Top Pickup Locations Breakdown** 🌟

    The bar chart highlights the top 10 zones with the highest frequency of pickups:

    🟠 **Most Popular Zones**: These locations see the most taxi activity, indicating key hotspots.

    🟡 **Less Frequent Zones**: While still popular, these areas see slightly less activity.

    **Key Insights**:
    - The most frequented zones are key areas of interest for taxi pickups.
    - The distribution of pickups might reflect high-demand areas such as commercial or tourist hubs.

    Understanding these trends helps in optimizing service coverage and identifying high-demand areas.
    ''')

# Calculate the frequency of dropoff locations
do_locations_freq = df['dolocationid'].value_counts().reset_index().rename(columns={'index': 'DOLocationID', 'dolocationid': 'Frequency'}).sort_values(by='Frequency', ascending=True)

# Ensure column names match
dropoff_locations = locations.rename(columns={'LocationID': 'DOLocationID'})[['DOLocationID', 'Zone']]


# Merge data with error handling
try:
    do_locations_freq = do_locations_freq.merge(dropoff_locations, on='DOLocationID', how='left')
except KeyError as e:
    st.error(f"KeyError: {e}")
    st.stop()

with col3:
    # Create the bar chart for the top 10 drop-off locations
    fig = px.bar(do_locations_freq.tail(10), y='Zone', x='Frequency', text_auto=True,
                 title='Top 10 Drop-off Locations', template='plotly_dark', color='Frequency')
    fig.update_xaxes(title='Frequency')
    fig.update_yaxes(title='Zone')
    st.plotly_chart(fig)

    # Add insights
    st.write('''
    🌟 **Top Drop-off Locations Breakdown** 🌟

    The bar chart showcases the top 10 zones with the highest frequency of drop-offs:

    🟠 **Most Frequent Drop-off Zones**: These areas are popular destinations, indicating key drop-off points.

    🟡 **Less Frequent Drop-off Zones**: These zones are still popular but see slightly less drop-off activity.

    **Key Insights**:
    - The most frequented drop-off zones are crucial areas, possibly indicating popular destinations or central locations.
    - The distribution of drop-offs provides insights into travel patterns and customer preferences.

    Analyzing these drop-off trends can help in optimizing routes and improving service efficiency.
    ''')

st.divider()


col1, col2, col3 = st.columns([6, 1, 6])

# Define holidays
df['holiday'] = df['day'].apply(lambda x: 1 if x in [1, 6, 7, 13, 14, 20, 21, 27, 28] else 0)

# Extract the drop-off and pickup hours from the datetime
df['dropoff_hour'] = pd.to_datetime(df['tpep_dropoff_datetime']).dt.hour
df['pickup_hour'] = pd.to_datetime(df['tpep_pickup_datetime']).dt.hour

# Separate data for holidays and non-holidays
df_holiday = df[df['holiday'] == 1]
df_non_holiday = df[df['holiday'] == 0]

# Create line chart for drop-off hour distribution
fig_dropoff = px.line(
    df_holiday['dropoff_hour'].value_counts().reset_index().rename(columns={'index': 'Hour', 'dropoff_hour': 'Frequency'}).sort_values(by='Hour'),
    x='Hour',
    y='Frequency',
    title='Drop-off Hour Distribution',
    template='plotly_dark',
    markers=True,
    line_dash_sequence=['solid'],  # Line style for holiday
    color_discrete_sequence=['#FF5733'],  # Color for holiday
    line_shape='linear'
)

fig_dropoff.add_scatter(
    x=df_non_holiday['dropoff_hour'].value_counts().reset_index().rename(columns={'index': 'Hour', 'dropoff_hour': 'Frequency'}).sort_values(by='Hour')['Hour'],
    y=df_non_holiday['dropoff_hour'].value_counts().reset_index().rename(columns={'index': 'Hour', 'dropoff_hour': 'Frequency'}).sort_values(by='Hour')['Frequency'],
    mode='lines+markers',
    name='Non-Holiday',
    line_dash='dash',  # Line style for non-holiday
    line_color='#33B5E5'  # Color for non-holiday
)

fig_dropoff.update_xaxes(title='Hour')
fig_dropoff.update_yaxes(title='Frequency')

# Create line chart for pickup hour distribution
fig_pickup = px.line(
    df_holiday['pickup_hour'].value_counts().reset_index().rename(columns={'index': 'Hour', 'pickup_hour': 'Frequency'}).sort_values(by='Hour'),
    x='Hour',
    y='Frequency',
    title='Pickup Hour Distribution',
    template='plotly_dark',
    markers=True,
    line_dash_sequence=['solid'],  # Line style for holiday
    color_discrete_sequence=['#FF5733'],  # Color for holiday
    line_shape='linear'
)

fig_pickup.add_scatter(
    x=df_non_holiday['pickup_hour'].value_counts().reset_index().rename(columns={'index': 'Hour', 'pickup_hour': 'Frequency'}).sort_values(by='Hour')['Hour'],
    y=df_non_holiday['pickup_hour'].value_counts().reset_index().rename(columns={'index': 'Hour', 'pickup_hour': 'Frequency'}).sort_values(by='Hour')['Frequency'],
    mode='lines+markers',
    name='Non-Holiday',
    line_dash='dash',  # Line style for non-holiday
    line_color='#33B5E5'  # Color for non-holiday
)

fig_pickup.update_xaxes(title='Hour')
fig_pickup.update_yaxes(title='Frequency')

# Display the charts in Streamlit
with col1:
    st.plotly_chart(fig_pickup)
    st.write('''
    🌟 **Pickup Hour Breakdown** 🌟

    The line chart shows the distribution of pickups across different hours of the day, with separate lines for holidays and non-holidays:

    - 🟠 **Holiday Hours**: Noticeable peaks in the early morning and evening, indicating high demand during those times.
    - 🔵 **Non-Holiday Hours**: Displays a more consistent distribution with a slight increase in the evening.

    **Key Takeaways**:
    - **Holiday pickups** tend to be concentrated around certain peak hours, reflecting leisure and event-based travel.
    - **Non-Holiday pickups** have a steadier pattern, likely reflecting routine travel such as commuting.

    Understanding these patterns can help optimize fleet management and improve service during peak times.
    ''')

with col3:
    st.plotly_chart(fig_dropoff)
    st.write('''
    🌟 **Drop-off Hour Breakdown** 🌟

    The line chart illustrates the distribution of drop-offs at different hours of the day, distinguishing between holidays and non-holidays:

    * 🟠 **Holiday Hours**: Significant peaks during early morning and late evening, suggesting travel linked to events and leisure activities.
    * 🔵 **Non-Holiday Hours**: Shows more uniform activity, with a slight evening rise indicating routine end-of-day travel.

    **Key Insights**:
    - **Holiday drop-offs** show higher variance with noticeable peaks at specific times, reflecting event-driven travel.
    - **Non-Holiday drop-offs** are more consistent throughout the day, likely reflecting regular commuting and daily routines.

    Analyzing these drop-off patterns provides valuable insights into passenger behavior and can inform service strategies.
    ''')

st.divider()
