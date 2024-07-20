import streamlit as st
from sectionproperties.analysis import Section
from sectionproperties.pre.library import mono_i_section


# Set Streamlit page
if __name__ == '__main__':
    st.set_page_config(page_title="Section Properties")
    st.write("Define Section")

# Inputs
sect_name = st.text_input("Enter Name for Section")
shape = st.radio("Beam Shape", ["I-Beam (Steel)", "I-Beam (Concrete)", "Box Beam (Concrete)", "Open Box Girder (Steel)","Tee Beam", "Rectangular Solid"])
if shape == "I-Beam (Steel)":
    h = st.number_input("Total Height", min_value = 0, value = 36)
    tf_w = st.number_input("Top Flange Width", min_value = 0, value = 10)
    bf_w = st.number_input("Bottom Flange Width", min_value = 0, value = 10)
    tf_t = st.number_input("Top Flange Thickness", min_value = 0, value = 2)
    bf_t = st.number_input("Bottom Flange Thickness", min_value = 0, value = 2)
    t_w = st.number_input("Web Thickness", min_value=0, value=1)
else:
    st.write("fail")

geometry = mono_i_section(d=h, b_t=tf_w, b_b=bf_w, t_ft=tf_t, t_fb=bf_t, t_w=t_w).plot_geometry()
