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

def create_page_mapping(removed_pages, total_pages):
    """Create mapping from old page numbers to new page numbers."""
    mapping = {}
    removed_set = set(removed_pages)
    new_page = 1
    
    for old_page in range(1, total_pages + 1):
        if (old_page - 1) not in removed_set: # Convert to 0-indexed for comparison
            mapping[old_page] = new_page
            new_page += 1
        else:
            mapping[old_page] = None # Page was removed
    
    return mapping

def update_index_files(base_path, page_mapping):
    """Update .idx and .ind files with new page numbers."""
    idx_file = Path(base_path).with_suffix('.idx')
    ind_file = Path(base_path).with_suffix('.ind')
    
    # Update .idx file
    if idx_file.exists():
        print(f"Updating {idx_file}")
        try:
            with open(idx_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            updated_lines = []
            for line in lines:
                # Look for {hyperpage}{number} pattern
                match = re.search(r'\{hyperpage\}\{(\d+)\}', line)
                if match:
                    old_page = int(match.group(1))
                    new_page = page_mapping.get(old_page)
                    if new_page is not None:
                        # Replace the page number
                        updated_line = re.sub(r'\{hyperpage\}\{(\d+)\}', f'{{hyperpage}}{{{new_page}}}', line)
                        updated_lines.append(updated_line)
                    # If new_page is None, skip this line (page was deleted)
                else:
                    updated_lines.append(line)
            
            with open(idx_file, 'w', encoding='utf-8') as f:
                f.writelines(updated_lines)
        except Exception as e:
            print(f"Error updating {idx_file}: {e}")
    
    # Update .ind file
    if ind_file.exists():
        print(f"Updating {ind_file}")
        try:
            with open(ind_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all \hyperpage{number} patterns and replace them
            def replace_hyperpage(match):
                old_page = int(match.group(1))
                new_page = page_mapping.get(old_page)
                if new_page is not None:
                    return f'\\hyperpage{{{new_page}}}'
                else:
                    return ''  # Remove entries for deleted pages
            
            # Use a more specific pattern that matches exactly \hyperpage{digits}
            pattern = r'\\hyperpage\{(\d+)\}'
            updated_content = re.sub(pattern, replace_hyperpage, content)
            
            # Clean up formatting issues caused by removed entries
            # Remove sequences of commas and spaces
            updated_content = re.sub(r',(\s*,)+', ',', updated_content)
            # Remove trailing commas before newlines
            updated_content = re.sub(r',\s*\n', '\n', updated_content)
            # Remove leading commas after newlines with whitespace
            updated_content = re.sub(r'\n(\s*),', r'\n\1', updated_content)
            
            # Split into lines and clean up each line
            lines = updated_content.split('\n')
            cleaned_lines = []
            for line in lines:
                # Remove lines that are just whitespace and commas
                stripped = re.sub(r'[\s,]+', '', line)
                if stripped or line.strip().startswith('\\'):  # Keep LaTeX commands
                    cleaned_lines.append(line)
            
            with open(ind_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(cleaned_lines))
                
        except Exception as e:
            print(f"Error updating {ind_file}: {e}")
            # If there's an error, try a simpler approach
            print("Attempting simpler update approach...")
            try:
                with open(ind_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                updated_lines = []
                for line in lines:
                    # Process line by line for \hyperpage patterns
                    if '\\hyperpage{' in line:
                        # Find all page numbers in this line
                        matches = list(re.finditer(r'\\hyperpage\{(\d+)\}', line))
                        if matches:
                            new_line = line
                            # Process matches in reverse order to preserve positions
                            for match in reversed(matches):
                                old_page = int(match.group(1))
                                new_page = page_mapping.get(old_page)
                                if new_page is not None:
                                    new_line = new_line[:match.start()] + f'\\hyperpage{{{new_page}}}' + new_line[match.end():]
                                else:
                                    # Remove this hyperpage reference
                                    new_line = new_line[:match.start()] + new_line[match.end():]
                            updated_lines.append(new_line)
                        else:
                            updated_lines.append(line)
                    else:
                        updated_lines.append(line)
                
                with open(ind_file, 'w', encoding='utf-8') as f:
                    f.writelines(updated_lines)
                    
            except Exception as e2:
                print(f"Fallback approach also failed: {e2}")
                print("Manual index regeneration may be required.")

def process_pdf(input_path):
    """Remove blank pages from PDF and update index."""
    doc = fitz.open(input_path)
    total_pages = len(doc)
    pages_to_remove = find_pages_to_remove(doc)
    
    if not pages_to_remove:
        doc.close()
        print("No blank pages found to remove.")
        return
    
    print(f"Removing {len(pages_to_remove)} blank pages: {pages_to_remove}")
    
    # Create page mapping before removing pages
    page_mapping = create_page_mapping(pages_to_remove, total_pages)
    
    # Remove pages (in reverse order to maintain indices)
    for page_num in reversed(pages_to_remove):
        doc.delete_page(page_num)
    
    # Save PDF
    doc.save(input_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()
    
    # Update index files
    base_path = Path(input_path).stem
    update_index_files(base_path, page_mapping)
    
    print(f"PDF updated. {len(pages_to_remove)} pages removed.")
    print("Index files updated with new page numbers.")

def main():
    parser = argparse.ArgumentParser(description='Remove blank pages and update index')
    parser.add_argument("input_pdf", help="Input PDF file")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (no changes)")
    args = parser.parse_args()
    
    try:
        if args.dry_run:
            doc = fitz.open(args.input_pdf)
            pages_to_remove = find_pages_to_remove(doc)
            doc.close()
            
            if pages_to_remove:
                print(f"Would remove {len(pages_to_remove)} blank pages: {pages_to_remove}")
                page_mapping = create_page_mapping(pages_to_remove, len(fitz.open(args.input_pdf)))
                print("Page mapping preview:")
                for old, new in list(page_mapping.items())[:10]:
                    print(f"  Page {old} -> {'Page ' + str(new) if new else 'REMOVED'}")
                if len(page_mapping) > 10:
                    print(f"  ... and {len(page_mapping) - 10} more")
            else:
                print("No blank pages found.")
        else:
            process_pdf(args.input_pdf)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 
