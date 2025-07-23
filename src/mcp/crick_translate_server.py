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
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP

# Import common functionality
import sys
import os
# Add the parent directory to the path so we can import common
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.cricket_translation import (
    translate_cricket_text,
    get_cricket_terminology_data,
    validate_language,
    logger
)

# Create FastMCP instance - will be properly configured based on mode type
# We initialize with default settings for decorator usage, but will reconfigure in main
mcp = FastMCP("crick-translate-mcp-server")

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
            
        is_valid, error_message = validate_language(target_language)
        if not is_valid:
            return error_message
        
        logger.info(f"Translating cricket text to {target_language} using model {model_id}")
        
        # Call the translation function
        result = await translate_cricket_text(input_text, target_language, model_id)
        
        # Return the result as JSON
        return json.dumps({
            "translated_text": result["translated_text"],
            "source_language": "English",
            "target_language": target_language
        }, indent=2, ensure_ascii=False)
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
        is_valid, error_message = validate_language(target_language)
        if not is_valid:
            return error_message
        
        logger.info(f"Getting cricket terminology for {target_language}")
        
        # Get the terminology data
        result = await get_cricket_terminology_data(target_language)
        
        # Return the terminology as JSON
        return json.dumps(result, indent=2, ensure_ascii=False)
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
                print(json.dumps(result, indent=2, ensure_ascii=False))
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Error running server: {str(e)}")
    finally:
        # Clean up agents
        from common.cricket_translation import AGENTS
        logger.info(f"Cleaning up {len(AGENTS)} agent instances")
        AGENTS.clear()
        logger.info("Server shutdown complete")
