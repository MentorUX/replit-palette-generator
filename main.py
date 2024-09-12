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

# Streamlit app
st.title("Color Palette Generator")

# Add new base color button
if st.button("Add new color"):
    add_color()

# Define the number of columns you want per row (up to 6)
columns_per_row = 6  # Display up to 6 color palettes side-by-side

# Loop through color inputs and display them in columns
for idx in range(0, len(st.session_state.color_inputs), columns_per_row):
    cols = st.columns(min(columns_per_row, len(st.session_state.color_inputs) - idx))  # Create a row of columns

    for i, col in enumerate(cols):
        color_input = st.session_state.color_inputs[idx + i]

        with col:
            # Display user input fields for each color
            st.write(f"## Color {idx + i + 1}")
            color_input["name"] = st.text_input(f"Color Name {idx + i + 1}", color_input["name"], key=f"name_{idx + i}")
            color_input["hex"] = st.color_picker(f"Select Color {idx + i + 1}", color_input["hex"], key=f"color_{idx + i}")
            color_input["hex"] = st.text_input(f"Hex Value {idx + i + 1}", color_input["hex"], key=f"hex_{idx + i}")

            # Remove Color button for each palette
            st.button("Remove Color", key=f"remove_{idx + i}", on_click=remove_color, args=(idx + i,))

            # Generate and display the palette
            if is_valid_hex(color_input["hex"]):
                palette = generate_palette(color_input["hex"], color_input["name"])
                st.write(f"### {color_input['name']} Palette")
                for color_name, color_hex in palette.items():
                    contrast_white = get_contrast_ratio(color_hex, "#FFFFFF")
                    contrast_black = get_contrast_ratio(color_hex, "#000000")
                    white_status = get_contrast_status(contrast_white)
                    black_status = get_contrast_status(contrast_black)
                    text_color = get_text_color(color_hex)

                    # Render the color palette inside the same column
                    st.markdown(f'''
                    <div style='background-color: {color_hex}; padding: 10px; border-radius: 8px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;'>
                        <div style='text-align: left; color: black;'>
                            <div style='font-size: 16px; font-weight: bold;'>{contrast_black:.2f}</div>
                            <div style='font-size: 16px;'>{black_status}</div>
                        </div>
                        <div style='text-align: center; color: {text_color};'>
                            <div style='font-size: 18px; font-weight: bold;'>{color_name}</div>
                            <div style='font-size: 18px;'>{color_hex}</div>
                        </div>
                        <div style='text-align: right; color: white;'>
                            <div style='font-size: 16px; font-weight: bold;'>{contrast_white:.2f}</div>
                            <div style='font-size: 16px;'>{white_status}</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                st.error(f"Invalid hex color for Base Color {idx + i + 1}. Please enter a valid hex color (e.g., #FF5733).")

# Generate and download buttons for CSS, SCSS, and JSON files
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
