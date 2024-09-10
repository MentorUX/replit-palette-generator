import colorsys
import json

def hex_to_rgb(hex_color):
    """Convert hex color to RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB color to hex."""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def blend_colors(color1, color2, ratio):
    """Blend two colors based on the given ratio."""
    return tuple(int(color1[i] * (1 - ratio) + color2[i] * ratio) for i in range(3))

def generate_palette(hex_color, color_name):
    """Generate a color palette from color.100 to color.900."""
    base_color = hex_to_rgb(hex_color)
    white = (255, 255, 255)
    black = (0, 0, 0)
    palette = {}

    # Generate lighter colors (color.100 to color.400)
    for i in range(1, 5):
        blend_ratio = 0.8 - (i - 1) * 0.2
        palette[f'{color_name}.{i}00'] = rgb_to_hex(blend_colors(base_color, white, blend_ratio))

    # color.500 is the base color
    palette[f'{color_name}.500'] = hex_color

    # Generate darker colors (color.600 to color.900)
    for i in range(6, 10):
        blend_ratio = (i - 5) * 0.2
        palette[f'{color_name}.{i}00'] = rgb_to_hex(blend_colors(base_color, black, blend_ratio))

    return palette

def is_valid_hex(hex_color):
    """Check if the input is a valid hex color."""
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    return len(hex_color) == 6 and all(c in '0123456789ABCDEFabcdef' for c in hex_color)

def get_luminance(rgb):
    rgb = [v / 255.0 for v in rgb]
    rgb = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]

def get_contrast_ratio(color1, color2):
    lum1 = get_luminance(hex_to_rgb(color1))
    lum2 = get_luminance(hex_to_rgb(color2))
    brightest = max(lum1, lum2)
    darkest = min(lum1, lum2)
    return (brightest + 0.05) / (darkest + 0.05)

def get_contrast_status(ratio):
    """Get the contrast status based on WCAG guidelines."""
    if ratio >= 7:
        return "AAA"
    elif ratio >= 4.5:
        return "AA"
    else:
        return "FAIL"

def get_text_color(bg_color):
    """Get the appropriate text color (black or white) based on the background color."""
    rgb = hex_to_rgb(bg_color)
    luminance = get_luminance(rgb)
    return "#000000" if luminance > 0.5 else "#FFFFFF"

def generate_css(palettes):
    """Generate CSS content for the color palettes."""
    css = ":root {\n"
    for palette in palettes:
        for color_name, color_hex in palette.items():
            css += f"  --{color_name.replace('.', '-')}: {color_hex};\n"
    css += "}\n"
    return css

def generate_scss(palettes):
    """Generate SCSS content for the color palettes."""
    scss = ""
    for i, palette in enumerate(palettes):
        scss += f"$palette-{i+1}: (\n"
        for color_name, color_hex in palette.items():
            scss += f"  '{color_name}': {color_hex},\n"
        scss = scss.rstrip(',\n') + "\n);\n"
    return scss

def generate_json(palettes):
    """Generate JSON content for the color palettes."""
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
