# Crickling MCP Server

A Model Context Protocol (MCP) server for translating cricket text to Indian regional languages while preserving cricket terminology and cultural context.

## Features

- Translates cricket text to Tamil, Hindi, Telugu, Kannada, Bengali, Malayalam, and Marathi
- Preserves cricket terminology appropriately for each language
- Maintains proper formatting of scores, player names, and statistics
- Follows cultural and linguistic conventions for cricket terminology

## Prerequisites

- Python 3.10 or higher
- Package manager: pip, uv, or conda
- Docker (optional, for containerized deployment)
- Amazon Q CLI (optional, for integration with Amazon Q)

## Installation

### Option 1: Standard Python Installation with pip

1. Clone this repository:
```bash
git clone https://github.com/yourusername/crickling-mcp-server.git
cd crickling-mcp-server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run in Standalone:
You can also run the server in standalone mode to directly execute the translation functions:

```bash
# For translation
python src/server.py --mode standalone --function translate --input-text "Kohli hits a magnificent six over long-on" --target-language Tamil
```

### Option 2: Conda Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crickling-mcp-server.git
cd crickling-mcp-server
```

2. Create and activate a conda environment:
```bash
conda create -n crickling python=3.10
conda activate crickling
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run in Standalone:
You can also run the server in standalone mode to directly execute the translation functions:

```bash
# For translation
python src/server.py --mode standalone --function translate --input-text "Kohli hits a magnificent six over long-on" --target-language Tamil
```

### Registering the MCP Server with Q CLI

To use this MCP server with Amazon Q CLI: Directly Updating mcp.json

You can also register the MCP server by directly updating the `.amazonq/mcp.json` file:

1. Locate or create the file at `~/.amazonq/mcp.json`
2. Add the server URL to the JSON array:

```json
{
  "mcpServers": {
    "crick-translate-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "<Project Directory>/src/server.py"
      ]
    }
  }
}

```

### Verifying Registration

Check that your MCP server is registered:

```bash
q mcp list
```

```bash
q chat -v
```

### Using the Translation Tool

Once registered, you can use the cricket translation tool in your Amazon Q conversations:

```
Translate "Kohli hits a magnificent six over long-on. India needs 45 runs in 36 balls." to Tamil
```

### Example Translations

1. Basic translation:
```
Translate "Rohit Sharma scored a century in just 35 balls" to Hindi
```

2. With specific model:
```
Translate "The match is tied with scores level at 245" to Telugu using model id us.amazon.nova-lite-v1:0
```

3. Commentary translation:
```
Translate "What a magnificent catch by Jadeja at the boundary! That's the turning point of the match." to Bengali
```

## Translation Guidelines

The translation follows these guidelines:

1. **Cricket Terminology Preservation:**
   - Keep standard cricket terms in English when commonly used: "over", "wicket", "boundary", "six", "four"
   - Translate action words and descriptions to target language
   - Maintain score formats: "45/2", "3.3 overs"

2. **Regional Cricket Vocabulary:**
   - Use established cricket terms in the target language where they exist
   - For Tamil: Use "ஓவர்" (over), "விக்கெட்" (wicket), "பந்து" (ball)
   - For Hindi: Use "ओवर" (over), "विकेट" (wicket), "गेंद" (ball)
   - For Telugu: Use "ఓవర్" (over), "వికెట్" (wicket), "బంతి" (ball)
   - For Kannada: Use "ಓವರ್" (over), "ವಿಕೆಟ್" (wicket), "ಚೆಂಡು" (ball)
   - For Bengali: Use "ওভার" (over), "উইকেট" (wicket), "বল" (ball)
   - For Malayalam: Use "ഓവർ" (over), "വിക്കറ്റ്" (wicket), "പന്ത്" (ball)
   - For Marathi: Use "षटक" (over), "विकेट" (wicket), "चेंडू" (ball)

3. **Player Names and Teams:**
   - Keep player names in original script/transliteration
   - Translate team descriptions but keep official team names

4. **Numbers and Statistics:**
   - Keep numerical values in standard format
   - Translate descriptive text around numbers

5. **Cricket Context Awareness:**
   - Understand batting/bowling context
   - Recognize match situations (chasing, defending, powerplay)
   - Maintain urgency and excitement in commentary style

## License

MIT
