
import os
import sys
from pathlib import Path


def cli_rename():
    """Command Line Interface for renaming files"""
    print("=" * 60)
    print("FILE RENAME TOOL - CLI (Command Line Interface)")
    print("=" * 60)
    print()
    
    while True:
        print("\nOptions:")
        print("  1. Rename a file")
        print("  2. List files in current directory")
        print("  3. Change directory")
        print("  4. Exit")
        print()
        
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            old_name = input("Enter old filename: ").strip()
            
            # Check if file exists
            if not os.path.exists(old_name):
                print(f"❌ Error: File '{old_name}' not found!")
                continue
            
            new_name = input("Enter new filename: ").strip()
            
            # Check if new name already exists
            if os.path.exists(new_name):
                print(f"❌ Error: File '{new_name}' already exists!")
                continue
            
            try:
                os.rename(old_name, new_name)
                print(f"✅ SUCCESS: '{old_name}' renamed to '{new_name}'")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "2":
            try:
                files = os.listdir(".")
                if files:
                    print("\nFiles in current directory:")
                    for i, file in enumerate(files, 1):
                        print(f"  {i}. {file}")
                else:
                    print("Directory is empty")
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            path = input("Enter path: ").strip()
            try:
                os.chdir(path)
                print(f"✅ Changed to: {os.getcwd()}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    cli_rename()
