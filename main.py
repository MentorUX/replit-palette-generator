import streamlit as st
import colorsys
from PIL import Image, ImageDraw, ImageFont

def hex_to_rgb(hex_color):
    """Convert a hex color to RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB to hex color."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def blend_color(color1, color2, factor):
    """Blend two colors with a given factor."""
    return tuple(int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3))

def generate_palette(base_color):
    """Generate a palette of 9 colors based on the input color."""
    rgb = hex_to_rgb(base_color)
    hsv = colorsys.rgb_to_hsv(*[x/255 for x in rgb])
    
    palette = []
    
    # Generate lighter colors (100-400)
    for i in range(4):
        factor = 0.8 - (i * 0.2)
        light_rgb = blend_color(rgb, (255, 255, 255), factor)
        palette.append(rgb_to_hex(light_rgb))
    
    # Add base color (500)
    palette.append(base_color)
    
    # Generate darker colors (600-900)
    for i in range(4):
        factor = 0.2 + (i * 0.2)
        dark_rgb = blend_color(rgb, (0, 0, 0), factor)
        palette.append(rgb_to_hex(dark_rgb))
    
    return palette

def create_color_image(hex_color, color_name, size=(300, 50)):
    """Create an image of a given color with color name and hex value."""
    img = Image.new('RGB', size, hex_color)
    draw = ImageDraw.Draw(img)
    
    # Use a default font
    font = ImageFont.load_default()
    
    # Calculate text position
    text = f"{color_name}: {hex_color}"
    text_width = draw.textlength(text, font=font)
    text_position = ((size[0] - text_width) // 2, (size[1] - font.size) // 2)
    
    # Determine text color (white for dark backgrounds, black for light backgrounds)
    rgb = hex_to_rgb(hex_color)
    text_color = 'white' if sum(rgb) < 382 else 'black'
    
    # Draw text
    draw.text(text_position, text, font=font, fill=text_color)
    
    return img

def main():
    st.set_page_config(page_title="Color Palette Generator", page_icon="🎨", layout="wide")
    
    st.title("🎨 Color Palette Generator")
    st.write("Enter a hex color value to generate a palette of 9 colors.")

    # User input for hex color
    base_color = st.text_input("Enter a hex color (e.g., #FF5733):", value="#FF5733")
    
    if base_color:
        try:
            # Generate palette
            palette = generate_palette(base_color)
            
            # Display palette
            st.subheader("Generated Palette")
            
            # Create a container for the color blocks
            container = st.container()
            
            # Display color blocks
            for i, color in enumerate(palette):
                color_name = f"color.{(i+1)*100}"
                container.image(create_color_image(color, color_name), use_column_width=True)
            
        except ValueError:
            st.error("Invalid hex color. Please enter a valid hex color (e.g., #FF5733).")

if __name__ == "__main__":
    main()
