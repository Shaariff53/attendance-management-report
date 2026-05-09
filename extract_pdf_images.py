#!/usr/bin/env python3
"""
Extract high-quality images from PDF (specific pages only)
"""

import fitz  # PyMuPDF
from pathlib import Path

def extract_high_quality_images(pdf_path):
    """Extract images from specific pages with high quality"""
    
    doc = fitz.open(pdf_path)
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    # Map page numbers to diagram names (1-indexed for user, 0-indexed for code)
    page_mappings = {
        0: "use-case-diagram.png",      # Page 1
        8: "context-diagram.png",        # Page 9 (Level 0 DFD)
        9: "level1-dfd.png",             # Page 10
        10: "class-diagram.png",         # Page 11
        11: "sequence-diagram.png",      # Page 12
        12: "activity-diagram.png",      # Page 13
        13: "state-diagram-attendance.png",  # Page 14
        14: "architecture-diagram.png",  # Page 15
        16: "state-machine-session.png", # Page 17
        19: "gantt-chart.png"            # Page 20
    }
    
    for page_num, filename in page_mappings.items():
        print(f"\nProcessing Page {page_num + 1}...")
        page = doc[page_num]
        
        # Get images from this page
        image_list = page.get_images()
        print(f"  Found {len(image_list)} image(s) on page {page_num + 1}")
        
        if image_list:
            # Extract the first/main image from the page
            xref = image_list[0][0]
            pix = fitz.Pixmap(doc, xref)
            
            # Convert CMYK to RGB if needed
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                pass
            else:  # CMYK
                pix = fitz.Pixmap(fitz.csRGB, pix)
            
            # Save with high quality
            output_path = images_dir / filename
            pix.save(str(output_path))
            pix = None
            
            # Verify file was created
            if output_path.exists():
                file_size = output_path.stat().st_size
                print(f"  ✓ Saved: {filename} ({file_size / 1024:.2f} KB)")
            else:
                print(f"  ❌ Failed to save: {filename}")
        else:
            print(f"  ⚠ No images found on page {page_num + 1}")
    
    doc.close()
    print("\n✓ Extraction complete!")

if __name__ == "__main__":
    pdf_file = "report.pdf"
    extract_high_quality_images(pdf_file)
