#!/usr/bin/env python3
"""
Lab 9 - AWS Comprehend: Keyphrase Detection
Detects key phrases (main topics and important concepts) in text.
"""

import boto3
from botocore.exceptions import ClientError

def detect_keyphrases(text, language_code='en'):
    """
    Detect key phrases in a text.

    Args:
        text (str): The text to analyze
        language_code (str): Language code (e.g., 'en', 'es', 'fr', 'it')

    Returns:
        list: List of detected keyphrases
    """
    client = boto3.client('comprehend', region_name='us-east-1')

    try:
        response = client.detect_key_phrases(
            Text=text,
            LanguageCode=language_code
        )

        return response['KeyPhrases']

    except ClientError as e:
        print(f"Error: {e}")
        return []

def main():
    """Test keyphrase detection with sample texts."""

    # Test texts from the lab worksheet
    test_texts = {
        'English': {
            'text': "The French Revolution was a period of social and political upheaval in France and its colonies beginning in 1789 and ending in 1799.",
            'lang': 'en'
        },
        'Spanish': {
            'text': "El Quijote es la obra más conocida de Miguel de Cervantes Saavedra. Publicada su primera parte con el título de El ingenioso hidalgo don Quijote de la Mancha a comienzos de 1605, es una de las obras más destacadas de la literatura española y la literatura universal, y una de las más traducidas. En 1615 aparecería la segunda parte del Quijote de Cervantes con el título de El ingenioso caballero don Quijote de la Mancha.",
            'lang': 'es'
        },
        'French': {
            'text': "Moi je n'étais rien Et voilà qu'aujourd'hui Je suis le gardien Du sommeil de ses nuits Je l'aime à mourir Vous pouvez détruire Tout ce qu'il vous plaira Elle n'a qu'à ouvrir L'espace de ses bras Pour tout reconstruire Pour tout reconstruire Je l'aime à mourir",
            'lang': 'fr'
        },
        'Italian': {
            'text': "L'amor che move il sole e l'altre stelle.",
            'lang': 'it'
        }
    }

    print("="*70)
    print("AWS Comprehend - Keyphrase Detection Test")
    print("="*70)

    for name, data in test_texts.items():
        print(f"\n{'─'*70}")
        print(f"Text: {name}")
        print(f"Preview: {data['text'][:80]}..." if len(data['text']) > 80 else f"Full text: {data['text']}")
        print(f"{'─'*70}")

        keyphrases = detect_keyphrases(data['text'], data['lang'])

        if keyphrases:
            print(f"✓ Found {len(keyphrases)} keyphrases:")

            # Sort by confidence (highest first)
            sorted_keyphrases = sorted(keyphrases, key=lambda x: x['Score'], reverse=True)

            for i, phrase in enumerate(sorted_keyphrases, 1):
                confidence = phrase['Score'] * 100
                print(f"  {i}. '{phrase['Text']}' (Confidence: {confidence:.2f}%)")
        else:
            print("✗ No keyphrases detected")

    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
