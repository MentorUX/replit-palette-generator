import streamlit as st
from color_utils import generate_palette, is_valid_hex, get_contrast_ratio, get_contrast_status, get_text_color, generate_css, generate_scss, generate_json

st.set_page_config(page_title="Color Palette Generator", page_icon="🎨", layout="wide")

# Initialize session state
if 'color_inputs' not in st.session_state:
    st.session_state.color_inputs = [{"name": "blue", "hex": "#4287f5"}]

# Function to add a new color input
def add_color():
    st.session_state.color_inputs.append({"name": f"New Color {len(st.session_state.color_inputs) + 1}", "hex": "#aaaaaa"})

# Function to remove a color input
def remove_color(index):
    st.session_state.color_inputs.pop(index)
    st.rerun()

# Streamlit app
st.title("Color Palette Generator")

# Add new base color button
if st.button("Add new color"):
    add_color()

# Display color inputs and generate palettes
for i, color_input in enumerate(st.session_state.color_inputs):
    with st.container():
        st.write(f"## Color {i + 1}")
        color_input["name"] = st.text_input(f"Color Name {i + 1}", color_input["name"], key=f"name_{i}")
        color_input["hex"] = st.color_picker(f"Select Color {i + 1}", color_input["hex"], key=f"color_{i}")
        
        # Move 'Remove Color' button to a new line below the color name
        if st.button("Remove Color", key=f"remove_{i}"):
            remove_color(i)
            st.rerun()

        if is_valid_hex(color_input["hex"]):
            palette = generate_palette(color_input["hex"], color_input["name"])
            
            # Display color palette
            st.write(f"### {color_input['name']} Palette")
            for color_name, color_hex in palette.items():
                # Calculate contrast ratios
                contrast_white = get_contrast_ratio(color_hex, "#FFFFFF")
                contrast_black = get_contrast_ratio(color_hex, "#000000")
                
                # Get contrast status
                white_status = get_contrast_status(contrast_white)
                black_status = get_contrast_status(contrast_black)
                
                # Get text color based on background
                text_color = get_text_color(color_hex)
                
                st.markdown(f'''
                <div style='background-color: {color_hex}; padding: 10px; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;'>
                    <div style='text-align: left; color: black;'>
                        <div style='font-size: 16px; font-weight: bold;'>{contrast_black:.2f}</div>
                        <div style='font-size: 16px;'>{black_status}</div>
                    </div>
                    <div style='text-align: center; color: {text_color};'>
                        <div style='font-size: 28px; font-weight: bold;'>{color_name}</div>
                        <div style='font-size: 20px;'>{color_hex}</div>
                    </div>
                    <div style='text-align: right; color: white;'>
                        <div style='font-size: 24px; font-weight: bold;'>{contrast_white:.2f}</div>
                        <div style='font-size: 16px;'>{white_status}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.error(f"Invalid hex color for Color {i + 1}. Please enter a valid hex color (e.g., #FF5733).")

# Generate and download buttons
if st.session_state.color_inputs:
    css_content = generate_css([generate_palette(color["hex"], color["name"]) for color in st.session_state.color_inputs if color["hex"] != ""])
    scss_content = generate_scss([generate_palette(color["hex"], color["name"]) for color in st.session_state.color_inputs if color["hex"] != ""])
    json_content = generate_json([generate_palette(color["hex"], color["name"]) for color in st.session_state.color_inputs if color["hex"] != ""])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.download_button(
            label="Download CSS",
            data=css_content,
            file_name="color_palettes.css",
            mime="text/css"
        )

    with col2:
        st.download_button(
            label="Download SCSS",
            data=scss_content,
            file_name="color_palettes.scss",
            mime="text/x-scss"
        )

    with col3:
        st.download_button(
            label="Download JSON",
            data=json_content,
            file_name="color_palettes.json",
            mime="application/json"
        )

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
