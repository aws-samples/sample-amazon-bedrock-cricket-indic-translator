# -*- coding: utf-8 -*-
import json
import logging
import argparse
import asyncio
import sys
import io
from typing import Any, Dict, List, Optional
from strands import Agent, tool
from strands.models import BedrockModel
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Import common functionality
from common.cricket_translation import (
    translate_cricket_text,
    get_cricket_terminology_data,
    validate_language,
    logger
)

# ==================== TRANSLATION TOOLS ====================

@tool(description="translate the cricket text, say commentary, article, pre and post analysis report etc")
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
            
        is_valid, error_message = validate_language(target_language)
        if not is_valid:
            return error_message
        
        logger.info(f"Translating cricket text to {target_language} using model {model_id}")
        
        # Call the translation function
        result = await translate_cricket_text(input_text, target_language, model_id)
        
        # Return the result as JSON with ensure_ascii=False to preserve Unicode characters
        return json.dumps({
            "translated_text": result["translated_text"],
            "source_language": "English",
            "target_language": target_language
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error translating cricket text: {str(e)}"

@tool()
async def get_cricket_terminology(target_language):
    """
    Get cricket terminology reference for the specified language.
    
    Args:
        target_language (str): Target language (Tamil, Hindi, Telugu, Kannada, Bengali, Malayalam, or Marathi)
        
    Returns:
        str: JSON response containing cricket terminology in the target language
    """
    try:
        is_valid, error_message = validate_language(target_language)
        if not is_valid:
            return error_message
        
        logger.info(f"Getting cricket terminology for {target_language}")
        
        # Get the terminology data
        result = await get_cricket_terminology_data(target_language)
        
        # Return the terminology as JSON with ensure_ascii=False to preserve Unicode characters
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error getting cricket terminology: {str(e)}"
    

app = BedrockAgentCoreApp()

agent = Agent(
    system_prompt="You are a professional cricket translator specializing in Indian regional languages. Translate the following cricket text accurately while maintaining proper cricket terminology and cultural context. executing always using the tool",
    tools=[translate_cricket]
)


# Specify the entry point function invoking the agent
@app.entrypoint
def invoke(payload):
    """Handler for agent invocation"""
    user_message = payload.get(
        "prompt", "No prompt found in input, please guide customer to create a json payload with prompt key"
    )
    result = agent(user_message)
    
    # Ensure proper encoding when returning the result
    # Convert result to string and ensure it's properly encoded
    result_str = str(result)
    
    # Return as JSON with ensure_ascii=False to preserve Unicode characters
    return {"result": result_str}

if __name__ == "__main__":
    app.run()
