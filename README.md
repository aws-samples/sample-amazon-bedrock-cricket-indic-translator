# Cricket-Centric Translation for Indic Languages

This project delivers a specialized natural language processing (NLP) system for translating cricket-related content across major Indian languages. Cricket has evolved its own rich vocabulary and expressions in the Indian subcontinent, creating unique translation challenges that this solution addresses.

Our domain-specific translation engine accurately captures the nuances, terminology, and cultural contexts of cricket commentary, news, and analysis across major Indic languages.

> **Note:** This solution can be deployed in three different modes:
> 
> - **MCP Server Mode**: Integrate with any Agent of your choice to explore these features - here we will use Amazon Q Command Line
> - **Agent Mode**: Leverages AWS Strands for an agentic approach with AgentCore for deployment both Local / Remote
> - **Standalone Mode**: Run as independent Python code

## Features

- Translates cricket content to 7 Indic languages: Tamil, Hindi, Telugu, Kannada, Bengali, Malayalam, and Marathi
- Preserves cricket terminology appropriately for each target language
- Maintains proper formatting of scores, player names, and statistics
- Follows cultural and linguistic conventions specific to cricket terminology
- Easily extensible architecture for additional Indic languages

## Quick Start

### Deploying as MCP Server for Amazon Q Command Line

#### Prerequisites

- [Install Amazon Q Command Line](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-installing.html)
- [Configure AWS CLI credentials](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html)
- [Install uv package manager](https://docs.astral.sh/uv/getting-started/installation/)
- [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to clone the repository

#### Deployment Steps

1. Clone the repository:

```bash
git clone https://github.com/aws-samples/sample-amazon-bedrock-cricket-indic-translator.git
```

2. Register the MCP server by updating the `.amazonq/mcp.json` file:

3. Locate or create the file at `~/.amazonq/mcp.json`

4. Add the server configuration to the JSON:

```json
{
  "mcpServers": {
    "crick-translate-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "<Project clone Directory>/sample-amazon-bedrock-cricket-indic-translator/src/mcp/crick_translate_server.py"
      ]
    }
  }
}
```

### Deploying Agent with Bedrock AgentCore Runtime (Remote)

#### Prerequisites

- Set up [required IAM permissions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-permissions.html) for Amazon Bedrock AgentCore (use managed policies)
- [Install Amazon Q Command Line](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-installing.html)
- [Configure AWS CLI credentials](https://docs.aws.amazon.com/cli/v1/userguide/cli-configure-files.html)

#### Deployment Steps

1. Navigate to the `src/agent` directory from the project root

2. Configure the entry point using AgentCore:

```bash
agentcore configure --entrypoint crick_translate_agent.py -er <IAM_ROLE_ARN that you created in prerequisite>
```

3. Launch the Agent on AWS:

```bash
agentcore launch
```

4. Once successfully launched, execute a test translation:

```bash
agentcore invoke '{"prompt": "Please translate the cricket text - Kohli hits a magnificent six over long-on, to Tamil" }'
```

### Deploying with Bedrock AgentCore Runtime (Local)

#### Prerequisites

#### Deployment Steps

1. Navigate to the `src/agent` directory from the project root

2. Run the Agent app:

```bash
python crick_translate_agent.py
```

3. Local invoke

```
curl -X POST http://localhost:8080/invocations \
-H "Content-Type: application/json" \
-d '{"prompt": "Please translate the cricket text - Kohli hits a magnificent six over long-on, to Tamil"}'
```

### Installation as MCP Server in streamable http mode.

#### Prerequisites
- Install python 3.10 or greater

#### Deployment Steps

1. Clone the repository to your preferred project directory:

```bash
git clone https://github.com/aws-samples/sample-amazon-bedrock-cricket-indic-translator.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Navigate to the `src/mcp` directory from the project root.
4. Start the streamable http MCP server

```
python crick_translate_server.py --mode mcp --mode-type streamable-http
```
5. Run the client

```
python crick_translate_client.py
```

6. Expected output as below

```
Translation Result:
{
  "translated_text": "विराट कोहली ने अंतिम ओवर में शतक बनाया, छह चौके और तीन छक्के लगाए।\n",
  "source_language": "English",
  "target_language": "Hindi"
}
```

### Installation for Python Standalone (Conda)

#### Prerequisites

- [Install Conda](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html)
- [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) to clone the repository

#### Deployment Steps

1. Clone the repository to your preferred project directory:

```bash
git clone https://github.com/aws-samples/sample-amazon-bedrock-cricket-indic-translator.git
```

2. Create a Conda environment:

```bash
conda create -n bedrock-crick-indic-translator python=3.12.7
```

3. Activate the Conda environment:

```bash
conda activate bedrock-crick-indic-translator
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Test the translation functionality:

```bash
python src/server.py --mode standalone --function translate --input-text "Kohli hits a magnificent six over long-on" --target-language Tamil
```


#### Cleanup Steps

1. Deactivate the Conda environment:

```bash
conda deactivate
```

2. Remove all Conda resources:

```bash
conda remove -n bedrock-crick-indic-translator --all
```

## Translation Guidelines

The translation system follows these specialized guidelines:

1. **Cricket Terminology Preservation:**
   - Retains standard cricket terms in English when commonly used: "over", "wicket", "boundary", "six", "four"
   - Translates action words and descriptions to the target language
   - Maintains score formats: "45/2", "3.3 overs"

2. **Regional Cricket Vocabulary:**
   - Utilizes established cricket terms in each target language
   - Tamil: "ஓவர்" (over), "விக்கெட்" (wicket), "பந்து" (ball)
   - Hindi: "ओवर" (over), "विकेट" (wicket), "गेंद" (ball)
   - Telugu: "ఓవర్" (over), "వికెట్" (wicket), "బంతి" (ball)
   - Kannada: "ಓವರ್" (over), "ವಿಕೆಟ್" (wicket), "ಚೆಂಡು" (ball)
   - Bengali: "ওভার" (over), "উইকেট" (wicket), "বল" (ball)
   - Malayalam: "ഓവർ" (over), "വിക്കറ്റ്" (wicket), "പന്ത്" (ball)
   - Marathi: "षटक" (over), "विकेट" (wicket), "चेंडू" (ball)

3. **Player Names and Teams:**
   - Preserves player names in original script/transliteration
   - Translates team descriptions while maintaining official team names

4. **Numbers and Statistics:**
   - Maintains numerical values in standard format
   - Translates descriptive text surrounding numbers

5. **Cricket Context Awareness:**
   - Understands batting/bowling context
   - Recognizes match situations (chasing, defending, powerplay)
   - Preserves the urgency and excitement of cricket commentary

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
