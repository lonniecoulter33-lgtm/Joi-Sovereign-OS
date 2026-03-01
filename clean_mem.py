import json
import re

try:
    with open('learning_data.json', 'r', encoding='utf-8') as f:
        content = f.read()

    count = content.count("I can't directly create")
    if count > 0:
        content = re.sub(r'\"I can\'t directly create[^\"]+\"', '\"[Attempted Image Generation] Please wait while I pull up my image generation tools...\"', content)
        with open('learning_data.json', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Replaced {count} occurrences in learning_data.json')
    else:
        print('String not found in learning_data.json.')
except Exception as e:
    print('Error:', e)
