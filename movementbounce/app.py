import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit App
def main():
    st.title("Bowling Analysis: Mean Movement vs Mean Bounce Per Length")

    # Add a button to generate the graph
    if st.button('Generate Graph'):
        # Load the data
        data = pd.read_csv('restrictedcounty.csv')

        # Filter out certain bowler types
        filtered_data = data[~data['Bowler Type'].isin(['RLB', 'ROB', 'LOB'])]
        filtered_data['Bounce Per Length'] = filtered_data['PastZ'] / filtered_data['PitchX']
        filtered_data['Movement'] = abs(filtered_data['PastY'] - filtered_data['PitchY'])

        # Get a list of unique bowlers
        bowlers = filtered_data['Bowler'].unique().tolist()

        # Calculate average movement and bounce per length for each entry
        for index, row in filtered_data.iterrows():
            date = row['Date']
            match = row['Match']
            innings = row['Innings']

            df = filtered_data[(filtered_data['Date'] == date) & 
                               (filtered_data['Match'] == match) & 
                               (filtered_data['Innings'] == innings)]

            # Calculate the mean values
            avg_movement = df['Movement'].mean()
            avg_bpl = df['Bounce Per Length'].mean()

            filtered_data.loc[index, 'Average Movement'] = avg_movement
            filtered_data.loc[index, 'Average BPL'] = avg_bpl

        # Calculate differences from averages
        filtered_data['BPL vs Avg'] = filtered_data['Bounce Per Length'] - filtered_data['Average BPL']
        filtered_data['Movement vs Avg'] = filtered_data['Movement'] - filtered_data['Average Movement']

        # Initialize lists to store mean values for each bowler
        mean_movement = []
        mean_bpl = []

        # Calculate the mean movement and bounce per length differences for each bowler
        for i in bowlers:
            fd = filtered_data[filtered_data['Bowler'] == i]
            mean_bpl.append(fd['BPL vs Avg'].mean())
            mean_movement.append(fd['Movement vs Avg'].mean())

        # Create a DataFrame to store the results
        result_df = pd.DataFrame({
            'Bowler': bowlers,
            'Mean Bounce Per Length': mean_bpl,
            'Mean Movement': mean_movement
        })

        # Create the plot using Plotly Express
        fig = px.scatter(result_df,
                         x='Mean Movement', 
                         y='Mean Bounce Per Length', 
                         hover_data=['Bowler'],  # Add bowler's name to hover info
                         title="Mean Movement vs Mean Bounce Per Length", 
                         width=1920, height=1080
                         )
        
        fig.add_shape(
            type="line",
            x0=0, x1=0, 
            y0=result_df['Mean Bounce Per Length'].min(), 
            y1=result_df['Mean Bounce Per Length'].max(),
            line=dict(color="rgba(255, 0, 0, 0.5)", width=2, dash="dot")  # Red line with 50% opacity
        )

        fig.add_shape(
            type="line",
            x0=result_df['Mean Movement'].min(), 
            x1=result_df['Mean Movement'].max(), 
            y0=0, y1=0,
            line=dict(color="rgba(255, 0, 0, 0.5)", width=2, dash="dot")  # Blue line with 50% opacity
        
        )
        
        fig.add_annotation(
            x=result_df['Mean Movement'].min(), 
            y=result_df['Mean Bounce Per Length'].max(), 
            text="Good Bounce, Bad Movement", 
            showarrow=False, 
            xanchor="left", 
            yanchor="top",
            font=dict(size=12, color="black")
        )

        fig.add_annotation(
            x=result_df['Mean Movement'].max(), 
            y=result_df['Mean Bounce Per Length'].max(), 
            text="Good Bounce, Good Movement", 
            showarrow=False, 
            xanchor="right", 
            yanchor="top",
            font=dict(size=12, color="black")
        )

        fig.add_annotation(
            x=result_df['Mean Movement'].min(), 
            y=result_df['Mean Bounce Per Length'].min(), 
            text="Bad Bounce, Bad Movement", 
            showarrow=False, 
            xanchor="left", 
            yanchor="bottom",
            font=dict(size=12, color="black")
        )

        fig.add_annotation(
            x=result_df['Mean Movement'].max(), 
            y=result_df['Mean Bounce Per Length'].min(), 
            text="Bad Bounce, Good Movement", 
            showarrow=False, 
            xanchor="right", 
            yanchor="bottom",
            font=dict(size=12, color="black")
        )

        # Display the plot
        st.plotly_chart(fig)

if __name__ == '__main__':
    main()
