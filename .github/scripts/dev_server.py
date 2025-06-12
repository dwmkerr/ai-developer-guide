#!/usr/bin/env python3
"""
Development server with live reload for the AI Developer Guide site.
Watches for changes in guides/, README.md, and the generation script.
"""

import os
import sys
import time
import threading
import subprocess
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SiteRegenerator(FileSystemEventHandler):
    """Handles file change events and regenerates the site."""
    
    def __init__(self, readme_path, output_dir):
        self.readme_path = readme_path
        self.output_dir = output_dir
        self.last_rebuild = 0
        self.rebuild_delay = 1  # seconds
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Only rebuild for relevant file changes
        if self.should_rebuild(event.src_path):
            current_time = time.time()
            if current_time - self.last_rebuild > self.rebuild_delay:
                self.rebuild_site()
                self.last_rebuild = current_time
    
    def should_rebuild(self, file_path):
        """Check if the changed file should trigger a rebuild."""
        file_path = str(file_path)
        return (
            file_path.endswith('.md') or 
            file_path.endswith('.py') or
            'generate_json' in file_path
        )
    
    def rebuild_site(self):
        """Regenerate the site."""
        print(f"\n🔄 Rebuilding site... ({time.strftime('%H:%M:%S')})")
        try:
            result = subprocess.run([
                'python', '.github/scripts/generate_json.py', 
                self.readme_path, self.output_dir
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print("✅ Site rebuilt successfully!")
                # Extract the file count from output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'Successfully generated' in line:
                        print(f"   {line}")
                        break
            else:
                print(f"❌ Build failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Build error: {e}")

class LiveReloadHTTPRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler with live reload injection."""
    
    def end_headers(self):
        # Inject live reload script for HTML files
        if hasattr(self, 'path') and self.path.endswith('.html'):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        super().end_headers()
    
    def do_GET(self):
        # Handle live reload endpoint
        if self.path == '/live-reload':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'ok')
            return
        
        # Inject live reload script into HTML files
        super().do_GET()

def start_http_server(directory, port):
    """Start the HTTP server in a separate thread."""
    os.chdir(directory)
    server = HTTPServer(('localhost', port), LiveReloadHTTPRequestHandler)
    print(f"🌐 HTTP server running at http://localhost:{port}")
    server.serve_forever()

def main():
    if len(sys.argv) != 3:
        print("Usage: python dev_server.py README_PATH OUTPUT_DIR")
        sys.exit(1)
    
    readme_path = sys.argv[1]
    output_dir = sys.argv[2]
    port = 9090
    
    # Get project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.chdir(project_root)
    
    print("🚀 AI Developer Guide - Development Server")
    print("=" * 50)
    
    # Initial build
    print("📦 Initial site build...")
    regenerator = SiteRegenerator(readme_path, output_dir)
    regenerator.rebuild_site()
    
    # Start file watcher
    observer = Observer()
    
    # Watch the guides directory
    guides_dir = os.path.join(project_root, 'guides')
    if os.path.exists(guides_dir):
        observer.schedule(regenerator, guides_dir, recursive=True)
        print(f"👀 Watching: {guides_dir}")
    
    # Watch README.md
    observer.schedule(regenerator, project_root, recursive=False)
    print(f"👀 Watching: README.md")
    
    # Watch the scripts directory
    scripts_dir = os.path.join(project_root, '.github', 'scripts')
    if os.path.exists(scripts_dir):
        observer.schedule(regenerator, scripts_dir, recursive=False)
        print(f"👀 Watching: {scripts_dir}")
    
    observer.start()
    
    # Start HTTP server in background thread
    server_thread = threading.Thread(
        target=start_http_server,
        args=(output_dir, port),
        daemon=True
    )
    server_thread.start()
    
    print(f"\n🎉 Development server ready!")
    print(f"   📂 Site directory: {output_dir}")
    print(f"   🌐 Local URL: http://localhost:{port}")
    print(f"   🔄 Auto-rebuild: Enabled")
    print(f"\n💡 Edit files in guides/ or README.md to see changes")
    print("   Press Ctrl+C to stop\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Stopping development server...")
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main() 