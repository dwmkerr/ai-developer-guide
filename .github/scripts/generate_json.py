#!/usr/bin/env python3
"""
Script to convert markdown guide files to JSON for API consumption.
Generates a main guide.json file and individual guide endpoints.
Also generates an MCP manifest file from a template.
"""

import json
import os
import re
import sys
from datetime import datetime

def extract_references(content, base_url="api/guides"):
    """
    Extract references to specialized guides and add API URLs.
    
    Args:
        content: The markdown content to extract references from
        base_url: Base URL for API endpoints (no leading slash for local compatibility)
    
    Returns:
        List of reference objects with name, path, type and apiUrl
    """
    references = []
    
    # Pattern to match markdown links like [Python Guide](./docs/guides/python.md)
    link_pattern = r'\[(.*?)\]\((.*?)\)'
    guide_links = re.finditer(link_pattern, content)
    
    for match in guide_links:
        name = match.group(1)
        path = match.group(2)
        
        # Only include links to guide documents
        if 'guides' in path and path.endswith('.md'):
            guide_type = infer_guide_type(path)
            filename = os.path.basename(path).replace('.md', '.json')
            api_url = f"{base_url}/{guide_type}s/{filename}"
            
            references.append({
                "name": name,
                "path": path,
                "type": guide_type,
                "apiUrl": api_url
            })
    
    return references

def infer_guide_type(path):
    """Infer the type of guide from its path."""
    if 'python' in path.lower():
        return "language"
    elif 'make' in path.lower():
        return "pattern"
    elif 'postgresql' in path.lower() or 'sql' in path.lower():
        return "platform"
    elif 'shell' in path.lower():
        return "language"
    else:
        return "other"

