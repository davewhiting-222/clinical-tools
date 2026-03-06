import os
from bs4 import BeautifulSoup

# Configuration
HANDOUTS_DIR = '.' 
INDEX_FILE = 'index.html'
EXCLUDE_FILES = [INDEX_FILE, 'generate_index.py', 'requirements.txt']

def get_metadata(filepath):
    """Extracts title and category from HTML."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            title = soup.title.string if soup.title else filepath
            # Look for <meta name="category" content="...">
            cat_tag = soup.find('meta', attrs={'name': 'category'})
            category = cat_tag['content'] if cat_tag else "Uncategorized"
            return title, category
    except Exception:
        return filepath, "Uncategorized"

def generate_index():
    files = [f for f in os.listdir(HANDOUTS_DIR) 
             if f.endswith('.html') and f not in EXCLUDE_FILES]
    
    # Build a list of dictionaries for easier sorting
    handouts = []
    for file in files:
        title, category = get_metadata(os.path.join(HANDOUTS_DIR, file))
        handouts.append({'file': file, 'title': title, 'category': category})

    # Sort by Category, then Title
    handouts.sort(key=lambda x: (x['category'], x['title']))

    # Generate the Table Rows
    rows_html = ""
    for h in handouts:
        rows_html += f"""
        <tr class="handout-row" data-category="{h['category']}">
            <td><span class="badge">{h['category']}</span></td>
            <td><a href="{h['file']}">{h['title']}</a></td>
        </tr>"""

    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical Handouts</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; max-width: 900px; margin: auto; background-color: #f4f7f6; }}
        h1 {{ color: #2c3e50; }}
        #searchInput {{ width: 100%; padding: 12px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; }}
        table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background-color: #3498db; color: white; }}
        .badge {{ background: #e1f5fe; color: #0288d1; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; text-transform: uppercase; }}
        a {{ text-decoration: none; color: #2c3e50; font-weight: 500; }}
        a:hover {{ color: #3498db; }}
    </style>
</head>
<body>
    <h1>Patient Handouts</h1>
    
    <input type="text" id="searchInput" onkeyup="filterTable()" placeholder="Search by name or category...">

    <table id="handoutTable">
        <thead>
            <tr>
                <th style="width: 150px;">Category</th>
                <th>Handout Title</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>

    <script>
    function filterTable() {{
        let input = document.getElementById("searchInput").value.toLowerCase();
        let rows = document.querySelectorAll(".handout-row");
        
        rows.forEach(row => {{
            let text = row.textContent.toLowerCase();
            row.style.display = text.includes(input) ? "" : "none";
        }});
    }}
    </script>
</body>
</html>"""

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(template)

if __name__ == "__main__":
    generate_index()
