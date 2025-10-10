#!/usr/bin/env python3
"""
Lab 9 - AWS Comprehend: Language Detection
Detects the dominant language in a given text and displays confidence as percentage.
"""

import boto3
from botocore.exceptions import ClientError

# Language code to language name mapping
LANGUAGE_NAMES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'it': 'Italian',
    'de': 'German',
    'pt': 'Portuguese',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ar': 'Arabic',
    'ru': 'Russian',
    'hi': 'Hindi',
    'ko': 'Korean',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'pl': 'Polish',
    'tr': 'Turkish',
    'da': 'Danish',
    'fi': 'Finnish',
    'no': 'Norwegian',
    'cs': 'Czech',
    'ro': 'Romanian',
    'hu': 'Hungarian',
    'th': 'Thai',
    'he': 'Hebrew',
    'id': 'Indonesian',
    'ms': 'Malay',
    'vi': 'Vietnamese',
}

def detect_language(text):
    """
    Detect the dominant language in the given text.

    Args:
        text (str): The text to analyze

    Returns:
        tuple: (language_name, confidence_percentage)
    """
    client = boto3.client('comprehend', region_name='ap-southeast-2')

    try:
        response = client.detect_dominant_language(Text=text)

        if response['Languages']:
            # Get the top language
            top_language = response['Languages'][0]
            language_code = top_language['LanguageCode']
            confidence_score = top_language['Score']

            # Convert language code to name
            language_name = LANGUAGE_NAMES.get(language_code, language_code.upper())

            # Convert confidence to percentage
            confidence_percentage = int(confidence_score * 100)

            return language_name, confidence_percentage
        else:
            return None, 0

    except ClientError as e:
        print(f"Error: {e}")
        return None, 0

def main():
    """Test the language detection with sample texts."""

    # Test texts from the lab worksheet
    test_texts = {
        'English': "The French Revolution was a period of social and political upheaval in France and its colonies beginning in 1789 and ending in 1799.",

        'Spanish': "El Quijote es la obra más conocida de Miguel de Cervantes Saavedra. Publicada su primera parte con el título de El ingenioso hidalgo don Quijote de la Mancha a comienzos de 1605, es una de las obras más destacadas de la literatura española y la literatura universal, y una de las más traducidas. En 1615 aparecería la segunda parte del Quijote de Cervantes con el título de El ingenioso caballero don Quijote de la Mancha.",

        'French': "Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses nuits Je l'aime à mourir Vous pouvez détruire Tout ce qu'il vous plaira Elle n'a qu'à ouvrir L'espace de ses bras Pour tout reconstruire Pour tout reconstruire Je l'aime à mourir",

        'Italian': "L'amor che move il sole e l'altre stelle."
    }

    print("="*60)
    print("AWS Comprehend - Language Detection Test")
    print("="*60)

    for expected_lang, text in test_texts.items():
        print(f"\n{'─'*60}")
        print(f"Expected: {expected_lang}")
        print(f"Text: {text[:80]}..." if len(text) > 80 else f"Text: {text}")
        print(f"{'─'*60}")

        language_name, confidence = detect_language(text)

        if language_name:
            print(f"✓ {language_name} was detected with {confidence}% confidence")
        else:
            print("✗ Could not detect language")

    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
