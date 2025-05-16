#!/usr/bin/env python3
"""
Simple script to seed the database with fake instrument data.
"""

import os
import sys
from seed_database import seed_database

if __name__ == "__main__":
    # Check if the user wants to reset the database
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        print("WARNING: This will reset all existing instrument data!")
        confirmation = input("Are you sure you want to continue? (y/n): ")
        if confirmation.lower() != 'y':
            print("Operation cancelled.")
            sys.exit(0)
    
    # Run the seed database function
    print("Seeding database with 350 fake instruments...")
    seed_database()
    print("Done! The database now contains fake instruments for testing.")
    print("\nYou can now run the main API with: python main.py") 