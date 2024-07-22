import streamlit as st
from sectionproperties.analysis import Section
from sectionproperties.pre.library import mono_i_section
import plotly.graph_objects as go
import numpy as np

# Set Streamlit page
if __name__ == '__main__':
    st.set_page_config(page_title="Section Properties")
    st.write("Define Section")
    col1, col2 = st.columns(2)

with col1:
# Inputs
    sect_name = st.text_input("Enter Name for Section")
    shape = st.radio("Beam Shape", ["I-Beam (Steel)", "I-Beam (Concrete)", "Box Beam (Concrete)", "Open Box Girder (Steel)","Tee Beam", "Rectangular Solid"])
    if shape == "I-Beam (Steel)":
        d = st.number_input("Total Height", min_value = 0, value = 36)
        b_t = st.number_input("Top Flange Width", min_value = 0, value = 10)
        b_b = st.number_input("Bottom Flange Width", min_value = 0, value = 10)
        t_ft = st.number_input("Top Flange Thickness", min_value = 0, value = 2)
        t_fb = st.number_input("Bottom Flange Thickness", min_value = 0, value = 2)
        t_w = st.number_input("Web Thickness", min_value=0, value=1)

        geom = mono_i_section(d=d, b_t=b_t, b_b=b_b, t_ft=t_ft, t_fb=t_fb, t_w=t_w, r=0, n_r=0)
        geom.create_mesh(mesh_sizes=[d/10])
        sec = Section(geometry=geom)
        sec.calculate_geometric_properties()
        A=sec.get_area()

    else:
       st.write("fail")

with col2:
# Create the figure
    points = np.array(geom.points)

    fig = go.Figure()

    if points.size > 0:
        x_points = np.append(points[:, 0], points[0, 0])
        y_points = np.append(points[:, 1], points[0, 1])
        fig.add_trace(go.Scatter(
            x=x_points, 
            y=y_points, 
            mode='markers+lines', 
            fill='toself', 
            line=dict(color='#555656'), 
            fillcolor='#5192ae',
            opacity=1,
            hoverinfo='skip',
            marker=dict(size=1)
        ))

    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
        plot_bgcolor="#ddeaef",
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    fig.layout.annotations = [
      #draw height dimension line
      dict(
          x=-d*0.025,  # arrows' head
          y=d,  # arrows' head
          ax=-d*0.025,  # arrows' tail
          ay=0,  # arrows' tail
          xref='x',
          yref='y',
          axref='x',
          ayref='y',
          text='',  # if you want only the arrow
          showarrow=True,
          arrowhead=3,
          arrowside="end+start",
          arrowsize=1,
          arrowwidth=1,
          arrowcolor='black'
        ),
        #annotate h dimension
        dict(
          text = str(d),
          showarrow = False,
          font=dict(size=14, color="black"),
          textangle = -90,
          xref = 'x',
          x = -d*0.05,
          yref = 'y',
          y = d/2,
        ),
    ]
    config = {'displayModeBar': False}
    st.plotly_chart(fig, use_container_width=True,config=config)

    # # Extract points
    # points = np.array(geom.points)  # Ensure points are in numpy array format

    # fig, ax = plt.subplots()

    # # Assuming points define a closed shape
    # if points.size > 0:
    #     polygon = plt.Polygon(points, closed=True, edgecolor='black', facecolor='#5192ae', alpha=0.75)
    #     ax.add_patch(polygon)

    #     # Plot the points
    #     ax.plot(points[:, 0], points[:, 1], 'ko', markersize=1)  # 'ko' for black circles

    # # Set aspect ratio to be equal
    # ax.set_aspect('equal')

    # # Remove the axes and spines
    # #ax.axis('off')  # Hide the axes
    # for spine in ax.spines.values():
    #     spine.set_visible(False)  # Hide the spines


    # ax.annotate("", xy=(0, d), xytext=(b_t, d), textcoords=ax.transData, arrowprops=dict(arrowstyle='<->'))
    # ax.annotate("", xy=(0, d), xytext=(b_t, d), textcoords=ax.transData, arrowprops=dict(arrowstyle='|-|'))
    # bbox=dict(fc="white", ec="none")
    # ax.text(b_t/2, d, "L=200 m", ha="center", va="center", bbox=bbox)


    # Show the plot in Streamlit

    st.write(A)
