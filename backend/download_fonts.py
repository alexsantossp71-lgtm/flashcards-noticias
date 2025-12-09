"""
Download Montserrat font from Google Fonts
Run this script to download the font files
"""
import urllib.request
import os

# Create fonts directory if it doesn't exist
os.makedirs('fonts', exist_ok=True)

# Download Montserrat Bold
urls = {
    'Montserrat-Bold.ttf': 'https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Bold.ttf',
    'Montserrat-Regular.ttf': 'https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Regular.ttf'
}

for filename, url in urls.items():
    filepath = os.path.join('fonts', filename)
    try:
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filepath)
        print(f"✓ Downloaded {filename}")
    except Exception as e:
        print(f"✗ Failed to download {filename}: {e}")

print("\nDone!")
