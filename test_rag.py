import sys
import json
from pathlib import Path

# Fix python path so imports resolve
sys.path.insert(0, str(Path("c:/Users/user/Desktop/AI Joi").resolve()))

from modules.joi_document_reader import ingest_long_document, query_document

# Create dummy file
dummy_path = Path("c:/Users/user/Desktop/AI Joi/dummy_book.txt")
content = "This is a random sentence about apples. " * 500
content += "\n\nCHAPTER 42: The Secret of the Golden Apple.\nIn this chapter we discover that the golden apple was actually hidden underneath the old oak tree by the river all along."
content += "\n\n" + "More random sentences about oranges. " * 500

dummy_path.write_text(content, encoding="utf-8")

# Ingest dummy file
print("Ingesting...")
ingest_res = ingest_long_document(file_path=str(dummy_path))
print(json.dumps(ingest_res, indent=2))

# Query dummy file
print("\nQuerying: 'where is the golden apple?'")
query_res = query_document(query="where is the golden apple?", filename="dummy_book.txt")
print(json.dumps(query_res, indent=2))

# Cleanup
dummy_path.unlink()
