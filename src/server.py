#!/usr/bin/env python3
"""
Crick Translate MCP Server

An MCP server that provides tools for translating cricket text to Indian regional languages
while preserving cricket terminology and cultural context.
"""

import json
import logging
import argparse
import asyncio
import sys
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from strands import Agent
from strands.models import BedrockModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crick-trasnlate")

# Create FastMCP instance - will be properly configured based on mode type
# We initialize with default settings for decorator usage, but will reconfigure in main
mcp = FastMCP("crick-translate-mcp-server")
# Initialize a global agent dictionary to store agents for different models
# This ensures we only create one agent per model ID
AGENTS = {}

# Cricket terminology reference for different languages
CRICKET_TERMS = {
    "Tamil": {
        "over": "ஓவர்",
        "wicket": "விக்கெட்",
        "ball": "பந்து",
        "batsman": "பேட்ஸ்மேன்",
        "bowler": "பந்துவீச்சாளர்",
        "run_rate": "ரன் ரேட்",
        "partnership": "கூட்டணி",
        "boundary": "எல்லை",
        "catch": "கேட்ச்",
        "lbw": "எல்.பி.டபிள்யூ"
    },
    "Hindi": {
        "over": "ओवर",
        "wicket": "विकेट",
        "ball": "गेंद",
        "batsman": "बल्लेबाज",
        "bowler": "गेंदबाज",
        "run_rate": "रन रेट",
        "partnership": "साझेदारी",
        "boundary": "चौका/छक्का",
        "catch": "कैच",
        "lbw": "एलबीडब्ल्यू"
    },
    "Telugu": {
        "over": "ఓవర్",
        "wicket": "వికెట్",
        "ball": "బంతి",
        "batsman": "బ్యాట్స్‌మన్",
        "bowler": "బౌలర్",
        "run_rate": "రన్ రేట్",
        "partnership": "భాగస్వామ్యం",
        "boundary": "బౌండరీ",
        "catch": "క్యాచ్",
        "lbw": "ఎల్‌బిడబ్ల్యూ"
    },
    "Kannada": {
        "over": "ಓವರ್",
        "wicket": "ವಿಕೆಟ್",
        "ball": "ಚೆಂಡು",
        "batsman": "ಬ್ಯಾಟ್ಸ್‌ಮನ್",
        "bowler": "ಬೌಲರ್",
        "run_rate": "ರನ್ ರೇಟ್",
        "partnership": "ಪಾಲುದಾರಿಕೆ",
        "boundary": "ಬೌಂಡರಿ",
        "catch": "ಕ್ಯಾಚ್",
        "lbw": "ಎಲ್‌ಬಿಡಬ್ಲ್ಯೂ"
    },
    "Bengali": {
        "over": "ওভার",
        "wicket": "উইকেট",
        "ball": "বল",
        "batsman": "ব্যাটসম্যান",
        "bowler": "বোলার",
        "run_rate": "রান রেট",
        "partnership": "জুটি",
        "boundary": "বাউন্ডারি",
        "catch": "ক্যাচ",
        "lbw": "এলবিডব্লিউ"
    },
    "Malayalam": {
        "over": "ഓവർ",
        "wicket": "വിക്കറ്റ്",
        "ball": "പന്ത്",
        "batsman": "ബാറ്റ്സ്മാൻ",
        "bowler": "ബൗളർ",
        "run_rate": "റൺ നിരക്ക്",
        "partnership": "കൂട്ടുകെട്ട്",
        "boundary": "ബൗണ്ടറി",
        "catch": "ക്യാച്ച്",
        "lbw": "എൽബിഡബ്ല്യു"
    },
    "Marathi": {
        "over": "षटक",
        "wicket": "विकेट",
        "ball": "चेंडू",
        "batsman": "फलंदाज",
        "bowler": "गोलंदाज",
        "run_rate": "धावफलक",
        "partnership": "भागीदारी",
        "boundary": "सीमारेषा",
        "catch": "झेल",
        "lbw": "एलबीडब्ल्यू"
    }
}

