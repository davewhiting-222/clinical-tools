import os
from bs4 import BeautifulSoup

# Configuration
HANDOUTS_DIR = '.'  # Set this to the subfolder if your handouts are in one
INDEX_FILE = 'index.html'
EXCLUDE_FILES = [INDEX_FILE, 'generate_index.py']

def get_html_title(filepath):
    """Extracts the <title> tag from an HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup.title.string if soup.title else filepath
    except Exception:
        return filepath

def generate_index():
    files = [f for f in os.listdir(HANDOUTS_DIR) 
             if f.endswith('.html') and f not in EXCLUDE_FILES]
    
    # Sort files alphabetically
    files.sort()

    links_html = ""
    for file in files:
        title = get_html_title(os.path.join(HANDOUTS_DIR, file))
        links_html += f'        <li><a href="{file}">{title}</a></li>\n'

    # The HTML Template
    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Patient Handouts Index</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: auto; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ margin: 10px 0; padding: 10px; background: #f9f9f9; border-radius: 5px; }}
        a {{ text-decoration: none; color: #3498db; font-weight: bold; }}
        a:hover {{ color: #2980b9; }}
    </style>
</head>
<body>
    <h1>Patient Information Handouts</h1>
    <p>Please select a handout from the list below:</p>
    <ul>
{links_html}
    </ul>
    <footer>
        <p><small>Last updated: {os.popen('date').read().strip()}</small></p>
    </footer>
</body>
</html>"""

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(template)
    print(f"Successfully updated {INDEX_FILE}")

if __name__ == "__main__":
    generate_index()
