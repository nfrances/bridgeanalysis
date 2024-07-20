import streamlit as st
import pycba as cba  # Ensure pycba is installed
import numpy as np  # For arrays
import plotly.graph_objects as go



# Set Streamlit page
if __name__ == '__main__':
    st.set_page_config(page_title="Beam Analysis App")
    st.write("# Welcome to Beam Analysis App")
    st.write("Use the inputs below to perform a beam analysis.")
col1, col2 = st.columns(2)

with col1:
    # Input for # of spans
    num_spans = st.selectbox('Num. of Spans', list(range(1,21)))
    
    # Input for span lengths
    span_lengths = []
    for i in range(num_spans):
        span_length = st.text_input(f'Length of Span {i+1}', '20.0')
        span_lengths.append(float(span_length))

with col2:

    # Input for EI
    EI_input = st.text_input("Enter EI (single value)", "180000000")
    EI = [float(span.strip()) for span in EI_input.split(",")]

# Define a function for the beam analysis
def analyze_beam(span_lengths, EI):
    R = [-1, 1, 0, 0, 0, 0]
    beam_analysis = cba.BeamAnalysis(span_lengths, EI, R)
    beam_analysis.add_udl(i_span=1, w=20)
    beam_analysis.add_udl(i_span=2, w=20)
    beam_analysis.analyze()
    max = beam_analysis.beam_results.vRes[0].M.max()

    fig = go.Figure()

    # Extracting results for plotting
    for span in range(num_spans):
        x = beam_analysis.beam_results.vRes[span].x
        x = x[1:-1]
        Moment = beam_analysis.beam_results.vRes[span].M
        Moment = Moment[1:-1]
        fig.add_trace(go.Scatter(x=x, y=Moment, mode='lines', name=f'Span {span + 1}',
                                 hovertemplate="Position: %{x:.2f} m<br>Bending Moment: %{y:.2f} kNm<br>"))
        
    
    fig.update_layout(title="Bending Moment Diagram",
                      xaxis_title="Position (m)",
                      yaxis_title="Bending Moment (kNm)")
    
    return max, fig

# Button to trigger analysis
if st.button("Analyze Beam"):
    try:
        # Perform beam analysis
        max, fig = analyze_beam(span_lengths, EI)
        st.plotly_chart(fig)
        st.success(f"Maximum Bending Moment: {max}")        
        
    except Exception as e:
        st.error(f"Error: {e}")
