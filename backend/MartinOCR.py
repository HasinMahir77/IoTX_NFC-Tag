import easyocr
import cv2
import os
import re
from datetime import datetime

def clean_text(text_list):
    """Clean and join text, removing spaces and special characters."""
    return ''.join(text_list).replace(' ', '').upper()

def is_martin_guitar(text):
    """Check if the text contains Martin brand name."""
    cleaned_text = clean_text(text)
    return 'MARTIN' in cleaned_text or 'MARTI' in cleaned_text

def decode_serial_number(serial):
    """Decode Martin guitar serial number based on its format."""
    # Remove any non-digit characters
    serial = re.sub(r'\D', '', serial)
    
    if not serial:
        return "Invalid serial number"
    
    try:
        num = int(serial)
        
        # Check for Little Martin (LX) format
        if num >= 41279 and num <= 361282:
            if num <= 41279:
                return {"format": "Little Martin", "year": "2005", "raw_serial": serial}
            elif 41280 <= num <= 54016:
                return {"format": "Little Martin", "year": "2006", "raw_serial": serial}
            elif 540167 <= num <= 69850:
                return {"format": "Little Martin", "year": "2007", "raw_serial": serial}
            elif 69851 <= num <= 85266:
                return {"format": "Little Martin", "year": "2008", "raw_serial": serial}
            elif 85267 <= num <= 98332:
                return {"format": "Little Martin", "year": "2009", "raw_serial": serial}
            elif 98333 <= num <= 115197:
                return {"format": "Little Martin", "year": "2010", "raw_serial": serial}
            elif 115198 <= num <= 129934:
                return {"format": "Little Martin", "year": "2011", "raw_serial": serial}
            elif 129935 <= num <= 145612:
                return {"format": "Little Martin", "year": "2012", "raw_serial": serial}
            elif 145613 <= num <= 172822:
                return {"format": "Little Martin", "year": "2013", "raw_serial": serial}
            elif 172823 <= num <= 205052:
                return {"format": "Little Martin", "year": "2014", "raw_serial": serial}
            elif 205053 <= num <= 236580:
                return {"format": "Little Martin", "year": "2015", "raw_serial": serial}
            elif 236581 <= num <= 263886:
                return {"format": "Little Martin", "year": "2016", "raw_serial": serial}
            elif 263887 <= num <= 284726:
                return {"format": "Little Martin", "year": "2017", "raw_serial": serial}
            elif 284727 <= num <= 319828:
                return {"format": "Little Martin", "year": "2018", "raw_serial": serial}
            elif 319829 <= num <= 344677:
                return {"format": "Little Martin", "year": "2019", "raw_serial": serial}
            elif 344678 <= num <= 361282:
                return {"format": "Little Martin", "year": "2020", "raw_serial": serial}
        
        # Check for Backpacker format
        if num >= 178146 and num <= 293493:
            if num <= 178146:
                return {"format": "Backpacker", "year": "1992-2006", "raw_serial": serial}
            elif 178147 <= num <= 188539:
                return {"format": "Backpacker", "year": "2007", "raw_serial": serial}
            elif 188540 <= num <= 195761:
                return {"format": "Backpacker", "year": "2008", "raw_serial": serial}
            elif 195762 <= num <= 203818:
                return {"format": "Backpacker", "year": "2009", "raw_serial": serial}
            elif 203819 <= num <= 211612:
                return {"format": "Backpacker", "year": "2010", "raw_serial": serial}
            elif 211613 <= num <= 220586:
                return {"format": "Backpacker", "year": "2011", "raw_serial": serial}
            elif 220587 <= num <= 229812:
                return {"format": "Backpacker", "year": "2012", "raw_serial": serial}
            elif 229813 <= num <= 239535:
                return {"format": "Backpacker", "year": "2013", "raw_serial": serial}
            elif 239536 <= num <= 249963:
                return {"format": "Backpacker", "year": "2014", "raw_serial": serial}
            elif 249964 <= num <= 260267:
                return {"format": "Backpacker", "year": "2015", "raw_serial": serial}
            elif 260268 <= num <= 267880:
                return {"format": "Backpacker", "year": "2016", "raw_serial": serial}
            elif 267881 <= num <= 274525:
                return {"format": "Backpacker", "year": "2017", "raw_serial": serial}
            elif 274526 <= num <= 280524:
                return {"format": "Backpacker", "year": "2018", "raw_serial": serial}
            elif 280525 <= num <= 288018:
                return {"format": "Backpacker", "year": "2019", "raw_serial": serial}
            elif 288019 <= num <= 293493:
                return {"format": "Backpacker", "year": "2020", "raw_serial": serial}
        
        # Check for Electric Models (E-18, EM-18, EB-18)
        if 1000 <= num <= 3645:
            if 1000 <= num <= 1099:
                return {"format": "Electric", "year": "1978", "raw_serial": serial}
            elif 1100 <= num <= 2831:
                return {"format": "Electric", "year": "1979", "raw_serial": serial}
            elif 2832 <= num <= 3645:
                return {"format": "Electric", "year": "1980", "raw_serial": serial}
        
        # Standard Martin Serial Numbers (1898-present)
        if num >= 8001:
            # 1898-2024 ranges
            if 8001 <= num <= 8349:
                return {"format": "Standard", "year": "1898", "raw_serial": serial}
            elif 8350 <= num <= 8716:
                return {"format": "Standard", "year": "1899", "raw_serial": serial}
            # ... (continuing with all ranges)
            elif 2829084 <= num:
                return {"format": "Standard", "year": "2024", "raw_serial": serial}
            
            # Add all other year ranges here
            year_ranges = {
                (8717, 9128): "1900",
                (9129, 9310): "1901",
                (9311, 9528): "1902",
                (9529, 9810): "1903",
                (9811, 9988): "1904",
                (9989, 10120): "1905",
                (10121, 10329): "1906",
                (10330, 10727): "1907",
                (10728, 10883): "1908",
                (10884, 11018): "1909",
                (11019, 11203): "1910",
                (11204, 11413): "1911",
                (11414, 11565): "1912",
                (11566, 11821): "1913",
                (11822, 12047): "1914",
                (12048, 12209): "1915",
                (12210, 12390): "1916",
                (12391, 12988): "1917",
                (12989, 13450): "1918",
                (13451, 14512): "1919",
                (14513, 15484): "1920",
                (15485, 16758): "1921",
                (16759, 17839): "1922",
                (17840, 19891): "1923",
                (19892, 22008): "1924",
                (22009, 24116): "1925",
                (24117, 28689): "1926",
                (28690, 34435): "1927",
                (34436, 37568): "1928",
                (37569, 40843): "1929",
                (40844, 45317): "1930",
                (45318, 49589): "1931",
                (49590, 52590): "1932",
                (52591, 55084): "1933",
                (55085, 58679): "1934",
                (58680, 61947): "1935",
                (61948, 65176): "1936",
                (65177, 68865): "1937",
                (68866, 71866): "1938",
                (71867, 74061): "1939",
                (74062, 76734): "1940",
                (76735, 80013): "1941",
                (80014, 83107): "1942",
                (83108, 86724): "1943",
                (86725, 90149): "1944",
                (90150, 93623): "1945",
                (93624, 98158): "1946",
                (98159, 103468): "1947",
                (103469, 108269): "1948",
                (108270, 112961): "1949",
                (112962, 117961): "1950",
                (117962, 122799): "1951",
                (122800, 128436): "1952",
                (128437, 134501): "1953",
                (134502, 141345): "1954",
                (141346, 147328): "1955",
                (147329, 153225): "1956",
                (153226, 159061): "1957",
                (159062, 165576): "1958",
                (165577, 171047): "1959",
                (171048, 175689): "1960",
                (175690, 181297): "1961",
                (181298, 187384): "1962",
                (187385, 193327): "1963",
                (193328, 199626): "1964",
                (199627, 207030): "1965",
                (207031, 217215): "1966",
                (217216, 230095): "1967",
                (230096, 241925): "1968",
                (241926, 256003): "1969",
                (256004, 271633): "1970",
                (271634, 294270): "1971",
                (294271, 313302): "1972",
                (313303, 333873): "1973",
                (333873, 353387): "1974",
                (353388, 371828): "1975",
                (371829, 388800): "1976",
                (388801, 399625): "1977",
                (399626, 407800): "1978",
                (407801, 419900): "1979",
                (419901, 430300): "1980",
                (430301, 436474): "1981",
                (436475, 439627): "1982",
                (439628, 446101): "1983",
                (446102, 453300): "1984",
                (453301, 460575): "1985",
                (460576, 468175): "1986",
                (468176, 476216): "1987",
                (476217, 483952): "1988",
                (483953, 493279): "1989",
                (493280, 503309): "1990",
                (503310, 512487): "1991",
                (512488, 522655): "1992",
                (522656, 535223): "1993",
                (535224, 551696): "1994",
                (551697, 570434): "1995",
                (570435, 592930): "1996",
                (592931, 624799): "1997",
                (624800, 668796): "1998",
                (668797, 724077): "1999",
                (724078, 780500): "2000",
                (780501, 845644): "2001",
                (845645, 916759): "2002",
                (916760, 978706): "2003",
                (978707, 1042558): "2004",
                (1042559, 1115862): "2005",
                (1115863, 1197799): "2006",
                (1197800, 1268091): "2007",
                (1268092, 1337042): "2008",
                (1337043, 1406715): "2009",
                (1406716, 1473461): "2010",
                (1473462, 1555767): "2011",
                (1555768, 1656742): "2012",
                (1656743, 1755536): "2013",
                (1755537, 1857399): "2014",
                (1857400, 1972129): "2015",
                (1972130, 2076795): "2016",
                (2076796, 2161732): "2017",
                (2161733, 2258889): "2018",
                (2258890, 2366880): "2019",
                (2366881, 293493): "2020",
                (293494, 2576415): "2021",
                (2576416, 2711440): "2022",
                (2711441, 2829083): "2023"
            }
            
            for (start, end), year in year_ranges.items():
                if start <= num <= end:
                    return {"format": "Standard", "year": year, "raw_serial": serial}
    
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
        if cleaned:
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
image_path = os.path.join(script_dir, 'Images/Martin/guitar1.jpg')

# Convert image to JPG if it's not already
if not image_path.lower().endswith('.jpg'):
    print(f"Converting {image_path} to JPG format...")
    image_path = convert_to_jpg(image_path)

# Read text from image
text = reader.readtext(image_path, detail=0)  # detail=0 for plain text

print("Extracted Text:")
print(text)
print("Analysis:")

# Check if it's a Martin guitar
if is_martin_guitar(text):
    print("This appears to be a Martin guitar")
    
    # Extract and decode serial number
    serial_info = extract_serial_number(text)
    if isinstance(serial_info, dict):
        print("\nSerial Number Information:")
        for key, value in serial_info.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    else:
        print(f"\nSerial Number: {serial_info}")
else:
    print("✗ This does not appear to be a Martin guitar") 