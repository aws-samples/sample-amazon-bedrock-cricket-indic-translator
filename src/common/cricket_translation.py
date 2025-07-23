"""
Common functionality for cricket translation services.
This module contains shared code used by both the MCP server and the agent.
"""

import json
import logging
from typing import Any, Dict, List, Optional
from strands import Agent
from strands.models import BedrockModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cricket-translation")

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

def validate_language(target_language: str) -> (bool, str):
    """
    Validate that the target language is supported.
    
    Args:
        target_language: The target language to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    supported_languages = ["Tamil", "Hindi", "Telugu", "Kannada", "Bengali", "Malayalam", "Marathi"]
    if target_language not in supported_languages:
        return False, f"Error: Target language must be one of: {', '.join(supported_languages)}. Got: {target_language}"
    return True, ""
