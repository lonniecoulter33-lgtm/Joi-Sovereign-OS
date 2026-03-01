import json
import re

try:
    with open('learning_data.json', 'r', encoding='utf-8') as f:
        content = f.read()

    patterns = [
        r'\"I don\'t have the capability to generate images directly[^\"]+\"',
        r'\"I can\'t generate images directly[^\"]+\"'
    ]
    
    total = 0
    for p in patterns:
        matches = len(re.findall(p, content))
        if matches > 0:
            content = re.sub(p, '\"[Attempted Image Generation] Please wait while I pull up my image generation tools...\"', content)
            total += matches
            
    if total > 0:
        with open('learning_data.json', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Replaced {total} occurrences in learning_data.json')
    else:
        print('String not found in learning_data.json.')
except Exception as e:
    print('Error LD:', e)

try:
    with open('learned_patterns.json', 'r', encoding='utf-8') as f:
        lp = json.load(f)
    if 'failed_patterns' in lp:
        for p in list(lp['failed_patterns'].keys()):
            val = lp['failed_patterns'][p].get('joi_response', '')
            if 'generate images directly' in val or 'capability to generate images' in val:
                del lp['failed_patterns'][p]
                print(f'Removed from learned_patterns: {p}')
    with open('learned_patterns.json', 'w', encoding='utf-8') as f:
        json.dump(lp, f, indent=2)
except Exception as e:
    print('Error LP:', e)
