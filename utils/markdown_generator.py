import os
import re
from datetime import datetime

class MarkdownGenerator:
    def __init__(self, output_dir="output"):
        """
        Initialize the Markdown Generator
        
        Parameters:
        - output_dir: Directory to save generated markdown files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_survey(self, data, filename=None):
        """
        Generate a markdown file from the survey data
        
        Parameters:
        - data: Dictionary containing all sections of the survey
        - filename: Optional filename for the output file, defaults to sanitized title
        
        Returns:
        - Path to the generated markdown file
        """
        title = data.get("title", "Literature Survey")
        if not filename:
            # Sanitize title for filename
            filename = re.sub(r'[^\w\s-]', '', title).strip().lower()
            filename = re.sub(r'[-\s]+', '-', filename)
            
        filepath = os.path.join(self.output_dir, f"{filename}.md")
        
        # Check if taxonomy has content
        taxonomy_data = data.get("taxonomy", {})
        has_taxonomy = bool(taxonomy_data) and any(content.strip() for content in taxonomy_data.values())
        
        with open(filepath, "w", encoding="utf-8") as f:
            # Title
            f.write(f"# {title}\n\n")
            
            # Table of Contents
            f.write("## Table of Contents\n\n")
            f.write("1. [Abstract](#abstract)\n")
            f.write("2. [Introduction](#introduction)\n")
            f.write("3. [Problem Definition and Basic Concepts](#problem-definition-and-basic-concepts)\n")
            
            # Only include taxonomy in TOC if it has content
            section_number = 4
            
            f.write(f"{section_number}. [Challenges and Open Problems](#challenges-and-open-problems)\n")
            section_number += 1
            f.write(f"{section_number}. [Future Research Directions](#future-research-directions)\n")
            section_number += 1
            f.write(f"{section_number}. [Conclusion](#conclusion)\n")
            section_number += 1
            f.write(f"{section_number}. [References](#references)\n\n")
            
            # Abstract
            f.write("## Abstract\n\n")
            f.write(data.get("abstract", "No abstract provided.") + "\n\n")
            
            # Introduction
            f.write("## Introduction\n\n")
            f.write(data.get("introduction", "No introduction provided.") + "\n\n")
            
            # Problem Definition
            f.write("## Problem Definition and Basic Concepts\n\n")
            f.write(data.get("problem_definition", "No problem definition provided.") + "\n\n")
            
            # Challenges
            f.write("## Challenges and Open Problems\n\n")
            f.write(data.get("challenges", "No challenges provided.") + "\n\n")
            
            # Future Directions
            f.write("## Future Research Directions\n\n")
            f.write(data.get("future_directions", "No future directions provided.") + "\n\n")
            
            # Conclusion
            f.write("## Conclusion\n\n")
            f.write(data.get("conclusion", "No conclusion provided.") + "\n\n")
            
            # References
            f.write("## References\n\n")
            references = data.get("references", [])
            
            # Filter out empty or invalid references
            valid_references = []
            for ref in references:
                if not ref or not ref.strip() or ref.strip() in [".", ",", "-", "None", "N/A"]:
                    continue
                
                # Check if reference has actual content beyond just authors and year
                # Looking for patterns like "Author et al. (2023) Title" or "Author et al. (2023). Title"
                if re.search(r'\(\d{4}\)[.,]?\s+\w+', ref) or len(ref.split(".")) > 1:
                    valid_references.append(ref)
            
            if not valid_references:
                f.write("No valid references found.\n")
            else:
                for i, ref in enumerate(valid_references, 1):
                    f.write(f"[{i}] {ref}\n\n")
        
        return filepath