def process_guide_markdown(file_path):
    """Read and process a guide markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Skip HTML comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        
        # Extract title from first heading
        title_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else os.path.basename(file_path).replace('.md', '')
        
        return {
            "title": title,
            "content": content
        }
    except Exception as e:
        print(f"Error processing guide {file_path}: {e}")
        return None

def create_guide_json(readme_path, output_dir):
    """
    Create guide JSON files from markdown files.
    
    Args:
        readme_path: Path to the main README.md file
        output_dir: Directory to output the generated files
    """
    # Get the project root directory
    project_dir = os.path.dirname(os.path.abspath(readme_path))
    guides_dir = os.path.join(project_dir, "docs", "guides")
    print(f"Looking for guides in: {guides_dir}")
    
    # Ensure output directories exist
    api_dir = os.path.join(output_dir, "api")
    api_guides_dir = os.path.join(api_dir, "guides")
    os.makedirs(api_dir, exist_ok=True)
    os.makedirs(api_guides_dir, exist_ok=True)
    
    # Create subdirectories for different guide types
    guide_types = ["languages", "patterns", "platforms", "other"]
    for guide_type in guide_types:
        os.makedirs(os.path.join(api_guides_dir, guide_type), exist_ok=True)
    
    # Process the main README.md
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading README: {e}")
        sys.exit(1)
    
    # Skip the HTML header and introduction sections
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Find where the actual guide begins
    guide_start_idx = content.find('## The Golden Rules')
    if guide_start_idx == -1:
        print("Error: Could not find the beginning of the guide.")
        sys.exit(1)
    
    # Get the main content from the guide start point onwards
    guide_content = content[guide_start_idx:]
    
    # Extract references to guides
    references = extract_references(guide_content)
    
    # Collect specific guide files
    guide_files = []
    generated_guides = []
    
    # Find all markdown files in the guides directory
    if os.path.exists(guides_dir):
        guide_files = [os.path.join(guides_dir, f) for f in os.listdir(guides_dir) 
                      if f.endswith('.md') and os.path.isfile(os.path.join(guides_dir, f))]
    
    # Process each guide file
    for guide_file in guide_files:
        filename = os.path.basename(guide_file)
        guide_data = process_guide_markdown(guide_file)
        
        if guide_data:
            # Determine the guide type and output path
            guide_type = infer_guide_type(guide_file)
            output_filename = filename.replace('.md', '.json')
            output_subdir = f"{guide_type}s"  # pluralize
            output_path = os.path.join(api_guides_dir, output_subdir, output_filename)
            
            # Create guide JSON structure
            specific_guide = {
                "metadata": {
                    "name": guide_data["title"],
                    "type": guide_type,
                    "version": "0.1.0",
                    "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
                    "source": f"https://github.com/dwmkerr/ai-developer-guide/docs/guides/{filename}"
                },
                "content": guide_data["content"]
            }
            
            # Write the guide JSON file
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(specific_guide, f, indent=2)
                relative_path = os.path.relpath(output_path, output_dir)
                print(f"✓ Created {relative_path}")
                generated_guides.append({
                    "name": guide_data["title"],
                    "type": guide_type,
                    "path": f"api/guides/{output_subdir}/{output_filename}"  # No leading slash for local compatibility
                })
    
    # Create the main guide.json structure
    guide_data = {
        "metadata": {
            "name": "AI Developer Guide",
            "version": "0.1.0",
            "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
            "source": "https://github.com/dwmkerr/ai-developer-guide"
        },
        "content": guide_content,
        "references": references
    }
    
    # Write the main guide.json
    guide_json_path = os.path.join(api_dir, "guide.json")
    with open(guide_json_path, 'w', encoding='utf-8') as f:
        json.dump(guide_data, f, indent=2)
        print(f"✓ Created api/guide.json")
    
    # Create index.html with links to all guides
    create_index_html(output_dir, generated_guides)
    
    print("Successfully generated JSON API files.")
    
    # Generate MCP manifest from template
    generate_mcp_manifest(project_dir, output_dir, generated_guides)
    
    # List all created files for verification
    print(f"\nGenerated files in {output_dir}:")
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            print(f"  - {os.path.relpath(os.path.join(root, file), output_dir)}")

def generate_mcp_manifest(project_dir, output_dir, generated_guides):
    """Generate MCP manifest.json from template."""
    template_path = os.path.join(project_dir, "mcp", "manifest.template.json")
    output_path = os.path.join(output_dir, "manifest.json")
    
    try:
        # Read the template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        # Remove any comments (lines starting with //)
        template_content = re.sub(r'\s+//.*$', '', template_content, flags=re.MULTILINE)
            
        # Parse the template JSON
        manifest = json.loads(template_content)
        
        # Start with the main guide endpoint (already in template)
        endpoints = [endpoint for endpoint in manifest.get("endpoints", []) 
                    if endpoint.get("name") == "main_guide"]
        
        # Group guides by type for better organization
        guides_by_type = {}
        for guide in generated_guides:
            guide_type = guide["type"]
            if guide_type not in guides_by_type:
                guides_by_type[guide_type] = []
            guides_by_type[guide_type].append(guide)
        
        # Add endpoints for each specialized guide
        for guide_type, guides in guides_by_type.items():
            type_label = guide_type.capitalize()
            for guide in guides:
                endpoint = {
                    "name": guide["path"].split("/")[-1].replace(".json", ""),
                    "description": f"{type_label} guide for {guide['name']}",
                    "path": f"/{guide['path']}"  # Add leading slash for MCP standard
                }
                endpoints.append(endpoint)
        
        # Update the manifest with all endpoints
        manifest["endpoints"] = endpoints
        
        # Write the final manifest
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
            print(f"✓ Created manifest.json")
    except Exception as e:
        print(f"Error generating MCP manifest: {e}")

def create_index_html(output_dir, generated_guides):
    """Create the index.html file with links to all guides."""
    
    # Group guides by type for the index page
    guides_by_type = {}
    for guide in generated_guides:
        guide_type = guide["type"]
        if guide_type not in guides_by_type:
            guides_by_type[guide_type] = []
        
        guides_by_type[guide_type].append(guide)
    
    # Generate the list items for the index page
    guide_links_html = ""
    for guide_type, guides in guides_by_type.items():
        guide_links_html += f"<h3>{guide_type.capitalize()} Guides</h3>\n<ul>\n"
        for guide in guides:
            guide_links_html += f'    <li><a href="{guide["path"]}">{guide["name"]}</a></li>\n'
        guide_links_html += "</ul>\n"
    
    # Create the HTML content with relative paths for local use
    index_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>AI Developer Guide API</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ color: #333; }}
        a {{ color: #0366d6; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        code {{ background-color: #f6f8fa; padding: 3px 5px; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>AI Developer Guide API</h1>
    <p>This is the JSON API for the AI Developer Guide.</p>
    
    <h2>Main Guide</h2>
    <ul>
        <li><a href="api/guide.json">guide.json</a> - Complete AI developer guide</li>
    </ul>
    
    <h2>Specialized Guides</h2>
    {guide_links_html}
    
    <h2>Usage with MCP</h2>
    <p>To use with Model Context Protocol:</p>
    <pre><code>GET api/guide.json                      // Get the complete developer guide
GET api/guides/languages/python.json    // Example of a specialized guide</code></pre>
</body>
</html>"""

    index_html_path = os.path.join(output_dir, "index.html")
    with open(index_html_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
        print(f"✓ Created index.html")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_json.py README_PATH OUTPUT_DIR")
        sys.exit(1)
    
    readme_path = sys.argv[1]
    output_dir = sys.argv[2]
    create_guide_json(readme_path, output_dir)
