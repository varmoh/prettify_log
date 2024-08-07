import json
import re
from datetime import datetime
import os
import webbrowser

def prettify_log(log):
    log_entries = log.split('\n')
    prettified_entries = []

    for entry in log_entries:
        match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z) (INFO|ERROR|DEBUG) \[([^\]]+)\]  : (.*)', entry)
        if match:
            timestamp, level, ids, message = match.groups()
            try:
                json_body = json.loads(message.split(': ', 1)[1])
                pretty_json = json.dumps(json_body, indent=4, ensure_ascii=False)
                prettified_entries.append(f'{timestamp} {level} [{ids}] : {message.split(": ")[0]}: {pretty_json}')
            except (IndexError, json.JSONDecodeError):
                prettified_entries.append(entry)
        else:
            prettified_entries.append(entry)

    return '\n'.join(prettified_entries)

def generate_html(prettified_log, output_file_path):
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Log Output</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }}
        .container {{
            padding: 20px;
        }}
        .log {{
            white-space: pre-wrap;
            font-family: monospace;
            background-color: #f0f0f0;
            color: #000;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        .dark-mode .log {{
            background-color: #1e1e1e;
            color: #c5c5c5;
        }}
        .toggle-button {{
            margin: 20px;
            padding: 10px;
            cursor: pointer;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <button class="toggle-button" onclick="toggleMode()">Toggle Dark Mode</button>
        <div class="log" id="log-content">{prettified_log}</div>
    </div>
    <script>
        function toggleMode() {{
            document.body.classList.toggle('dark-mode');
        }}
    </script>
</body>
</html>
"""
    with open(output_file_path, 'w') as file:
        file.write(html_content)

def process_log_file(input_file_path):
    with open(input_file_path, 'r') as file:
        log_data = file.read()

    prettified_log = prettify_log(log_data).replace('\n', '<br>')

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file_path = f'log_output_{timestamp}.html'

    generate_html(prettified_log, output_file_path)

    webbrowser.open('file://' + os.path.realpath(output_file_path))

if __name__ == '__main__':
    input_file_path = 'log_input.txt'  # Path to the input log file
    process_log_file(input_file_path)
