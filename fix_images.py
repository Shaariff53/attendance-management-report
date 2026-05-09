#!/usr/bin/env python3
"""
Extract largest images from pages (for pages with multiple diagrams)
"""

import fitz  # PyMuPDF
from pathlib import Path

def extract_largest_image(pdf_path):
    """Extract the largest image from specific pages"""
    
    doc = fitz.open(pdf_path)
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    # Pages where we need to find the largest diagram
    problem_pages = {
        14: "architecture-diagram.png",   # Page 15 (0-indexed: 14)
        16: "state-machine-session.png",  # Page 17 (0-indexed: 16)
        19: "gantt-chart.png"             # Page 20 (0-indexed: 19)
    }
    
    for page_num, filename in problem_pages.items():
        print(f"\nProcessing Page {page_num + 1}...")
        page = doc[page_num]
        
        image_list = page.get_images()
        print(f"  Found {len(image_list)} image(s)")
        
        if not image_list:
            print(f"  ⚠ No images found")
            continue
        
        # Find the largest image
        largest_size = 0
        largest_xref = None
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            size = pix.n * pix.width * pix.height
            
            if size > largest_size:
                largest_size = size
                largest_xref = xref
            pix = None
        
        if largest_xref:
            pix = fitz.Pixmap(doc, largest_xref)
            
            # Convert CMYK to RGB if needed
            if pix.n - pix.alpha >= 4:  # CMYK
                pix = fitz.Pixmap(fitz.csRGB, pix)
            
            output_path = images_dir / filename
            pix.save(str(output_path))
            pix = None
            
            if output_path.exists():
                file_size = output_path.stat().st_size
                print(f"  ✓ Saved: {filename} ({file_size / 1024:.2f} KB)")
    
    doc.close()
    print("\n✓ Extraction complete!")

if __name__ == "__main__":
    extract_largest_image("report.pdf")
