import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gdown
import numpy as np
import requests
import plotly.graph_objects as go

# Function to download data

st.set_option('deprecation.showPyplotGlobalUse', False)

def download_data():
    try:
        file_id = '1hfgKN8HeajewZLuAShNDYcXKfME3uIcS'
        url = f'https://drive.google.com/uc?id={file_id}'
        output_path = 'dataset.csv'  # Change the output path and filename as needed
        response = requests.get(url)
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return output_path
    except Exception as e:
        print(f"An error occurred while downloading the data: {str(e)}")
        return None

# Load the dataset

def load_data():
    file_path = download_data()
    if file_path:
        return pd.read_csv(file_path)
    else:
        print("Failed to download the data file.")
        return None

# Load data
data = load_data()

# Handle date format
data['REGISTRATION DATE'] = pd.to_datetime(data['REGISTRATION DATE'], format='%d/%m/%Y', errors='coerce')

# Visualizations
def main():
    st.title("East Haven Business Analysis")

    # Set up the sidebar
    st.sidebar.title("Options")

    # Sidebar option for selecting visualization
    visualization_option = st.sidebar.selectbox(
        "Select Visualization",
        ("Welcome to Our Project!", "Most Common Business Types", "Trends in New Business Registrations", "Comparison of Business Statuses Over Time", "Distribution of Business Types by Ownership Characteristics", "Map", "Industries")
    )





    # Main section
    if visualization_option == "Welcome to Our Project!":
            # Header
        st.header("Welcome to Our Project!")
        st.write("For our Data Vis project, we decided to explore the business landscape in East Haven, CT. As business majors, it's very important for us to understand the intricacies of the different markets in our area. Our motivation behind researching this topic revolved around being intrigued by understanding the landscape of businesses in Connecticut. Analyzing business registry data can provide insights into the types of businesses, their distribution across regions, and their overall impact on employment and economic growth.")
        st.write("We hope you enjoy (and learn something)!")

    elif visualization_option == "Most Common Business Types":
        # Question 1: Most common types of businesses registered in EH
        st.subheader("Most Common Types of Businesses Registered in EH")
        business_types = data['BUS TYPE'].value_counts()
        st.bar_chart(business_types)

    elif visualization_option == "Trends in New Business Registrations":
        # Question 4: Trends in new business registrations over the past decade
        st.subheader("Trends in New Business Registrations Over the Past Decade")

        # Filter active businesses
        active_businesses = data[data['STATUS'] == 'Active']

        # Extract year from 'REGISTRATION DATE'
        active_businesses['Year'] = active_businesses['REGISTRATION DATE'].dt.year

        # Filter data for the past decade
        current_year = pd.Timestamp.now().year
        past_decade_data = active_businesses[(active_businesses['Year'] >= current_year - 10) & (active_businesses['Year'] <= current_year)]

        # Group by year and count new registrations
        new_registrations = past_decade_data.groupby('Year').size()

        # Plot the trends
        plt.figure(figsize=(10, 6))
        plt.plot(new_registrations.index, new_registrations.values, marker='o')
        plt.xlabel('Year')
        plt.ylabel('Number of New Registrations')
        plt.title('Trends in New Business Registrations Over the Past Decade')
        st.pyplot()

    elif visualization_option == "Comparison of Business Statuses Over Time":
        # Question 6: Comparison of business statuses over time
        st.subheader("Comparison of Business Statuses Over Time")

        # Extract year from 'REGISTRATION DATE'
        data['Year'] = data['REGISTRATION DATE'].dt.year

        # Group by year and count statuses
        status_counts = data.groupby(['Year', 'STATUS']).size().unstack(fill_value=0)

        # Get list of unique status keywords
        status_keywords = status_counts.columns.tolist()

        # Radio button for selecting display option
        display_option = st.radio("Display Option", ("Separate Lines", "All Lines Together"))

        if display_option == "Separate Lines":
            # Radio button for selecting status keyword
            selected_status = st.radio("Select Status", status_keywords)

            # Plot the selected status
            plt.figure(figsize=(10, 6))
            plt.plot(status_counts.index, status_counts[selected_status], marker='o')
            plt.xlabel('Year')
            plt.ylabel('Number of Businesses')
            plt.title(f'Comparison of Business Statuses Over Time: {selected_status}')
            st.pyplot()
        else:
            # Plot all lines together
            plt.figure(figsize=(10, 6))
            for column in status_counts.columns:
                plt.plot(status_counts.index, status_counts[column], marker='o', label=column)
            plt.xlabel('Year')
            plt.ylabel('Number of Businesses')
            plt.title('Comparison of Business Statuses Over Time: All Lines Together')
            plt.legend()
            st.pyplot()

    elif visualization_option == "Distribution of Business Types by Ownership Characteristics":
        demographic_categories = data.columns[-5:]

# Display radio buttons to select a demographic category
        selected_category = st.radio("Select a demographic category", demographic_categories)
# Calculate counts of True values for the selected category
        true_counts = data[selected_category].value_counts()

# Plot the result
        fig = go.Figure(go.Bar(
           x=true_counts.index,
            y=true_counts.values,
            text=true_counts.values,
           textposition='auto',
           marker_color=['blue', 'pink']  # Green for True, Red for False
))

        fig.update_layout(
            title=f"Number of Businesses with True Values for {selected_category}",
           xaxis_title="True/False",
           yaxis_title="Count",
           template='plotly_white'
)

        st.plotly_chart(fig)

    elif visualization_option == "Map":
        # Create a DataFrame with latitude and longitude values for each plot point
        map_data = pd.DataFrame({
            'latitude': [41.2769635, 41.2779489, 41.321269, 41.3221245, 41.2923771, 41.274841, 41.3198516, 41.2825023, 41.3186952, 41.2815203, 41.2676504, 41.2610875, 41.3235421, 41.272753, 41.2830810, 41.3206622, 41.278407, 41.2779026, 41.2838507, 41.3295974, 41.2464493, 41.2809961, 41.324997, 41.2808243, 41.2807047, 41.3208578, 41.3288204, 41.2478531, 41.3147466, 41.283659, 41.2705685, 41.256254, 41.2796166, 41.2647843, 41.2821227],
            'longitude': [-72.8615908, -72.8725686, -72.8497132, -72.8659915, -72.8699458, -72.8753109, -72.8575243, -72.877294, -72.8642667, -728855425, -72.8775402, -72.8584114, -72.8417504, -72.8762529, -72.8670057, -72.8598195, -72.8734337, -72.8915958, -72.8827028, -72.8566749, -72.8643557, -72.8651408, -72.858951, -72.8768381, -72.8649318, -72.8586249, -72.8387787, -72.8747727, -72.842654, -72.883565, -72.8746741, -72.8759345, -72.8756138, -72.8704618, -72.8865424]
        })

        # Create a map with the plot points
        st.map(map_data)


    elif visualization_option == "Industries":
        labels = 'Other', 'Entertainment', 'Real Estate', 'Various Medical', 'Beauty', 'Construction', 'Retail'
        sizes = [534, 913, 455, 1652, 1251, 305, 1878]
        explode = (0, 0, 0, 0, 0, 0, 0)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig1)

# Call the main function
if __name__ == "__main__":
    main()

