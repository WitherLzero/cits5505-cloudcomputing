#!/usr/bin/env python3
"""
Lab 9 - AWS Comprehend: Syntax Detection
Detects parts of speech (grammatical structure) in text.
"""

import boto3
from botocore.exceptions import ClientError

def detect_syntax(text, language_code='en'):
    """
    Detect syntax (parts of speech) in a text.

    Args:
        text (str): The text to analyze
        language_code (str): Language code (e.g., 'en', 'es', 'fr', 'it')

    Returns:
        list: List of tokens with their POS tags
    """
    client = boto3.client('comprehend', region_name='ap-southeast-2')

    try:
        response = client.detect_syntax(
            Text=text,
            LanguageCode=language_code
        )

        return response['SyntaxTokens']

    except ClientError as e:
        print(f"Error: {e}")
        return []

def main():
    """Test syntax detection with sample texts."""

    # Test texts from the lab worksheet (using first sentence of each for clarity)
    test_texts = {
        'English': {
            'text': "The French Revolution was a period of social and political upheaval in France.",
            'lang': 'en'
        },
        'Spanish': {
            'text': "El Quijote es la obra más conocida de Miguel de Cervantes Saavedra.",
            'lang': 'es'
        },
        'French': {
            'text': "Je suis le gardien du sommeil de ses nuits.",
            'lang': 'fr'
        },
        'Italian': {
            'text': "L'amor che move il sole e l'altre stelle.",
            'lang': 'it'
        }
    }

    # POS tag explanations
    pos_meanings = {
        'NOUN': 'Noun (person, place, thing)',
        'VERB': 'Verb (action or state)',
        'ADJ': 'Adjective (describes noun)',
        'ADV': 'Adverb (describes verb)',
        'PRON': 'Pronoun (replaces noun)',
        'DET': 'Determiner (the, a, this)',
        'ADP': 'Adposition (preposition)',
        'AUX': 'Auxiliary verb (is, was, have)',
        'CONJ': 'Conjunction (and, but, or)',
        'CCONJ': 'Coordinating conjunction',
        'SCONJ': 'Subordinating conjunction',
        'PROPN': 'Proper noun (names)',
        'NUM': 'Number',
        'PART': 'Particle',
        'INTJ': 'Interjection',
        'PUNCT': 'Punctuation',
        'O': 'Other'
    }

    print("="*70)
    print("AWS Comprehend - Syntax Detection Test")
    print("="*70)

    for name, data in test_texts.items():
        print(f"\n{'─'*70}")
        print(f"Text: {name}")
        print(f"Sentence: {data['text']}")
        print(f"{'─'*70}")

        syntax_tokens = detect_syntax(data['text'], data['lang'])

        if syntax_tokens:
            print(f"✓ Found {len(syntax_tokens)} tokens:\n")

            # Display in a table format
            print(f"  {'#':<4} {'Word':<20} {'POS':<8} {'Confidence':<12}")
            print(f"  {'-'*4} {'-'*20} {'-'*8} {'-'*12}")

            for i, token in enumerate(syntax_tokens, 1):
                word = token['Text']
                pos_tag = token['PartOfSpeech']['Tag']
                confidence = token['PartOfSpeech']['Score'] * 100

                print(f"  {i:<4} {word:<20} {pos_tag:<8} {confidence:>6.2f}%")

            # Summary of POS types
            pos_counts = {}
            for token in syntax_tokens:
                pos = token['PartOfSpeech']['Tag']
                pos_counts[pos] = pos_counts.get(pos, 0) + 1

            print(f"\n  Summary:")
            for pos, count in sorted(pos_counts.items(), key=lambda x: x[1], reverse=True):
                meaning = pos_meanings.get(pos, 'Unknown')
                print(f"    {pos}: {count} ({meaning})")

        else:
            print("✗ Syntax detection not supported for this language")

    print(f"\n{'='*70}\n")

if __name__ == "__main__":
    main()
