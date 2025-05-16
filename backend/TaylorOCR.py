import easyocr
import cv2
import os
import re
from datetime import datetime

def clean_text(text_list):
    """Clean and join text, removing spaces and special characters."""
    return ''.join(text_list).replace(' ', '').upper()

def is_taylor_guitar(text):
    """Check if the text contains Taylor brand name."""
    cleaned_text = clean_text(text)
    return 'TAYLOR' in cleaned_text or 'TAYLO' in cleaned_text

def decode_serial_number(serial):
    """Decode Taylor guitar serial number based on its format."""
    # Remove any non-digit characters
    serial = re.sub(r'\D', '', serial)
    
    if not serial:
        return "Invalid serial number"
    
    # Handle 10-digit serial numbers (2009-present)
    if len(serial) == 10:
        try:
            factory = "El Cajon, California, USA" if serial[0] == '1' else "Tecate, Baja California, Mexico"
            year = f"20{serial[1]}{serial[6]}"
            month = serial[2:4]
            day = serial[4:6]
            sequence = serial[7:]
            
            date_str = f"{year}-{month}-{day}"
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                return {
                    "format": "10-digit (2009-present)",
                    "factory": factory,
                    "date": date.strftime("%B %d, %Y"),
                    "sequence": sequence,
                    "raw_serial": serial
                }
            except ValueError:
                return "Invalid date in serial number"
        except IndexError:
            return "Invalid 10-digit serial number format"
    
    # Handle 11-digit serial numbers (2000-2009)
    elif len(serial) == 11:
        try:
            year = serial[0:4]
            month = serial[4:6]
            day = serial[6:8]
            series_code = serial[8]
            sequence = serial[9:]
            
            series_map = {
                '0': '300 or 400 Series',
                '1': '500 through Presentation Series',
                '2': '200 Series',
                '3': 'Baby or Big Baby (through 2002)',
                '4': 'Big Baby (2004-2009)',
                '5': 'T5',
                '6': 'T3',
                '7': 'Nylon Series',
                '8': '100 Series',
                '9': 'SolidBody Series'
            }
            
            series = series_map.get(series_code, "Unknown Series")
            
            date_str = f"{year}-{month}-{day}"
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                return {
                    "format": "11-digit (2000-2009)",
                    "year": year,
                    "date": date.strftime("%B %d, %Y"),
                    "series": series,
                    "sequence": sequence,
                    "raw_serial": serial
                }
            except ValueError:
                return "Invalid date in serial number"
        except IndexError:
            return "Invalid 11-digit serial number format"
    
    # Handle 9-digit serial numbers (1993-1999)
    elif len(serial) == 9:
        try:
            year = f"19{serial[0:2]}"
            month = serial[2:4]
            day = serial[4:6]
            series_code = serial[6]
            sequence = serial[7:]
            
            series_map = {
                '0': '300 or 400 Series',
                '1': '500 through Presentation Series',
                '2': '200 Series',
                '3': 'Baby or Big Baby (through 2002)',
                '4': 'Big Baby (2004-2009)',
                '5': 'T5',
                '7': 'Nylon Series',
                '8': '100 Series',
                '9': 'SolidBody Series'
            }
            
            series = series_map.get(series_code, "Unknown Series")
            
            date_str = f"{year}-{month}-{day}"
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                return {
                    "format": "9-digit (1993-1999)",
                    "year": year,
                    "date": date.strftime("%B %d, %Y"),
                    "series": series,
                    "sequence": sequence,
                    "raw_serial": serial
                }
            except ValueError:
                return "Invalid date in serial number"
        except IndexError:
            return "Invalid 9-digit serial number format"
    
    # Handle 4-digit serial numbers (1991-1992)
    elif len(serial) == 5 and serial.startswith('4-'):
        try:
            sequence = int(serial[2:])  # Get digits after "4-"
            
            if 1 <= sequence <= 1121:
                return {
                    "format": "4-digit (1991)",
                    "year": "1991",
                    "sequence": str(sequence),
                    "raw_serial": serial,
                    "note": "410 model introduced in 1991"
                }
            elif 1122 <= sequence <= 3152:
                return {
                    "format": "4-digit (1992)",
                    "year": "1992",
                    "sequence": str(sequence),
                    "raw_serial": serial,
                    "note": "410 model continued in 1992"
                }
        except ValueError:
            pass
    
    # Handle 5-digit and 3-digit serial numbers (1974-1992)
    elif len(serial) in [3, 5]:
        try:
            num = int(serial)
            # Special case for earliest serials
            if num == 108:  # 00108
                return {"format": "5-digit", "year": "1975", "raw_serial": serial, "note": "One of the earliest Taylor guitars"}
            elif 10109 <= num <= 10146:
                return {"format": "5-digit", "year": "1975", "raw_serial": serial}
            elif 20147 <= num <= 20315:
                return {"format": "5-digit", "year": "1976", "raw_serial": serial}
            # Handle both 3-digit and 5-digit numbers for 1977
            elif (30316 <= num <= 450) or (num >= 316 and num <= 450 and len(serial) == 3):
                return {"format": "3/5-digit", "year": "1977", "raw_serial": serial, "note": "Mid-year switch to 3-digit format"}
            elif 451 <= num <= 900:
                return {"format": "5-digit", "year": "1978", "raw_serial": serial}
            elif 901 <= num <= 1300:
                return {"format": "5-digit", "year": "1979", "raw_serial": serial}
            elif 1301 <= num <= 1400:
                return {"format": "5-digit", "year": "1980", "raw_serial": serial}
            elif 1401 <= num <= 1670:
                return {"format": "5-digit", "year": "1981", "raw_serial": serial}
            elif 1671 <= num <= 1951:
                return {"format": "5-digit", "year": "1982", "raw_serial": serial}
            elif 1952 <= num <= 2445:
                return {"format": "5-digit", "year": "1983", "raw_serial": serial}
            elif 2446 <= num <= 3206:
                return {"format": "5-digit", "year": "1984", "raw_serial": serial}
            elif 3207 <= num <= 3888:
                return {"format": "5-digit", "year": "1985", "raw_serial": serial}
            elif 3889 <= num <= 4778:
                return {"format": "5-digit", "year": "1986", "raw_serial": serial}
            elif 4779 <= num <= 5981:
                return {"format": "5-digit", "year": "1987", "raw_serial": serial}
            elif 5982 <= num <= 7831:
                return {"format": "5-digit", "year": "1988", "raw_serial": serial}
            elif 7832 <= num <= 10070:
                return {"format": "5-digit", "year": "1989", "raw_serial": serial}
            elif 10071 <= num <= 12497:
                return {"format": "5-digit", "year": "1990", "raw_serial": serial}
            elif 12498 <= num <= 15249:
                return {"format": "5-digit", "year": "1991", "raw_serial": serial}
            elif 15250 <= num <= 17947:
                return {"format": "5-digit", "year": "1992", "raw_serial": serial}
        except ValueError:
            pass
    
    return "Unknown serial number format"

