#!/usr/bin/env python3
import fitz
import argparse
import re
from pathlib import Path

def is_blank(page):
    """Check if page is blank by counting non-white pixels."""
    pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5), colorspace=fitz.csGRAY)
    samples = pix.samples
    if not samples:
        return True
    non_white = sum(1 for p in samples if p < 250)
    return (non_white / len(samples)) < 0.01

def has_article(page):
    """Check if page has "ARTICLE" in the top right corner."""
    rect = page.rect
    top_right = fitz.Rect(rect.width * 0.7, 0, rect.width, rect.height * 0.2)
    try:
        text = page.get_text("text", clip=top_right).upper()
        return "ARTICLE" in re.sub(r'\s+', '', text)
    except:
        return False

def find_article_bounds(doc):
    """Find first and last pages with "ARTICLE" in top right corner."""
    first = last = None
    for i, page in enumerate(doc):
        if has_article(page):
            if first is None:
                first = i
            last = i
    return first, last

def find_pages_to_remove(doc):
    """Find pages to remove."""
    to_remove = set()
    
    first, last = find_article_bounds(doc)
    if first is not None and last is not None:
        for i in range(first, last + 1):
            if is_blank(doc[i]):
                to_remove.add(i)
    
    blank_group = []
    for i, page in enumerate(doc):
        if is_blank(page):
            blank_group.append(i)
        else:
            if len(blank_group) >= 2:
                to_remove.update(blank_group[1:])
            blank_group = []
    
    if len(blank_group) >= 2:
        to_remove.update(blank_group[1:])
    
    return sorted(to_remove)

def process_pdf(input_path):
    """Remove blank pages from PDF."""
    doc = fitz.open(input_path)
    pages_to_remove = find_pages_to_remove(doc)
    
    if not pages_to_remove:
        doc.close()
        return
    
    for page_num in reversed(pages_to_remove):
        doc.delete_page(page_num)
    
    doc.save(input_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf")
    args = parser.parse_args()
    
    try:
        process_pdf(args.input_pdf)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 