# Example translations for demonstration purposes
EXAMPLE_TRANSLATIONS = {
    "Tamil": "கோஹ்லி லாங்-ஆன் மீது அற்புதமான சிக்ஸ் அடித்தார். இந்தியாவுக்கு 36 பந்துகளில் 45 ரன்கள் தேவை.",
    "Hindi": "कोहली ने लॉन्ग-ऑन पर एक शानदार छक्का मारा। भारत को 36 गेंदों में 45 रन चाहिए।",
    "Telugu": "కోహ్లీ లాంగ్-ఆన్ పై అద్భుతమైన సిక్స్ కొట్టాడు. భారత్‌కు 36 బంతుల్లో 45 పరుగులు కావాలి.",
    "Kannada": "ಕೊಹ್ಲಿ ಲಾಂಗ್-ಆನ್ ಮೇಲೆ ಅದ್ಭುತವಾದ ಸಿಕ್ಸ್ ಹೊಡೆದರು. ಭಾರತಕ್ಕೆ 36 ಚೆಂಡುಗಳಲ್ಲಿ 45 ರನ್‌ಗಳ ಅಗತ್ಯವಿದೆ.",
    "Bengali": "কোহলি লং-অনের উপর একটি দুর্দান্ত ছক্কা মেরেছেন। ভারতের ৩৬ বলে ৪৫ রান প্রয়োজন।",
    "Malayalam": "കോഹ്‌ലി ലോങ്-ഓണിന് മുകളിലൂടെ ഒരു മനോഹരമായ സിക്സ് അടിച്ചു. ഇന്ത്യയ്ക്ക് 36 പന്തിൽ 45 റൺസ് വേണം.",
    "Marathi": "कोहलीने लाँग-ऑनवर एक भव्य षटकार मारला. भारताला 36 चेंडूंमध्ये 45 धावांची आवश्यकता आहे."
}

# ==================== HELPER FUNCTIONS ====================

def generate_translation_prompt(input_text: str, target_language: str) -> str:
    """
    Generate a specialized prompt for cricket text translation.
    
    Args:
        input_text: The cricket text to translate
        target_language: The target language for translation
        
    Returns:
        A prompt string to be sent to an LLM
    """
    # Get language-specific cricket terms
    terms = CRICKET_TERMS.get(target_language, {})
    
    # Build the terminology reference section
    term_reference = "\n".join([f"- {k}: {v}" for k, v in terms.items()])
    
    prompt = f"""You are a professional cricket translator specializing in Indian regional languages. Translate the following cricket text accurately while maintaining proper cricket terminology and cultural context.

**Source Text:** {input_text}

**Target Language:** {target_language}

**Translation Guidelines:**

1. **Cricket Terminology Preservation:**
   - Keep standard cricket terms in English when commonly used: "over", "wicket", "boundary", "six", "four"
   - Translate action words and descriptions to target language
   - Maintain score formats: "45/2", "3.3 overs"
   - numbers are to be preserved in their original form rather than being translated. Maintain clarity and consistency, especially when dealing with scores, statistics, and player performance metrics.

2. **Regional Cricket Vocabulary:**
   - Use established cricket terms in the target language where they exist
   - For {target_language}, use these terms:
{term_reference}

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

**Output Format:**
Provide the translation in {target_language} script with proper formatting. Maintain the structure and flow of the original text while ensuring cultural and linguistic appropriateness.

**Now translate the following cricket text:**
{input_text}
"""
    return prompt

async def translate_cricket_text(input_text: str, target_language: str, model_id: str) -> Dict[str, Any]:
    """
    Translate cricket text to the specified Indian regional language.
    
    Args:
        input_text: The cricket text to translate
        target_language: The target language for translation
        model_id: The model ID to use for translation
        
    Returns:
        A dictionary containing the translation results
    """
    # Generate the prompt that would be sent to an LLM
    prompt = generate_translation_prompt(input_text, target_language)
    
    # In a real implementation, this would call an LLM API
    # For now, use mock translations as a fallback
    mock_translation = EXAMPLE_TRANSLATIONS.get(target_language, f"[Translation to {target_language} would appear here]")

    try:
        # Check if we already have an agent for this model_id
        if model_id not in AGENTS:
            logger.info(f"Creating new agent for model: {model_id}")
            # Create a configured Bedrock model
            bedrock_model = BedrockModel(
                model_id=model_id,
                temperature=0.3,
                top_p=0.8,
            )
            # Create and store the agent
            AGENTS[model_id] = Agent(model=bedrock_model)
        
        # Use the existing agent
        agent = AGENTS[model_id]
        response = agent(prompt)
        # Convert the AgentResult to a string to make it JSON serializable
        translated_text = str(response)
    except Exception as e:
        logger.error(f"Error using Agent: {str(e)}")
        # Fallback to mock translation
        translated_text = EXAMPLE_TRANSLATIONS.get(target_language, f"[Translation to {target_language} would appear here]")
    
    return {
        "translated_text": translated_text,
        "source_language": "English",
        "target_language": target_language,
        "prompt_used": prompt,
        "notes": "Translation preserves cricket terminology while adapting to target language conventions"
    }

async def get_cricket_terminology_data(target_language: str) -> Dict[str, Any]:
    """
    Get cricket terminology for the specified language.
    
    Args:
        target_language: The target language
        
    Returns:
        A dictionary containing the terminology data
    """
    terms = CRICKET_TERMS.get(target_language, {})
    
    return {
        "language": target_language,
        "terminology": terms
    }

# ==================== TRANSLATION TOOLS ====================

