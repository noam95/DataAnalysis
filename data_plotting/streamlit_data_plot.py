import streamlit as st
import plotly.graph_objects as go


def draw_histogram(data):
    st.subheader('Raw data')
    print(data)
    st.subheader('Number of pickups by hour')
    st.dataframe(data)
    # hist_values = np.histogram(
    #     data['datetime']  , bins=24, range=(0, 24))[0]
    # st.bar_chart(hist_values)
    st.line_chart(
        data,
        x='time',  # The name of the column to use for the x axis.
        y='bpm',  # The name of the column to use for the data itself.
        # color='stock_name',  # The name of the column to use for the line colors.
    )

def plotly_histogram(data):
    fig = go.Figure(go.Scatter(x=data['time'], y=data['bpm'], mode='lines+markers'))

    # Set axis labels
    fig.update_layout(xaxis_title='X-Axis', yaxis_title='Y-Axis')

    # Enable zooming, panning, and grabbing functionality
    fig.update_layout(dragmode='zoom', hovermode='x unified', autosize=True)

    # Show the figure
    fig.show()


#
def plot_data_on_map(data):
    st.subheader('Map of all pickups')
    st.map(data)
    st.subheader('Map of all pickups')
    st.map(data)
    hour_to_filter = 17
    filtered_data = data[data['bpm'] == hour_to_filter]
    st.subheader(f'Map of all pickups at {hour_to_filter}:00')
    st.map(filtered_data)


#
def filter_resault_with_slider(data):
    hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h


#
#

