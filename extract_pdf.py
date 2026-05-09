#!/usr/bin/env python3
"""
Extract text and images from the Smart Attendance System PDF report
"""

import fitz  # PyMuPDF
import os
import json
from pathlib import Path

# Define image filenames based on expected diagram types
diagram_names = [
    "use-case-diagram.png",
    "context-diagram.png",
    "level1-dfd.png",
    "class-diagram.png",
    "sequence-diagram.png",
    "activity-diagram.png",
    "state-diagram-attendance.png",
    "architecture-diagram.png",
    "state-machine-session.png",
    "gantt-chart.png"
]

def extract_pdf_content(pdf_path):
    """Extract text and images from PDF"""
    
    doc = fitz.open(pdf_path)
    all_text = {}
    image_count = 0
    images_dir = Path("images")
    images_dir.mkdir(exist_ok=True)
    
    print(f"Processing PDF: {pdf_path}")
    print(f"Total pages: {len(doc)}\n")
    
    # Extract text and images from each page
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        all_text[f"page_{page_num + 1}"] = text
        
        # Extract images from page
        image_list = page.get_images()
        print(f"Page {page_num + 1}: Found {len(image_list)} image(s)")
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            
            # Determine filename
            if image_count < len(diagram_names):
                img_filename = diagram_names[image_count]
            else:
                img_filename = f"diagram-{image_count + 1}.png"
            
            img_path = images_dir / img_filename
            
            # Save image
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                pix.save(str(img_path))
            else:  # CMYK
                pix = fitz.Pixmap(fitz.csRGB, pix)
                pix.save(str(img_path))
            
            print(f"  ✓ Saved: {img_filename}")
            image_count += 1
    
    doc.close()
    
    # Save extracted text to JSON for reference
    with open("extracted_text.json", "w", encoding="utf-8") as f:
        json.dump(all_text, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Total images extracted: {image_count}")
    print(f"✓ Text content saved to: extracted_text.json")
    print(f"✓ Images saved to: images/")
    
    return all_text, image_count

if __name__ == "__main__":
    pdf_file = "report.pdf"
    if os.path.exists(pdf_file):
        text_content, total_images = extract_pdf_content(pdf_file)
        print("\nExtraction complete!")
    else:
        print(f"Error: {pdf_file} not found!")