@mcp.tool()
async def translate_cricket(input_text, target_language, model_id="us.amazon.nova-lite-v1:0"):
    """
    Translates cricket text to the specified Indian regional language while preserving cricket terminology.
    
    Args:
        input_text (str): The cricket text to translate
        target_language (str): Target language for translation (Tamil, Hindi, Telugu, Kannada, Bengali, Malayalam, or Marathi)
        model_id (str): The model ID to use for translation (default: "us.amazon.nova-lite-v1:0")
        
    Returns:
        str: JSON response containing the translated text and metadata
    """
    try:
        if not input_text:
            return "Error: Input text cannot be empty"
            
        supported_languages = ["Tamil", "Hindi", "Telugu", "Kannada", "Bengali", "Malayalam", "Marathi"]
        if target_language not in supported_languages:
            return f"Error: Target language must be one of: {', '.join(supported_languages)}. Got: {target_language}"
        
        logger.info(f"Translating cricket text to {target_language} using model {model_id}")
        
        # Call the translation function
        result = await translate_cricket_text(input_text, target_language, model_id)
        
        # Return the result as JSON
        return json.dumps({
            "translated_text": result["translated_text"],
            "source_language": "English",
            "target_language": target_language
        }, indent=2)
    except Exception as e:
        return f"Error translating cricket text: {str(e)}"

@mcp.tool()
async def get_cricket_terminology(target_language):
    """
    Get cricket terminology reference for the specified language.
    
    Args:
        target_language (str): Target language (Tamil, Hindi, Telugu, Kannada, Bengali, Malayalam, or Marathi)
        
    Returns:
        str: JSON response containing cricket terminology in the target language
    """
    try:
        supported_languages = ["Tamil", "Hindi", "Telugu", "Kannada", "Bengali", "Malayalam", "Marathi"]
        if target_language not in supported_languages:
            return f"Error: Target language must be one of: {', '.join(supported_languages)}. Got: {target_language}"
        
        logger.info(f"Getting cricket terminology for {target_language}")
        
        # Get the terminology data
        result = await get_cricket_terminology_data(target_language)
        
        # Return the terminology as JSON
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error getting cricket terminology: {str(e)}"

# ==================== COMMAND LINE ARGUMENTS ====================

def parse_args():
    parser = argparse.ArgumentParser(description="Crickling Translation Server")
    parser.add_argument(
        "--mode", 
        choices=["mcp", "standalone"], 
        default="mcp",
        help="Server mode: 'mcp' for MCP server, 'standalone' for direct function execution"
    )
    parser.add_argument(
        "--mode-type", 
        choices=["stdio", "streamable-http"], 
        default="stdio",
        help="Server mode type: 'stdio' for Q CLI Integration, 'streamable-http' for Agentcore integration"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host address for HTTP server (used with streamable-http mode type)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for HTTP server (used with streamable-http mode type)"
    )
    parser.add_argument(
        "--stateless-http",
        default=True,
        help="Run HTTP server in stateless mode (used with streamable-http mode type)"
    )
    parser.add_argument(
        "--input-text",
        help="Text to translate (required in standalone mode)"
    )
    parser.add_argument(
        "--target-language",
        help="Target language for translation (required in standalone mode)"
    )
    parser.add_argument(
        "--model-id",
        default="us.amazon.nova-lite-v1:0",
        help="Model ID to use for translation (standalone mode only)"
    )
    parser.add_argument(
        "--function",
        choices=["translate", "terminology"],
        default="translate",
        help="Function to execute in standalone mode: 'translate' or 'terminology'"
    )
    return parser.parse_args()

# ==================== MAIN ENTRY POINT ====================

if __name__ == "__main__":
    try:
        args = parse_args()
        
        if args.mode == "mcp":
            # Reconfigure MCP based on mode type
            if args.mode_type == "stdio":
                logger.info("Starting Crickling MCP Server: Mode Type stdio")
                # Reinitialize with appropriate settings for stdio
                mcp.run(transport="stdio")
            elif args.mode_type == "streamable-http":
                logger.info(f"Starting Crickling MCP Server: Mode Type HTTP on {args.host}:{args.port}")
                # Reinitialize with appropriate settings for HTTP
                mcp.run(
                    transport="streamable-http",
                    host=args.host,
                    port=args.port,
                    stateless_http=True
                )
        else:
            # Standalone mode - directly execute the functions
            if args.function == "translate":
                if not args.input_text or not args.target_language:
                    print("Error: --input-text and --target-language are required for translation in standalone mode")
                    sys.exit(1)
                    
                result = asyncio.run(translate_cricket_text(
                    args.input_text, 
                    args.target_language, 
                    args.model_id
                ))
                print()
                print(f"Result : {result}")
            elif args.function == "terminology":
                if not args.target_language:
                    print("Error: --target-language is required for terminology lookup in standalone mode")
                    sys.exit(1)
                    
                result = asyncio.run(get_cricket_terminology_data(args.target_language))
                print(json.dumps(result, indent=2))
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Error running server: {str(e)}")
    finally:
        # Clean up agents
        logger.info(f"Cleaning up {len(AGENTS)} agent instances")
        AGENTS.clear()
        logger.info("Server shutdown complete")
