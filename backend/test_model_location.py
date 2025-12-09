"""
Test script to verify HF_HOME environment variable is correctly set
"""
import os

expected_path = "F:\\AI_Models\\huggingface"
actual_path = os.environ.get('HF_HOME', 'NOT SET')

print("="*50)
print("  HF_HOME VERIFICATION TEST")
print("="*50)
print()
print(f"Expected HF_HOME: {expected_path}")
print(f"Actual HF_HOME:   {actual_path}")
print()

if actual_path == expected_path:
    print("✅ Environment variable is correctly set!")
    print()
    print("Models will be stored in and loaded from:")
    print(f"  {expected_path}")
else:
    print("❌ Environment variable is NOT set correctly!")
    print()
    print("Troubleshooting:")
    print("1. Make sure you started the backend via iniciar_flashnews.bat")
    print("2. Check that .env file has HF_HOME=F:/AI_Models/huggingface")
    print("3. Restart the backend server after making changes")

print()
print("="*50)
