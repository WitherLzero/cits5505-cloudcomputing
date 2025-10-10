#!/usr/bin/env python3
"""
Lab 9 - AWS Rekognition Tests
Tests label recognition, image moderation, facial analysis, and text extraction.
"""

import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from utils import config
import boto3
from botocore.exceptions import ClientError
import json

# Configuration
BUCKET_NAME = f'{config.STUDENT_NUMBER}-lab9-in-ap'
BUCKET_REGION = 'ap-southeast-2'
REKOGNITION_REGION = 'ap-southeast-2'

# Initialize Rekognition client
rekognition_client = boto3.client('rekognition', region_name=REKOGNITION_REGION)

def detect_labels(bucket, key, max_labels=10, min_confidence=80):
    """
    Detect labels (objects, scenes, concepts) in an image.

    Args:
        bucket: S3 bucket name
        key: S3 object key (image filename)
        max_labels: Maximum number of labels to return
        min_confidence: Minimum confidence threshold (0-100)
    """
    try:
        response = rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MaxLabels=max_labels,
            MinConfidence=min_confidence,
            Settings={'GeneralLabels': {'LabelInclusionFilters': []}}
        )

        return response['Labels']
    except ClientError as e:
        print(f"✗ Error: {e}")
        return []

def detect_moderation_labels(bucket, key, min_confidence=60):
    """
    Detect moderation labels (explicit or inappropriate content).

    Args:
        bucket: S3 bucket name
        key: S3 object key (image filename)
        min_confidence: Minimum confidence threshold (0-100)
    """
    try:
        response = rekognition_client.detect_moderation_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MinConfidence=min_confidence
        )

        return response['ModerationLabels']
    except ClientError as e:
        print(f"✗ Error: {e}")
        return []

def detect_faces(bucket, key):
    """
    Detect and analyze faces in an image.

    Args:
        bucket: S3 bucket name
        key: S3 object key (image filename)
    """
    try:
        response = rekognition_client.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            Attributes=['ALL']
        )

        return response['FaceDetails']
    except ClientError as e:
        print(f"✗ Error: {e}")
        return []

def detect_text(bucket, key):
    """
    Detect and extract text from an image (OCR).

    Args:
        bucket: S3 bucket name
        key: S3 object key (image filename)
    """
    try:
        response = rekognition_client.detect_text(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}}
        )

        return response['TextDetections']
    except ClientError as e:
        print(f"✗ Error: {e}")
        return []

def test_label_recognition():
    """Test label recognition on all images."""
    print("\n" + "="*70)
    print("TEST 1: LABEL RECOGNITION")
    print("="*70)

    test_images = ['urban.jpg', 'beach.jpg', 'faces.jpg', 'text.jpg']

    for image in test_images:
        print(f"\nImage: {image}")
        print("-"*70)

        labels = detect_labels(BUCKET_NAME, image)

        if labels:
            print(f"✓ Found {len(labels)} labels:")
            for label in labels:
                print(f"  • {label['Name']}: {label['Confidence']:.2f}% confidence")
                if label.get('Parents'):
                    parents = [p['Name'] for p in label['Parents']]
                    print(f"    Categories: {', '.join(parents)}")
        else:
            print("✗ No labels detected")

def test_image_moderation():
    """Test image moderation on all images."""
    print("\n" + "="*70)
    print("TEST 2: IMAGE MODERATION")
    print("="*70)

    test_images = ['urban.jpg', 'beach.jpg', 'faces.jpg', 'text.jpg']

    for image in test_images:
        print(f"\nImage: {image}")
        print("-"*70)

        labels = detect_moderation_labels(BUCKET_NAME, image)

        if labels:
            print(f"⚠️  Found {len(labels)} moderation labels:")
            for label in labels:
                print(f"  • {label['Name']}: {label['Confidence']:.2f}% confidence")
                if label.get('ParentName'):
                    print(f"    Parent category: {label['ParentName']}")
        else:
            print("✓ No inappropriate content detected")

def test_facial_analysis():
    """Test facial analysis on images with people."""
    print("\n" + "="*70)
    print("TEST 3: FACIAL ANALYSIS")
    print("="*70)

    # Test on images that likely contain faces
    face_images = ['faces.jpg', 'beach.jpg']

    for image in face_images:
        print(f"\nImage: {image}")
        print("-"*70)

        faces = detect_faces(BUCKET_NAME, image)

        if faces:
            print(f"✓ Found {len(faces)} face(s):")
            for i, face in enumerate(faces, 1):
                print(f"\n  Face {i}:")
                print(f"    Age range: {face['AgeRange']['Low']}-{face['AgeRange']['High']} years")
                print(f"    Gender: {face['Gender']['Value']} ({face['Gender']['Confidence']:.2f}% confidence)")

                # Emotions
                emotions = sorted(face['Emotions'], key=lambda x: x['Confidence'], reverse=True)
                print(f"    Top emotion: {emotions[0]['Type']} ({emotions[0]['Confidence']:.2f}% confidence)")

                # Other attributes
                print(f"    Smile: {face['Smile']['Value']} ({face['Smile']['Confidence']:.2f}% confidence)")
                print(f"    Eyes open: {face['EyesOpen']['Value']} ({face['EyesOpen']['Confidence']:.2f}% confidence)")
                print(f"    Sunglasses: {face['Sunglasses']['Value']} ({face['Sunglasses']['Confidence']:.2f}% confidence)")
                print(f"    Beard: {face['Beard']['Value']} ({face['Beard']['Confidence']:.2f}% confidence)")
                print(f"    Mustache: {face['Mustache']['Value']} ({face['Mustache']['Confidence']:.2f}% confidence)")
        else:
            print("✗ No faces detected")

def test_text_extraction():
    """Test text extraction (OCR) on all images."""
    print("\n" + "="*70)
    print("TEST 4: TEXT EXTRACTION (OCR)")
    print("="*70)

    test_images = ['urban.jpg', 'beach.jpg', 'faces.jpg', 'text.jpg']

    for image in test_images:
        print(f"\nImage: {image}")
        print("-"*70)

        text_detections = detect_text(BUCKET_NAME, image)

        if text_detections:
            # Separate WORD and LINE detections
            lines = [t for t in text_detections if t['Type'] == 'LINE']
            words = [t for t in text_detections if t['Type'] == 'WORD']

            print(f"✓ Found {len(lines)} line(s) and {len(words)} word(s)")

            if lines:
                print("\n  Lines detected:")
                for line in lines:
                    print(f"    • '{line['DetectedText']}' ({line['Confidence']:.2f}% confidence)")

            if words and len(words) <= 20:
                print("\n  Words detected:")
                for word in words:
                    print(f"    • '{word['DetectedText']}' ({word['Confidence']:.2f}% confidence)")
            elif words:
                print(f"\n  (Showing first 20 of {len(words)} words)")
                for word in words[:20]:
                    print(f"    • '{word['DetectedText']}' ({word['Confidence']:.2f}% confidence)")
        else:
            print("✗ No text detected")

def main():
    """Run all Rekognition tests."""

    print("="*70)
    print("Lab 9 - AWS Rekognition Tests")
    print(f"Bucket: {BUCKET_NAME} (Region: {BUCKET_REGION})")
    print(f"Rekognition Region: {REKOGNITION_REGION}")
    print("="*70)

    # Run all tests
    test_label_recognition()
    test_image_moderation()
    test_facial_analysis()
    test_text_extraction()

    print("\n" + "="*70)
    print("All tests completed!")
    print("="*70)

if __name__ == "__main__":
    main()
