#!/usr/bin/env python3
"""
Script to convert markdown guide files to JSON for API consumption.
Generates a main guide.json file and individual guide endpoints.
Creates a simple API index and shields.io version badge.
"""

import json
import os
import re
import sys
from datetime import datetime

def read_version(project_dir):
    """Read version from version.txt file."""
    version_file = os.path.join(project_dir, "version.txt")
    try:
        with open(version_file, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"Warning: Could not read version from {version_file}: {e}")
        return "0.1.0"  # fallback version

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
    
    # Pattern to match markdown links like [Python Guide](./guides/python.md)
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
    elif 'shell' in path.lower():
        return "language"
    elif 'make' in path.lower():
        return "pattern"
    elif 'cicd' in path.lower() or 'ci-cd' in path.lower():
        return "pattern"
    elif 'cli' in path.lower():
        return "pattern"
    elif 'documentation' in path.lower():
        return "pattern"
    elif 'open-source' in path.lower():
        return "pattern"
    elif 'postgresql' in path.lower() or 'sql' in path.lower():
        return "platform"
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
    guides_dir = os.path.join(project_dir, "guides")
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
                    "version": read_version(project_dir),
                    "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
                    "source": f"https://github.com/dwmkerr/ai-developer-guide/guides/{filename}"
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
            "version": read_version(project_dir),
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
    create_index_html(output_dir, generated_guides, project_dir)
    
    # Generate API index
    generate_api_index(project_dir, output_dir, generated_guides)
    
    # Create version badge for shields.io
    create_version_badge(output_dir, project_dir)
    
    print("Successfully generated JSON API files.")
    
    # List all created files for verification
    print(f"\nGenerated files in {output_dir}:")
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            print(f"  - {os.path.relpath(os.path.join(root, file), output_dir)}")

