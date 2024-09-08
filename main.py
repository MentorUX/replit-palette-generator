import streamlit as st
from streamlit import session_state as state
from color_utils import generate_palette, is_valid_hex, get_contrast_ratio, hex_to_rgb, get_luminance
import json
from streamlit.components.v1 import html

st.set_page_config(page_title="Color Palette Generator", page_icon="🎨", layout="wide")

st.title("🌈 Color Palette Generator")

st.markdown("""
This app generates color palettes from color.100 (lightest) to color.900 (darkest) based on your input color(s).
Enter hex color codes (e.g., #FF5733) in the input fields below to get started!
""")

# Initialize the state for color inputs if it doesn't exist
if 'color_inputs' not in state:
    state.color_inputs = [{"hex": "#4287f5", "name": "Blue"}]

def add_new_color():
    state.color_inputs.append({"hex": "#aaaaaa", "name": "Gray"})
    state.color_inputs = state.color_inputs  # Trigger a rerun

def remove_color(index):
    if len(state.color_inputs) > 1:
        del state.color_inputs[index]
        state.color_inputs = state.color_inputs  # Trigger a rerun

def generate_css(palettes):
    css = ":root {\n"
    for i, palette in enumerate(palettes):
        for color_name, color_hex in palette.items():
            css += f"  --{color_name.replace('.', '-')}: {color_hex};\n"
    css += "}\n"
    return css

def generate_scss(palettes):
    scss = ""
    for i, palette in enumerate(palettes):
        scss += f"$palette-{i+1}: (\n"
        for color_name, color_hex in palette.items():
            scss += f"  '{color_name}': {color_hex},\n"
        scss = scss.rstrip(',\n') + "\n);\n\n"
    return scss

def generate_json(palettes):
    json_data = {}
    for palette in palettes:
        color_name = next(iter(palette)).split('.')[0]  # Get the base color name
        json_data[color_name] = {}
        for full_color_name, color_hex in palette.items():
            shade = full_color_name.split('.')[1]
            json_data[color_name][shade] = {
                "value": color_hex,
                "type": "color"
            }
    return json.dumps(json_data, indent=2)

# Update CSS to improve button layout
st.markdown("""
<style>
    div.stButton, div.stDownloadButton {
        display: inline-block;
        margin-right: 10px;
    }
    div.stButton > button, div.stDownloadButton > button {
        width: auto;
        padding: 0.25rem 0.75rem;
        font-size: 0.8rem;
        line-height: 1.5;
    }
    .stApp > header {
        background-color: transparent;
    }
    .main .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Create a single row for buttons
button_col = st.columns(4)

with button_col[0]:
    st.button("Add new base color", on_click=add_new_color)

with button_col[1]:
    # Generate and download CSS
    css_content = generate_css([generate_palette(color["hex"], color["name"]) for color in state.color_inputs if color["hex"] != ""]) if 'color_inputs' in state else ""
    st.download_button(
        label="Download CSS",
        data=css_content,
        file_name="color_palettes.css",
        mime="text/css"
    )

with button_col[2]:
    # Generate and download SCSS
    scss_content = generate_scss([generate_palette(color["hex"], color["name"]) for color in state.color_inputs if color["hex"] != ""]) if 'color_inputs' in state else ""
    st.download_button(
        label="Download SCSS",
        data=scss_content,
        file_name="color_palettes.scss",
        mime="text/x-scss"
    )

with button_col[3]:
    # Generate and download JSON
    json_content = generate_json([generate_palette(color["hex"], color["name"]) for color in state.color_inputs if color["hex"] != ""]) if 'color_inputs' in state else ""
    st.download_button(
        label="Download JSON",
        data=json_content,
        file_name="color_palettes.json",
        mime="application/json"
    )

# ... (rest of the code remains unchanged)
