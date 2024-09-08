import streamlit as st
from streamlit import session_state as state
from color_utils import generate_palette, is_valid_hex, get_contrast_ratio, hex_to_rgb, get_luminance
import json

st.set_page_config(page_title="Color Palette Generator", page_icon="🎨", layout="wide")
st.title("🌈 Color Palette Generator")
st.markdown('''
This app generates color palettes from color.100 (lightest) to color.900 (darkest) based on your input color(s).
Enter hex color codes (e.g., #FF5733) in the input fields below to get started!
''')

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
        scss = scss.rstrip(',\n') + "\n);\n"
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

# Move the "Add new base color" button to the top of the page
st.button("Add new base color", on_click=add_new_color)

# Create columns for each color input
cols = st.columns(len(state.color_inputs))

# Display color inputs and generate palettes
for i, (col, color_input) in enumerate(zip(cols, state.color_inputs)):
    with col:
        color_input["hex"] = st.text_input(f"Base Color {i+1} (Hex)", color_input["hex"], key=f"hex_{i}")
        color_input["name"] = st.text_input(f"Color Name {i+1}", color_input["name"], key=f"name_{i}")
        
        if len(state.color_inputs) > 1:
            st.button(f"Remove Color {i+1}", on_click=remove_color, args=(i,), key=f"remove_{i}")
        
        if is_valid_hex(color_input["hex"]):
            palette = generate_palette(color_input["hex"], color_input["name"])
            
            # Display color palette
            st.write(f"### {color_input['name']} Palette")
            for color_name, color_hex in palette.items():
                # Calculate contrast ratios
                contrast_white = get_contrast_ratio(color_hex, "#FFFFFF")
                contrast_black = get_contrast_ratio(color_hex, "#000000")
                
                # Determine text color based on contrast
                text_color = "#FFFFFF" if contrast_white > contrast_black else "#000000"
                
                st.markdown(f'''
                <div style='background-color: {color_hex}; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>
                    <p style='color: {text_color}; margin: 0;'>{color_name}: {color_hex}</p>
                    <p style='color: {text_color}; margin: 0; font-size: 0.8em;'>
                        White: {contrast_white:.2f} ({'AAA' if contrast_white >= 7 else 'AA' if contrast_white >= 4.5 else 'Fail'})
                        Black: {contrast_black:.2f} ({'AAA' if contrast_black >= 7 else 'AA' if contrast_black >= 4.5 else 'Fail'})
                    </p>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.error(f"Invalid hex color for Base Color {i+1}. Please enter a valid hex color (e.g., #FF5733).")

# Generate and download buttons
css_content = generate_css([generate_palette(color["hex"], color["name"]) for color in state.color_inputs if color["hex"] != ""]) if 'color_inputs' in state else ""
scss_content = generate_scss([generate_palette(color["hex"], color["name"]) for color in state.color_inputs if color["hex"] != ""]) if 'color_inputs' in state else ""
json_content = generate_json([generate_palette(color["hex"], color["name"]) for color in state.color_inputs if color["hex"] != ""]) if 'color_inputs' in state else ""

st.download_button(
    label="Download CSS",
    data=css_content,
    file_name="color_palettes.css",
    mime="text/css"
)

st.download_button(
    label="Download SCSS",
    data=scss_content,
    file_name="color_palettes.scss",
    mime="text/x-scss"
)

st.download_button(
    label="Download JSON",
    data=json_content,
    file_name="color_palettes.json",
    mime="application/json"
)

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
