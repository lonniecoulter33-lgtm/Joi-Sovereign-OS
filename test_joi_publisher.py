import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from modules.joi_publisher import publisher_init_project, publisher_edit_chapter, publisher_generate_asset, PROJECTS_DIR
import json

def test_publisher():
    print("1. Testing Init Project")
    res1 = publisher_init_project(project_name="The_AI_Publisher")
    print(json.dumps(res1, indent=2))
    
    print("\n2. Testing Edit Chapter")
    res2 = publisher_edit_chapter(project_name="The_AI_Publisher", chapter_num=1, content="# Chapter 1\n\nThe AI began to write...")
    print(json.dumps(res2, indent=2))

    print("\n3. Testing Gemini Image Gen")
    res3 = publisher_generate_asset(
        project_name="The_AI_Publisher", 
        prompt="A sleek, futuristic book cover featuring a glowing neon cybernetic eye, dark moody lighting, cinematic, 8k resolution, highly detailed",
        asset_type="cover",
        file_name="cover.png"
    )
    print(json.dumps(res3, indent=2))
    
    # We will test the pdf generation manually next if this passes

if __name__ == "__main__":
    test_publisher()
