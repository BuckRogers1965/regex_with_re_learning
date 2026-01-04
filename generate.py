#!/usr/bin/env python3
"""
Regex Learning HTML Generator
Tests regex patterns and generates HTML documentation
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
import html
import json

@dataclass
class Example:
    name: str
    pattern: str
    test_input: str
    results: str
    description: str
    topic: str

class RegexLearningGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.examples_dir = self.base_dir / "examples"
        self.templates_dir = self.base_dir / "templates"
        self.html_output_dir = self.base_dir / "html_output"
    
    def test_pattern(self, pattern_file: Path) -> tuple[str, str, str]:
        """Test a regex pattern against its test cases"""
        # Read pattern
        with open(pattern_file, 'r') as f:
            pattern = f.read().strip()
        
        # Read test input
        input_file = pattern_file.parent / "test_input.txt"
        with open(input_file, 'r') as f:
            test_input = f.read()
        
        # Execute regex tests
        results_html = ""
        
        try:
            compiled_pattern = re.compile(pattern, re.MULTILINE)
            
            # Test each line or the whole input depending on pattern

            # Test each line
            test_lines = test_input.strip().split('\n')
            
            for i, line in enumerate(test_lines, 1):
                # Use finditer to locate ALL matches on the line
                matches = list(compiled_pattern.finditer(line))
                
                if matches:
                    # 1. Build the highlighted string
                    highlighted_line = ""
                    last_idx = 0
                    
                    for m in matches:
                        s, e = m.span()
                        # Add text since last match
                        highlighted_line += html.escape(line[last_idx:s])
                        # Add the highlighted match
                        highlighted_line += f'<span style="background-color: #a5d6a7; font-weight: bold; border-radius: 3px; padding: 0 2px;">{html.escape(line[s:e])}</span>'
                        last_idx = e
                    
                    # Add remaining text after last match
                    highlighted_line += html.escape(line[last_idx:])
                    
                    # 2. Start the result block
                    results_html += f'<div class="match-result">'
                    results_html += f'<strong>Line {i}:</strong> "{highlighted_line}"<br>'
                    
                    # 3. List details for each match found
                    for k, match in enumerate(matches, 1):
                        results_html += f'<div style="margin-top: 4px; margin-left: 10px; font-size: 0.9em; border-left: 2px solid #888; padding-left: 8px;">'
                        results_html += f'<strong>Match {k}:</strong> "{html.escape(match.group(0))}"'
                        
                        # Show captured groups if any
                        if match.groups():
                            results_html += '<br><strong>Groups:</strong> '
                            group_items = []
                            for j, group in enumerate(match.groups(), 1):
                                val = group if group is not None else "None"
                                group_items.append(f'{j}: "{html.escape(val)}"')
                            results_html += ', '.join(group_items)
                        
                        # Show named groups if any
                        if match.groupdict():
                            results_html += '<br><strong>Named:</strong> '
                            named_items = []
                            for name, value in match.groupdict().items():
                                val = value if value is not None else "None"
                                named_items.append(f'{name}: "{html.escape(val)}"')
                            results_html += ', '.join(named_items)
                            
                        results_html += '</div>'
                    
                    results_html += '</div>'
                else:
                    results_html += f'<div class="no-match">'
                    results_html += f'<strong>Line {i}:</strong> "{html.escape(line)}" - No match'
                    results_html += '</div>'
            
            # Also show findall results
            all_matches = compiled_pattern.findall(test_input)
            if all_matches:
                results_html += '<div class="group-info">'
                results_html += f'<strong>All matches found:</strong> {len(all_matches)}<br>'
                results_html += f'Matches: {html.escape(str(all_matches)[:200])}'
                if len(str(all_matches)) > 200:
                    results_html += '...'
                results_html += '</div>'
        
        except re.error as e:
            results_html = f'<div class="no-match"><strong>Regex Error:</strong> {html.escape(str(e))}</div>'
        except Exception as e:
            results_html = f'<div class="no-match"><strong>Error:</strong> {html.escape(str(e))}</div>'
        
        return pattern, test_input, results_html
    
    def discover_topics(self) -> List[Dict]:
        """Dynamically discover all topics and examples"""
        topics = []
        
        for topic_dir in sorted(self.examples_dir.iterdir()):
            if not topic_dir.is_dir():
                continue
            
            # Read topic metadata
            metadata_file = topic_dir / "topic.json"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)
            else:
                metadata = {
                    "title": topic_dir.name.replace("_", " ").title(),
                    "description": f"Examples for {topic_dir.name}"
                }
            
            # Find all examples in this topic
            examples = []
            for example_dir in sorted(topic_dir.iterdir()):
                if not example_dir.is_dir():
                    continue
                
                # Find the pattern file
                pattern_file = example_dir / "pattern.txt"
                if not pattern_file.exists():
                    continue
                
                desc_file = example_dir / "description.html"
                
                # Read description
                if desc_file.exists():
                    with open(desc_file) as f:
                        description = f.read()
                else:
                    description = "<p>No description provided.</p>"
                
                # Test the pattern
                print(f"  Testing: {topic_dir.name}/{example_dir.name}")
                pattern, test_input, results = self.test_pattern(pattern_file)
                
                examples.append(Example(
                    name=example_dir.name.replace("_", " ").title(),
                    pattern=pattern,
                    test_input=test_input,
                    results=results,
                    description=description,
                    topic=topic_dir.name
                ))
            
            if examples:
                topics.append({
                    "name": topic_dir.name,
                    "title": metadata["title"],
                    "description": metadata["description"],
                    "examples": examples
                })
        
        return topics
    
    def generate_html(self):
        """Generate all HTML documentation"""
        print("Discovering topics and examples...")
        topics = self.discover_topics()
        
        if not topics:
            print("⚠ No topics found to generate")
            return
        
        print(f"\nFound {len(topics)} topics")
        
        # Load templates
        with open(self.templates_dir / "header.html") as f:
            header_template = f.read()
        with open(self.templates_dir / "footer.html") as f:
            footer_template = f.read()
        with open(self.templates_dir / "example.html") as f:
            example_template = f.read()
        
        # Generate navigation links
        #nav_links = " | ".join([
            #f'<a href="{topic["name"]}.html">{topic["title"]}</a>'
            #for topic in topics
        #])
        # Generate navigation links (Start with Home)
        links = ['<a href="index.html"><strong>Home</strong></a>']
        for topic in topics:
            links.append(f'<a href="{topic["name"]}.html">{topic["title"]}</a>')
        
        nav_links = " | ".join(links)
        
        print("\nGenerating HTML pages...")
        
        # Generate topic pages
        for topic in topics:
            output_file = self.html_output_dir / f"{topic['name']}.html"
            
            # Build page content
            content = header_template.replace("{TITLE}", topic["title"]).replace("{NAV_LINKS}", nav_links)
            
            # Add topic description
            content += f'<div class="example"><h2>Overview</h2><div class="description"><p>{topic["description"]}</p></div></div>\n'
            
            # Add examples
            for example in topic["examples"]:
                example_html = example_template.replace("{EXAMPLE_NAME}", example.name)
                example_html = example_html.replace("{DESCRIPTION}", example.description)
                example_html = example_html.replace("{PATTERN}", html.escape(example.pattern))
                example_html = example_html.replace("{TEST_INPUT}", html.escape(example.test_input))
                example_html = example_html.replace("{RESULTS}", example.results)
                content += example_html
            
            content += footer_template
            
            with open(output_file, "w") as f:
                f.write(content)
            
            print(f"  ✓ {output_file.name}")
        
        # Generate index page
        self._generate_index(topics, nav_links, header_template, footer_template)
        
        print(f"\n{'='*60}")
        print(f"✓ All HTML generated in: {self.html_output_dir}")
        print(f"  Open: {self.html_output_dir / 'index.html'}")
        print(f"{'='*60}")
    
    def _generate_index(self, topics, nav_links, header_template, footer_template):
        """Generate the index page"""
        content = header_template.replace("{TITLE}", "Regular Expression Learning").replace("{NAV_LINKS}", nav_links)
        
        content += """
    <div class="example">
        <h2>Welcome to Regular Expression Learning</h2>
        <div class="description">
            <p>This documentation demonstrates how regular expressions work by showing the pattern, test input, and match results side-by-side. Each example uses Python's <code>re</code> module with clear explanations of what each pattern does.</p>
            
            <h3>How to Use This Guide</h3>
            <p>Each example includes:</p>
            <ul>
                <li><strong>Pattern</strong>: The regular expression pattern</li>
                <li><strong>Test Input</strong>: Sample text to match against</li>
                <li><strong>Match Results</strong>: What matched, captured groups, and whether each test case succeeded</li>
                <li><strong>Explanations</strong>: Detailed breakdown of how the pattern works</li>
            </ul>
            
            <h3>Python re Module</h3>
            <p>All examples use Python's standard <code>re</code> module. The patterns shown work with:</p>
            <ul>
                <li><code>re.search()</code>: Find first match</li>
                <li><code>re.findall()</code>: Find all matches</li>
                <li><code>re.match()</code>: Match at beginning of string</li>
                <li><code>re.sub()</code>: Replace matches</li>
            </ul>
            
            <h3>Learning Path</h3>
            <p>Start with <strong>Basic Patterns</strong> to understand character matching and simple quantifiers. Progress through <strong>Character Classes</strong> and <strong>Anchors</strong> to gain more control. Then explore <strong>Groups and Capturing</strong> to extract data. Finally, study <strong>Practical Examples</strong> for real-world use cases like email validation and data parsing.</p>
            
            <div class="reference">
                <strong>Additional Resources:</strong><br>
                • <a href="https://docs.python.org/3/library/re.html" target="_blank">Python re Module Documentation</a><br>
                • <a href="https://regex101.com/" target="_blank">Regex101 - Online Regex Tester</a><br>
                • <a href="https://www.regular-expressions.info/" target="_blank">Regular-Expressions.info - Comprehensive Tutorial</a><br>
                • <a href="https://regexr.com/" target="_blank">RegExr - Learn, Build, & Test RegEx</a>
            </div>
        </div>
        <h3>Available Topics</h3>
"""
        
        for topic in topics:
            content += f"""
        <div style="margin: 20px 0; padding: 15px; background: #ecf0f1; border-radius: 5px;">
            <h4><a href="{topic['name']}.html">{topic['title']}</a></h4>
            <p>{topic['description']}</p>
            <p><em>{len(topic['examples'])} examples</em></p>
        </div>
"""
        
        content += "    </div>\n"
        content += footer_template
        
        with open(self.html_output_dir / "index.html", "w") as f:
            f.write(content)
        
        print(f"  ✓ index.html")

def main():
    generator = RegexLearningGenerator()
    generator.generate_html()

if __name__ == "__main__":
    main()
