#!/usr/bin/env python3
"""
Lab 9 - AWS Comprehend: Sentiment Analysis
Analyzes whether text is positive, negative, neutral, or mixed.
"""

import boto3
from botocore.exceptions import ClientError

def analyze_sentiment(text, language_code='en'):
    """
    Analyze the sentiment of a text.

    Args:
        text (str): The text to analyze
        language_code (str): Language code (e.g., 'en', 'es', 'fr')

    Returns:
        dict: Sentiment analysis results
    """
    client = boto3.client('comprehend', region_name='us-east-1')

    try:
        response = client.detect_sentiment(
            Text=text,
            LanguageCode=language_code
        )

        return response

    except ClientError as e:
        print(f"Error: {e}")
        return None

def main():
    """Test sentiment analysis with sample texts."""

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
    print("AWS Comprehend - Sentiment Analysis Test")
    print("="*70)

    for name, data in test_texts.items():
        print(f"\n{'─'*70}")
        print(f"Text: {name}")
        print(f"Preview: {data['text'][:80]}..." if len(data['text']) > 80 else f"Text: {data['text']}")
        print(f"{'─'*70}")

        result = analyze_sentiment(data['text'], data['lang'])

        if result:
            sentiment = result['Sentiment']
            scores = result['SentimentScore']

            print(f"✓ Overall Sentiment: {sentiment}")
            print(f"\n  Confidence Scores:")
            print(f"    Positive:  {scores['Positive']:.4f} ({scores['Positive']*100:.2f}%)")
            print(f"    Negative:  {scores['Negative']:.4f} ({scores['Negative']*100:.2f}%)")
            print(f"    Neutral:   {scores['Neutral']:.4f} ({scores['Neutral']*100:.2f}%)")
            print(f"    Mixed:     {scores['Mixed']:.4f} ({scores['Mixed']*100:.2f}%)")
        else:
            print("✗ Could not analyze sentiment")

    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