def extract_serial_number(text_list):
    """Extract and validate serial number from text."""
    # Look for patterns that might be serial numbers
    for text in text_list:
        # Remove spaces and special characters
        cleaned = re.sub(r'\D', '', text)
        
        # Check for different serial number formats
        if len(cleaned) in [9, 10, 11, 4, 5]:
            result = decode_serial_number(cleaned)
            if isinstance(result, dict):
                return result
    
    return "No valid serial number found"

def convert_to_jpg(image_path):
    """Convert any image format to JPG and return the path to the converted image."""
    # Get the directory and filename without extension
    directory = os.path.dirname(image_path)
    filename = os.path.splitext(os.path.basename(image_path))[0]
    
    # Create output path for JPG
    output_path = os.path.join(directory, f"{filename}_converted.jpg")
    
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Save as JPG
        cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        return output_path
    except Exception as e:
        print(f"Error converting image: {str(e)}")
        return image_path  # Return original path if conversion fails

# Initialize reader (English)
reader = easyocr.Reader(['en'])

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, 'Images/Taylor/guitar1.jpg')

# Convert image to JPG if it's not already
if not image_path.lower().endswith('.jpg'):
    print(f"Converting {image_path} to JPG format...")
    image_path = convert_to_jpg(image_path)

# Read text from image
text = reader.readtext(image_path, detail=0)  # detail=0 for plain text

print("Extracted Text:")
print(text)
print("Analysis:")

# Check if it's a Taylor guitar
if is_taylor_guitar(text):
    print("This appears to be a Taylor guitar")
    
    # Extract and decode serial number
    serial_info = extract_serial_number(text)
    if isinstance(serial_info, dict):
        print("\nSerial Number Information:")
        for key, value in serial_info.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    else:
        print(f"\nSerial Number: {serial_info}")
else:
    print("✗ This does not appear to be a Taylor guitar")