def create_index_html(output_dir, generated_guides, project_dir):
    """Create a simple index.html file for the AI Developer Guide API."""
    
    # Read version for display
    version = read_version(project_dir)
    
    # Group guides by type for the index page
    guides_by_type = {}
    for guide in generated_guides:
        guide_type = guide["type"]
        if guide_type not in guides_by_type:
            guides_by_type[guide_type] = []
        
        guides_by_type[guide_type].append(guide)
    
    # Generate table rows for the sidebar guides
    sidebar_table_rows = ""
    
    # Define the order of guide types
    guide_type_order = ["language", "pattern", "platform", "other"]
    
    # Add all specialized guides to the sidebar table in the specified order
    for guide_type in guide_type_order:
        if guide_type in guides_by_type:
            guides = guides_by_type[guide_type]
            # Sort guides by name for consistent ordering
            guides.sort(key=lambda g: g["name"])
            for guide in guides:
                sidebar_table_rows += f"""
    <tr>
        <td>{guide_type.capitalize()}</td>
        <td><a href="{guide["path"]}">{guide["name"]}</a></td>
        <td><a href="{guide["path"]}" class="text-decoration-none"><code>{guide["path"]}</code></a></td>
    </tr>
    """
    
    # Create the HTML content - updated per requirements
    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Developer Guide API</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="https://github.com/dwmkerr/ai-developer-guide">
                AI Developer Guide API
            </a>
            <div class="d-flex align-items-center">
                <span class="navbar-text me-3">
                    Version {version}
                </span>
                <a class="btn btn-outline-light btn-sm me-2" href="https://github.com/dwmkerr/ai-developer-guide#readme">
                    <i class="bi bi-file-text"></i> Documentation
                </a>
                <a class="btn btn-outline-light btn-sm" href="https://github.com/dwmkerr/ai-developer-guide">
                    <i class="bi bi-github"></i> GitHub
                </a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <h1>AI Developer Guide API</h1>
                <p class="lead">JSON API providing standards, patterns and principles for effective AI-assisted development. This API is used by the MCP server to connect LLMs to the guide.</p>
                
                <div class="alert alert-primary">
                    <h5><i class="bi bi-rocket-takeoff"></i> Quickstart</h5>
                    <p class="mb-2">Add this JSON structure to your AI assistant (Claude Desktop, Cursor, VS Code, etc.):</p>
                    <div class="bg-dark p-3 rounded">
                        <pre class="text-light mb-0"><code>{{
  "mcpServers": {{
    "ai-developer-guide": {{
      "command": "npx",
      "args": ["@dwmkerr/ai-developer-guide-mcp"]
    }}
  }}
}}</code></pre>
                    </div>
                    <p class="mt-2 mb-2">
                        <a href="https://github.com/dwmkerr/ai-developer-guide/tree/main/mcp" class="alert-link">
                            See the MCP documentation for detailed setup instructions (Claude, Cursor, VS Code, etc.) →
                        </a>
                    </p>
                    <p class="mb-2"><strong>Example prompt:</strong> <em>"Review my Python code and suggest improvements following best practices"</em></p>
                    
                    <div class="mt-3 p-2 bg-light rounded">
                        <small class="text-muted"><strong>Test with MCP Inspector:</strong></small><br>
                        <code class="small">npx @modelcontextprotocol/inspector npx @dwmkerr/ai-developer-guide-mcp</code>
                    </div>
                </div>

                <div class="row">
                    <div class="col-md-8">
                        <h2>About This API</h2>
                        <p>This JSON API serves the AI Developer Guide content in a structured format that can be consumed by Large Language Models (LLMs) through the Model Context Protocol (MCP) server.</p>
                        
                        <h3>Core Features</h3>
                        <ul>
                            <li><strong>Main Guide:</strong> Complete development methodology with Plan/Implement/Review approach</li>
                            <li><strong>Language-Specific Guides:</strong> Best practices for Python, Shell Scripts, and more</li>
                            <li><strong>Pattern Guides:</strong> Reusable patterns like Makefiles and project structure</li>
                            <li><strong>Platform Guides:</strong> Database and infrastructure-specific recommendations</li>
                        </ul>
                    </div>
                    
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-header">
                                <h6><i class="bi bi-info-circle"></i> API Info</h6>
                            </div>
                            <div class="card-body">
                                <p class="card-text small">
                                    <strong>Base URL:</strong> Current domain<br>
                                    <strong>Format:</strong> JSON<br>
                                    <strong>Version:</strong> {version}<br>
                                    <strong>Updated:</strong> {datetime.now().strftime("%Y-%m-%d")}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <h2>Available Guides</h2>
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead class="table-dark">
                            <tr>
                                <th>Type</th>
                                <th>Guide</th>
                                <th>Endpoint</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="table-info">
                                <td><strong>Main</strong></td>
                                <td><a href="api/guide.json"><strong>AI Developer Guide</strong></a></td>
                                <td><a href="api/guide.json" class="text-decoration-none"><code>api/guide.json</code></a></td>
                            </tr>
                            {sidebar_table_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    index_html_path = os.path.join(output_dir, "index.html")
    with open(index_html_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
        print(f"✓ Created index.html")

def create_version_badge(output_dir, project_dir):
    """Create a shields.io compatible version badge JSON file."""
    version = read_version(project_dir)
    
    badge_data = {
        "schemaVersion": 1,
        "label": "version",
        "message": version,
        "color": "blue"
    }
    
    badge_path = os.path.join(output_dir, "version-badge.json")
    with open(badge_path, 'w', encoding='utf-8') as f:
        json.dump(badge_data, f, indent=2)
        print(f"✓ Created version-badge.json")

def generate_api_index(project_dir, output_dir, generated_guides):
    """Generate a simple API index file."""
    output_path = os.path.join(output_dir, "api.json")
    
    try:
        # Read version
        version = read_version(project_dir)
        
        # Create a simple API index
        api_index = {
            "name": "AI Developer Guide API",
            "description": "JSON API providing standards, patterns and principles for effective AI-assisted development",
            "version": version,
            "source": "https://github.com/dwmkerr/ai-developer-guide",
            "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
            "endpoints": {
                "main_guide": {
                    "path": "/api/guide.json",
                    "description": "Complete AI Developer Guide with core rules and Plan/Implement/Review approach"
                }
            }
        }
        
        # Group guides by type
        guides_by_type = {}
        for guide in generated_guides:
            guide_type = guide["type"]
            if guide_type not in guides_by_type:
                guides_by_type[guide_type] = {}
            
            guide_name = guide["path"].split("/")[-1].replace(".json", "")
            guides_by_type[guide_type][guide_name] = {
                "path": f"/{guide['path']}",
                "description": f"{guide['name']} guide"
            }
        
        # Add specialized guides to endpoints
        for guide_type, guides in guides_by_type.items():
            api_index["endpoints"][f"{guide_type}_guides"] = guides
        
        # Write the API index
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(api_index, f, indent=2)
            print("✓ Created api.json")
            
    except Exception as e:
        print(f"Error generating API index: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_json.py README_PATH OUTPUT_DIR")
        sys.exit(1)
    
    readme_path = sys.argv[1]
    output_dir = sys.argv[2]
    create_guide_json(readme_path, output_dir)
