import os
from bs4 import BeautifulSoup

# Configuration
HANDOUTS_DIR = '.' 
INDEX_FILE = 'index.html'
EXCLUDE_FILES = [INDEX_FILE, 'generate_index.py', 'requirements.txt', 'README.md']

def get_metadata(filepath):
    """Extracts title and category from HTML."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            title = soup.title.string if soup.title else filepath
            cat_tag = soup.find('meta', attrs={'name': 'category'})
            category = cat_tag['content'].strip() if cat_tag else "Uncategorized"
            return title, category
    except Exception:
        return filepath, "Uncategorized"

def generate_index():
    files = [f for f in os.listdir(HANDOUTS_DIR) 
             if f.endswith('.html') and f not in EXCLUDE_FILES]
    
    handouts = []
    for file in files:
        title, category = get_metadata(os.path.join(HANDOUTS_DIR, file))
        handouts.append({'file': file, 'title': title, 'category': category})

    # SMART SORTING LOGIC:
    # 1. We take the category (e.g., "SKIN_ACNE") and split it by the underscore.
    # 2. We use the FIRST part ("SKIN") as the primary group.
    # 3. This ensures "SKIN" and "SKIN_ACNE" are always siblings.
    handouts.sort(key=lambda x: (x['category'].split('_')[0], x['category'], x['title']))

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
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 30px; max-width: 1000px; margin: auto; background-color: #f8fafc; color: #1e293b; }}
        h1 {{ color: #0f172a; border-bottom: 3px solid #3b82f6; padding-bottom: 12px; margin-bottom: 30px; font-weight: 800; }}
        #searchInput {{ width: 100%; padding: 15px; margin-bottom: 25px; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 18px; outline: none; transition: border-color 0.2s; }}
        #searchInput:focus {{ border-color: #3b82f6; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1); }}
        table {{ width: 100%; border-collapse: separate; border-spacing: 0; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }}
        th {{ background-color: #f1f5f9; color: #475569; font-weight: 600; text-transform: uppercase; font-size: 12px; letter-spacing: 0.05em; padding: 15px; text-align: left; }}
        td {{ padding: 16px; border-bottom: 1px solid #f1f5f9; }}
        .badge {{ background: #eff6ff; color: #1d4ed8; padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: 700; border: 1px solid #dbeafe; display: inline-block; }}
        tr:last-child td {{ border-bottom: none; }}
        tr:hover td {{ background-color: #f8fafc; }}
        a {{ text-decoration: none; color: #2563eb; font-weight: 600; font-size: 16px; }}
        a:hover {{ color: #1d4ed8; text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Patient Information Handouts</h1>
    <input type="text" id="searchInput" onkeyup="filterTable()" placeholder="Search handouts (e.g., 'diet', 'skin', 'sleep')..." autofocus>
    <table id="handoutTable">
        <thead>
            <tr><th style="width: 200px;">Category</th><th>Handout Title</th></tr>
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
