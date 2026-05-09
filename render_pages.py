#!/usr/bin/env python3
"""
Render pages as images (captures all content including drawn diagrams)
"""

import fitz  # PyMuPDF
from pathlib import Path

def render_pages_as_images(pdf_path):
    """Render specific pages as high-resolution images"""
    
    doc = fitz.open(pdf_path)
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    # Pages to render (with descriptive crop for main diagram area)
    pages_to_render = {
        14: ("architecture-diagram.png", "Page 15 - Architecture"),
        16: ("state-machine-session.png", "Page 17 - Session State Machine"),
        19: ("gantt-chart.png", "Page 20 - Gantt Chart")
    }
    
    for page_num, (filename, desc) in pages_to_render.items():
        print(f"\nRendering {desc}...")
        page = doc[page_num]
        
        # Render at 2x zoom for better quality (150 DPI)
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        output_path = images_dir / filename
        pix.save(str(output_path))
        pix = None
        
        if output_path.exists():
            file_size = output_path.stat().st_size
            print(f"  ✓ Saved: {filename} ({file_size / 1024:.2f} KB)")
    
    doc.close()
    print("\n✓ Rendering complete!")

if __name__ == "__main__":
    render_pages_as_images("report.pdf")
