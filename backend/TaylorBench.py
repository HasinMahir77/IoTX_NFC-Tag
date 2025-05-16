import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from PIL import Image

# Import the necessary functions from ocrTest
from TaylorOCR import (
    convert_to_jpg,
    is_taylor_guitar,
    extract_serial_number,
    easyocr
)

def is_image_file(file_path):
    """Check if the file is a valid image file."""
    # Common image extensions
    image_extensions = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
        '.webp', '.jfif', '.pjpeg', '.pjp', '.svg', '.ico', '.cur'
    }
    
    # Check extension
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in image_extensions:
        return False
    
    # Verify it's actually an image file using PIL
    try:
        with Image.open(file_path) as img:
            img.verify()  # Verify it's an image
            return True
    except Exception:
        return False

class TaylorBenchmark:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        self.stats = {
            'total_images': 0,
            'successful_identifications': 0,
            'failed_identifications': 0,
            'successful_serial_numbers': 0,
            'failed_serial_numbers': 0,
            'errors': [],
            'results': [],
            'timing': {
                'total_time': 0,
                'avg_time': 0,
                'min_time': float('inf'),
                'max_time': 0,
                'processing_times': []
            },
            'skipped_files': []  # Track non-image files
        }
        
    def process_image(self, image_path):
        """Process a single image and return the results."""
        start_time = time.time()
        
        result = {
            'filename': os.path.basename(image_path),
            'is_taylor': False,
            'serial_number_found': False,
            'serial_info': None,
            'error': None,
            'processing_time': 0,
            'extracted_text': None  # Add field for extracted text
        }
        
        try:
            # Convert to JPG if needed
            if not image_path.lower().endswith('.jpg'):
                image_path = convert_to_jpg(image_path)
            
            # Read text from image
            text = self.reader.readtext(image_path, detail=0)
            result['extracted_text'] = text  # Store the extracted text
            
            # Check if it's a Taylor guitar
            is_taylor = is_taylor_guitar(text)
            result['is_taylor'] = is_taylor
            
            if is_taylor:
                # Extract and decode serial number
                serial_info = extract_serial_number(text)
                result['serial_number_found'] = isinstance(serial_info, dict)
                result['serial_info'] = serial_info
                
                # Update stats
                if result['serial_number_found']:
                    self.stats['successful_serial_numbers'] += 1
                else:
                    self.stats['failed_serial_numbers'] += 1
                
                self.stats['successful_identifications'] += 1
            else:
                self.stats['failed_identifications'] += 1
                
        except Exception as e:
            result['error'] = str(e)
            self.stats['errors'].append({
                'filename': result['filename'],
                'error': str(e)
            })
            self.stats['failed_identifications'] += 1
        
        # Calculate processing time
        processing_time = time.time() - start_time
        result['processing_time'] = processing_time
        
        # Update timing statistics
        self.stats['timing']['processing_times'].append(processing_time)
        self.stats['timing']['min_time'] = min(self.stats['timing']['min_time'], processing_time)
        self.stats['timing']['max_time'] = max(self.stats['timing']['max_time'], processing_time)
        
        self.stats['total_images'] += 1
        self.stats['results'].append(result)
        return result

    def run_benchmark(self, directory):
        """Process all images in the specified directory using 2 threads."""
        print(f"Starting benchmark on directory: {directory}")
        print("=" * 50)
        
        # Get all files and filter for valid image files
        all_files = os.listdir(directory)
        image_files = []
        skipped_files = []
        
        for filename in all_files:
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                if is_image_file(file_path):
                    image_files.append(file_path)
                else:
                    skipped_files.append(filename)
        
        # Report skipped files
        if skipped_files:
            print("\nSkipped non-image files:")
            for filename in skipped_files:
                print(f"  - {filename}")
            print()
        
        if not image_files:
            print("No valid image files found in directory!")
            return
        
        print(f"Found {len(image_files)} valid image files to process")
        
        start_time = time.time()
        
        # Process images using ThreadPoolExecutor with 2 threads
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Submit all tasks
            future_to_image = {
                executor.submit(self.process_image, image_path): image_path 
                for image_path in image_files
            }
            
            # Process results as they complete
            for future in as_completed(future_to_image):
                image_path = future_to_image[future]
                try:
                    result = future.result()
                    # Print immediate feedback
                    print(f"\nProcessing: {result['filename']} (Time: {result['processing_time']:.2f}s)")
                    if result['extracted_text']:
                        print("Extracted Text:")
                        print("\n".join(result['extracted_text']))
                    if result['is_taylor']:
                        print("✓ Taylor guitar identified")
                        if result['serial_number_found']:
                            print(f"✓ Serial number found: {result['serial_info']['raw_serial']}")
                            print(f"  Date: {result['serial_info'].get('date', 'N/A')}")
                            print(f"  Series: {result['serial_info'].get('series', 'N/A')}")
                        else:
                            print("✗ No valid serial number found")
                    else:
                        print("✗ Not identified as a Taylor guitar")
                    
                    if result['error']:
                        print(f"! Error: {result['error']}")
                except Exception as e:
                    print(f"\nError processing {os.path.basename(image_path)}: {str(e)}")
        
        # Calculate total and average time
        total_time = time.time() - start_time
        self.stats['timing']['total_time'] = total_time
        if self.stats['total_images'] > 0:
            self.stats['timing']['avg_time'] = sum(self.stats['timing']['processing_times']) / self.stats['total_images']
        
        self.print_statistics()
        self.save_results(directory)
    
    def print_statistics(self):
        """Print benchmark statistics."""
        print("\n" + "=" * 50)
        print("BENCHMARK STATISTICS")
        print("=" * 50)
        
        total = self.stats['total_images']
        if total == 0:
            print("No images were processed!")
            return
        
        # Calculate percentages
        id_success_rate = (self.stats['successful_identifications'] / total) * 100
        serial_success_rate = (self.stats['successful_serial_numbers'] / total) * 100
        
        print(f"\nTotal Images Processed: {total}")
        print(f"\nTaylor Guitar Identification:")
        print(f"  Successful: {self.stats['successful_identifications']} ({id_success_rate:.1f}%)")
        print(f"  Failed: {self.stats['failed_identifications']} ({100-id_success_rate:.1f}%)")
        
        print(f"\nSerial Number Extraction:")
        print(f"  Successful: {self.stats['successful_serial_numbers']} ({serial_success_rate:.1f}%)")
        print(f"  Failed: {self.stats['failed_serial_numbers']} ({100-serial_success_rate:.1f}%)")
        
        print(f"\nProcessing Times:")
        print(f"  Total Time: {self.stats['timing']['total_time']:.2f}s")
        print(f"  Average Time: {self.stats['timing']['avg_time']:.2f}s")
        print(f"  Minimum Time: {self.stats['timing']['min_time']:.2f}s")
        print(f"  Maximum Time: {self.stats['timing']['max_time']:.2f}s")
        
        if self.stats['errors']:
            print(f"\nErrors encountered: {len(self.stats['errors'])}")
            for error in self.stats['errors']:
                print(f"  - {error['filename']}: {error['error']}")
    
    def save_results(self, directory):
        """Save benchmark results to a JSON file."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(directory, f"benchmark_results_{timestamp}.json")
        
        try:
            with open(output_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
            print(f"\nResults saved to: {output_file}")
        except Exception as e:
            print(f"\nError saving results: {str(e)}")

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    taylor_dir = os.path.join(script_dir, 'Images/Taylor')
    
    # Check if directory exists
    if not os.path.exists(taylor_dir):
        print(f"Error: Directory not found: {taylor_dir}")
        sys.exit(1)
    
    # Run the benchmark
    benchmark = TaylorBenchmark()
    benchmark.run_benchmark(taylor_dir)

if __name__ == "__main__":
    main() 