# Cricket Centric Translation for Indic Languages

The project aims to develop a specialized natural language processing (NLP) system focused on translating cricket-related content across various Indian languages. Cricket, being a cultural phenomenon in the Indian subcontinent, has developed its own rich vocabulary, idioms, and expressions that often present unique challenges in translation.

This project will create a domain-specific translation engine that accurately captures the nuances, terminology, and cultural contexts of cricket commentary, news and analysis across major Indic languages.

## Features

- Translates cricket centric text to Tamil, Hindi, Telugu, Kannada, Bengali, Malayalam, and Marathi
- Preserves cricket terminology appropriately for each language
- Maintains proper formatting of scores, player names, and statistics
- Follows cultural and linguistic conventions for cricket terminology
- Easily extensible for more indic languages.

## Quick Start

### Deploying as MCP server for Amazon Q Command Line

#### Prerequisite

- [Install](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-installing.html) Amazon Q Ccommand Line 
- [Install](https://docs.astral.sh/uv/getting-started/installation/) uv
- [Install](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) git to clone the repository

#### Deployment steps

1. Clone the repository using the below command

```
git clone https://github.com/aws-samples/sample-amazon-bedrock-cricket-indic-translator.git
```

2. To use this MCP server with Amazon Q CLI

You can also register the MCP server by directly updating the `.amazonq/mcp.json` file:

3. Locate or create the file at `~/.amazonq/mcp.json`
4. Add the server URL to the JSON array:

```json
{
  "mcpServers": {
    "crick-translate-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "<Project clone Directory>/sample-amazon-bedrock-cricket-indic-translator/server.py"
      ]
    }
  }
}

```

### Installation in Conda Environment

#### Prerequisite

- [Install](https://docs.conda.io/projects/conda/en/stable/user-guide/install/index.html) Conda 
- [Install](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) git to clone the repository

#### Deployment steps

1. Clone the repository using the below command under your preferred project directory.

```
git clone https://github.com/aws-samples/sample-amazon-bedrock-cricket-indic-translator.git
```

1. Create conda environemnt using below command

```
conda create -n bedrock-crick-indic-translator python=3.12.7
```
2. Conda environment activate using below command.

```
conda activate bedrock-crick-indic-translator
```

3. Deploy dependencies:

```
pip install -r requirements.txt
```

4. Execute the below command to test

```
python server.py --mode standalone --function translate --input-text "Kohli hits a magnificent six over long-on" --target-language Tamil
```

#### Cleanup steps

1. Deactivate conda environment

```
conda deactivate 
```

2. Remove all the conda resources

```
conda remove -n bedrock-crick-indic-translator --all
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

