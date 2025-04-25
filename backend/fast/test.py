import google.generativeai as genai
import inspect

print(f"Installed google-generativeai version: {genai.__version__}")

try:
    from google.generativeai.types.content_types import Part
    print("Successfully imported Part from google.generativeai.types.content_types")
    exit()  # If successful, exit to avoid further checks
except ImportError:
    print("Failed to import Part from google.generativeai.types.content_types")

try:
    from google.generativeai.generative_models import Part
    print("Successfully imported Part from google.generativeai.generative_models")
    exit()  # If successful, exit
except ImportError:
    print("Failed to import Part from google.generativeai.generative_models")

try:
    from google.generativeai.types import Part
    print("Successfully imported Part from google.generativeai.types")
    exit()  # If successful, exit
except ImportError:
    print("Failed to import Part from google.generativeai.types")

print("Could not find the Part class in the expected locations. Let's inspect the google.generativeai module:")
print(inspect.getmembers(genai))
