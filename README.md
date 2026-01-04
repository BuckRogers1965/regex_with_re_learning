# Regular Expression Learning System

This system helps you learn regular expressions by showing patterns, test inputs,
and match results side-by-side with detailed explanations.

[This is live on github pages](https://buckrogers1965.github.io/regex_with_re_learning)

## Quick Start

1. Generate HTML documentation:
   ```bash
   cd regex_learning
   python generate.py
   ```

2. Open `html_output/index.html` in your browser

## Adding New Examples

1. Navigate to the appropriate topic folder in `examples/`
2. Create a new directory for your example
3. Add three files:
   - `pattern.txt` - Your regex pattern
   - `test_input.txt` - Test cases (one per line or multi-line as needed)
   - `description.html` - HTML description with explanation
4. Run `python generate.py` to rebuild

## Adding New Topics

1. Create a new directory in `examples/` (e.g., `07_my_topic`)
2. Add a `topic.json` file:
   ```json
   {
     "title": "My Topic",
     "description": "Description of this topic"
   }
   ```
3. Add examples as subdirectories
4. Run `python generate.py` - it will automatically discover the new topic

## Directory Structure

```
regex_learning/
├── generate.py          # Run this to generate HTML
├── examples/            # Your regex patterns and tests
│   ├── 01_basic_patterns/
│   ├── 02_character_classes/
│   └── ...
├── templates/           # HTML templates (customize if desired)
└── html_output/         # Generated HTML (open in browser)
```

## Example Structure

Each example directory contains:
- `pattern.txt` - The regex pattern (single line)
- `test_input.txt` - Test strings (one per line or multi-line)
- `description.html` - Explanation with links to references

## Features

- **Side-by-side view**: Pattern, input, and results clearly displayed
- **Match highlighting**: See what matched, what didn't
- **Group extraction**: View captured groups and named groups
- **Comprehensive examples**: From basics to real-world patterns
- **Attributed sources**: All examples cite their references

## Resources

All examples include references to authoritative sources:
- [Python re Module Documentation](https://docs.python.org/3/library/re.html)
- [Regular-Expressions.info](https://www.regular-expressions.info/)
- [Regex101](https://regex101.com/) - Interactive testing
- [RegExr](https://regexr.com/) - Visual learning tool
