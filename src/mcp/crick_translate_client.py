import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    print("calling main")
    mcp_url = "http://0.0.0.0:8080/mcp"
    headers = {}

    async with streamablehttp_client(mcp_url, headers, timeout=120, terminate_on_close=False) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            tool_result = await session.list_tools()
            print(tool_result)

            # Define the input parameters for translate_cricket tool
            cricket_text = "Virat Kohli scored a century in the final over, hitting six boundaries and three sixes."
            target_lang = "Hindi"
            
            # Call the translate_cricket tool
            print(f"Translating cricket text to {target_lang}...")
            print(f"Original text: {cricket_text}")
            
            translation_result = await session.call_tool(
                "translate_cricket",
                {
                    "input_text": cricket_text,
                    "target_language": target_lang
                    # Using default model_id
                }
            )
            
            # Pretty print the result
            print("\nTranslation Result:")
            print(translation_result.content[0].text)
            print(json.dumps(translation_result, indent=2, ensure_ascii=False))

asyncio.run(main())