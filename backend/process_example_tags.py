import easyocr
import cv2
import os
import re
import torch
import platform
from datetime import datetime

# Configure GPU acceleration based on available hardware
def get_device():
    device_info = {
        "device": "cpu",
        "name": "CPU",
        "platform": platform.system(),
        "processor": platform.processor()
    }
    
    # Check for Apple Silicon
    if torch.backends.mps.is_available() and torch.backends.mps.is_built():
        device_info["device"] = "mps"
        device_info["name"] = "Apple Silicon"
        try:
            # Try to get more specific Apple chip info
            import subprocess
            result = subprocess.run(['sysctl', '-n', 'machdep.cpu.brand_string'], 
                                    capture_output=True, text=True)
            if result.stdout:
                device_info["name"] = result.stdout.strip()
        except:
            pass
        print(f"Using MPS acceleration on {device_info['name']}")
        return device_info
    
    # Check for NVIDIA CUDA
    elif torch.cuda.is_available():
        device_info["device"] = "cuda"
        device_info["name"] = torch.cuda.get_device_name(0)
        device_info["cuda_version"] = torch.version.cuda
        device_info["gpu_count"] = torch.cuda.device_count()
        print(f"Using CUDA acceleration on {device_info['name']} (CUDA {device_info['cuda_version']})")
        return device_info
    
    # Fall back to CPU
    else:
        print(f"Using CPU only: {device_info['processor']}")
        return device_info

# Get hardware information and set device
DEVICE_INFO = get_device()
DEVICE = DEVICE_INFO["device"]

def clean_text(text_list):
    """Clean and join text, removing spaces and special characters."""
    return ''.join(text_list).replace(' ', '').upper()

def is_valid_tag_id(text):
    """Check if the text contains a tag ID pattern (00001-00350)."""
    # First, remove non-alphanumeric characters and convert to uppercase
    cleaned_text = re.sub(r'[^A-Z0-9]', '', text.upper())
    
    # Search for patterns like "00NNN" where NNN is 1-350
    matches = re.findall(r'00([0-9]{3})', cleaned_text)
    for match in matches:
        try:
            num = int(match)
            if 1 <= num <= 350:
                return f"00{num:03d}"
        except ValueError:
            pass
            
    return None

def is_valid_serial_number(text):
    """Identify potential serial numbers in text."""
    # First, clean the text
    cleaned_text = re.sub(r'[^A-Z0-9]', '', text.upper())
    
    # Common instrument serial number patterns
    serial_patterns = [
        # Model number patterns (often 1-3 letters followed by 4-10 digits)
        r'[A-Z]{1,3}\d{4,10}',  # Like CLD210913 (Clarinet)
        
        # Pure numeric serials (common in many instruments)
        r'\d{4,12}',  # 4-12 digit numbers
        
        # Mixed alphanumeric patterns (common in brass/woodwinds)
        r'[A-Z]\d{4,7}',  # Letter followed by digits (C67015)
        r'\d{2,6}[A-Z]\d{1,6}',  # Digits-letter-digits format
        
        # Short serial formats with letters (like PCN33)
        r'[A-Z]{2,4}\d{1,4}',
        
        # Year-based serials (common in guitars, etc.)
        r'\d{2}[A-Z]{1,4}\d{4,6}'  # Year code + model + sequence
    ]
    
    # Check for any of these patterns in the cleaned text
    for pattern in serial_patterns:
        matches = re.findall(pattern, cleaned_text)
        for match in matches:
            # Ensure minimum complexity (avoid false positives)
            if len(match) >= 4:
                return match
    
    # Check if there's a model name followed by something that looks like a serial
    model_serial = re.search(r'(GUITAR|BASS|TRUMPET|VIOLIN|CLARINET|FLUTE|SAXOPHONE|SAX|TROMBONE).{0,5}([A-Z0-9]{4,12})', cleaned_text)
    if model_serial:
        return model_serial.group(2)
    
    return None

def process_image(image_path):
    """Process an image to find either a tag ID or serial number."""
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} not found")
        return None
    
    try:
        # Initialize OCR reader with GPU support if available
        gpu = DEVICE != "cpu"
        reader = easyocr.Reader(['en'], gpu=gpu)
        
        # Extract text from image with detail=0 for plain text list
        text_list = reader.readtext(image_path, detail=0)
        
        print(f"Raw OCR results: {text_list}")
        
        # First, look for tag IDs directly
        for text in text_list:
            tag_id = is_valid_tag_id(text)
            if tag_id:
                return {
                    "type": "tag_id",
                    "value": tag_id
                }
        
        # Try with merged text - sometimes OCR splits digits across multiple detections
        merged_text = clean_text(text_list)
        print(f"Merged text: {merged_text}")
        tag_id = is_valid_tag_id(merged_text)
        if tag_id:
            return {
                "type": "tag_id",
                "value": tag_id
            }
        
        # If no tag ID found, look for serial numbers
        for text in text_list:
            serial = is_valid_serial_number(text)
            if serial:
                return {
                    "type": "serial_number",
                    "value": serial
                }
                
        # Try with merged text
        serial = is_valid_serial_number(merged_text)
        if serial:
            return {
                "type": "serial_number",
                "value": serial
            }
        
        return {
            "type": "none",
            "value": None
        }
    
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return {
            "type": "error",
            "value": str(e)
        }

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    example_dir = os.path.join(script_dir, 'Example Instrument Tags')
    
    # Process each image in the directory
    for filename in os.listdir(example_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(example_dir, filename)
            print(f"\n---\nProcessing {filename}...")
            
            result = process_image(image_path)
            if result and result["type"] != "none" and result["type"] != "error":
                print(f"Found {result['type']}: {result['value']}")
            else:
                print("No valid tag ID or serial number found")

if __name__ == "__main__":
    main() 