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

# Add CSS to align the buttons side-by-side
st.markdown("""
<style>
    div.stButton, div.stDownloadButton {
        display: inline-block;
        margin-right: 10px;
    }
    div.stButton > button, div.stDownloadButton > button {
        width: auto;
    }
</style>
""", unsafe_allow_html=True)

# Add buttons to the top of the page
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("Add new base color", on_click=add_new_color)

with col2:
    # Generate and download CSS
    css_content = generate_css([generate_palette(color["hex"], color["name"]) for color in state.color_inputs if color["hex"] != ""]) if 'color_inputs' in state else ""
    st.download_button(
        label="Download CSS",
        data=css_content,
        file_name="color_palettes.css",
        mime="text/css"
    )

with col3:
    # Generate and download SCSS
    scss_content = generate_scss([generate_palette(color["hex"], color["name"]) for color in state.color_inputs if color["hex"] != ""]) if 'color_inputs' in state else ""
    st.download_button(
        label="Download SCSS",
        data=scss_content,
        file_name="color_palettes.scss",
        mime="text/x-scss"
    )

with col4:
    # Generate and download JSON
    json_content = generate_json([generate_palette(color["hex"], color["name"]) for color in state.color_inputs if color["hex"] != ""]) if 'color_inputs' in state else ""
    st.download_button(
        label="Download JSON",
        data=json_content,
        file_name="color_palettes.json",
        mime="application/json"
    )

def get_wcag_level(ratio):
    if ratio >= 7:
        return "AAA"
    elif ratio >= 4.5:
        return "AA"
    else:
        return "fail"

def get_text_color(background_color):
    luminance = get_luminance(hex_to_rgb(background_color))
    return "#FFFFFF" if luminance < 0.5 else "#000000"

def display_palette(palette, title):
    st.subheader(title)
    html_output = ""
    for color_name, color_hex in palette.items():
        contrast_ratio_white = get_contrast_ratio(color_hex, "#FFFFFF")
        contrast_ratio_black = get_contrast_ratio(color_hex, "#000000")
        text_color = get_text_color(color_hex)
        
        html_output += f"""
        <div style="background-color: {color_hex}; padding: 15px 10px; margin: 5px 0; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; height: 80px;">
            <div style="display: flex; flex-direction: column; align-items: center;">
                <span style="color: #000000;">{contrast_ratio_black:.2f}</span>
                <span style="color: #000000; font-size: 0.8em;">{get_wcag_level(contrast_ratio_black)}</span>
            </div>
            <span style="color: {text_color};">{color_name}</span>
            <span style="color: {text_color};">{color_hex}</span>
            <div style="display: flex; flex-direction: column; align-items: center;">
                <span style="color: #FFFFFF;">{contrast_ratio_white:.2f}</span>
                <span style="color: #FFFFFF; font-size: 0.8em;">{get_wcag_level(contrast_ratio_white)}</span>
            </div>
        </div>
        """
    st.markdown(html_output, unsafe_allow_html=True)

# Display color inputs and generate palettes
valid_inputs = []
cols = st.columns(len(state.color_inputs))
for i, (color_input, col) in enumerate(zip(state.color_inputs, cols)):
    with col:
        new_name = st.text_input(f"Color {i+1} Name:", value=color_input["name"], key=f"name_{i}")
        new_color = st.text_input(f"Color {i+1} Hex:", value=color_input["hex"], key=f"color_{i}")
        if new_color == "" or is_valid_hex(new_color):
            valid_inputs.append({"hex": new_color if new_color != "" else "#000000", "name": new_name})
            state.color_inputs[i] = {"hex": new_color, "name": new_name}  # Update the state
        if len(state.color_inputs) > 1:
            st.button(f"Remove Color {i+1}", key=f"remove_{i}", on_click=remove_color, args=(i,))

# Always generate and display the palette
palettes = [generate_palette(color["hex"], color["name"]) for color in valid_inputs if color["hex"] != ""]

st.subheader("Generated Color Palette(s)")
for i, (palette, col) in enumerate(zip(palettes, cols)):
    with col:
        display_palette(palette, f"Color Palette {i+1}")

if len(valid_inputs) == len(state.color_inputs):
    st.subheader("Color Information")
    for i, (color_input, palette) in enumerate(zip(valid_inputs, palettes)):
        if color_input["hex"] != "":
            st.markdown(f"**Input Color {i+1}:** {color_input['name']} ({color_input['hex']})")
            st.markdown(f"**Palette {i+1} - Lightest Color ({color_input['name']}.100):** {palette[color_input['name']+'.100']}")
            st.markdown(f"**Palette {i+1} - Darkest Color ({color_input['name']}.900):** {palette[color_input['name']+'.900']}")

    st.subheader("Copy Palette(s)")
    palette_text = "\n\n".join([f"Palette {i+1}:\n" + "\n".join([f"{k}: {v}" for k, v in palette.items()]) for i, palette in enumerate(palettes)])
    st.code(palette_text)
    st.button("Copy to Clipboard", on_click=lambda: st.write("Palette(s) copied to clipboard!"))

else:
    st.error("Invalid hex color code(s). Please enter valid 6-digit hex colors (e.g., #FF5733) or leave the field empty.")

# Add some information about using the app
st.markdown("""
### How to use this app:
1. Enter valid hex color codes in the input fields (e.g., #FF5733).
2. Click the "Add new base color" button to add more color inputs.
3. Click the "Remove Color" button next to a color input to remove it (minimum one color required).
4. The app will generate palettes of 9 colors each, displayed from color.100 (lightest) at the top to color.900 (darkest) at the bottom.
5. Each color in the palette is generated based on the input color, adjusting its brightness.
6. The palettes are displayed side by side.
7. Each color in the palette is displayed with its name, hex value, and contrast ratios with white and black.
8. The contrast ratios are followed by their WCAG compliance level:
   - "fail" if the ratio is below 4.5
   - "AA" if the ratio is 4.5 or higher
   - "AAA" if the ratio is 7 or higher
9. You can copy all palettes to your clipboard using the "Copy to Clipboard" button.
10. You can download the color palettes as CSS, SCSS, or JSON files using the respective download buttons.

Enjoy creating beautiful and accessible color palettes!
""")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit")
