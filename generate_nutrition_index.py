import os
import json
from html.parser import HTMLParser

class MetaExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.title = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and 'name' in attrs and 'content' in attrs:
            self.meta[attrs['name']] = attrs['content']
        if tag == 'title':
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False

    def handle_data(self, data):
        if self._in_title and self.title is None:
            self.title = data.strip()

def parse_list(value):
    """Parse comma-separated string into list, stripping whitespace."""
    if not value:
        return []
    return [v.strip() for v in value.split(',') if v.strip()]

def main():
    repo_root = os.path.dirname(os.path.abspath(__file__))
    handouts = []

    for filename in sorted(os.listdir(repo_root)):
        if not filename.endswith('.html'):
            continue
        if filename.startswith('index'):
            continue

        filepath = os.path.join(repo_root, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()  # Read full file to catch all metadata
        except Exception:
            continue

        parser = MetaExtractor()
        parser.feed(content)

        # Only include handouts tagged for the nutrition module
        if parser.meta.get('module', '').strip().lower() != 'nutrition':
            continue

        entry = {
            "filename": filename,
            "title": parser.title or filename.replace('_', ' ').replace('.html', '').title(),
            "topics": parse_list(parser.meta.get('topics', '')),
            "diet_codes": parse_list(parser.meta.get('diet_codes', '')),
            "flags": parse_list(parser.meta.get('flags', '')),
            "section": parser.meta.get('section', 'general'),
            "description": parser.meta.get('description', '')
        }
        handouts.append(entry)

    output = {
        "version": "1.0",
        "generated": "auto",
        "handouts": handouts
    }

    output_path = os.path.join(repo_root, 'index_nutrition.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"Generated index_nutrition.json with {len(handouts)} handouts")

if __name__ == '__main__':
    main()
