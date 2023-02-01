import requests
import re

def get_js_files(domain):
    # Get the source code of the website
    try:
        response = requests.get("http://" + domain)
        source_code = response.text
    except:
        return []

    # Extract the URLs of all the JavaScript files
    js_files = re.findall(r'<script.*?src="(.*?)".*?>', source_code)

    return js_files

def search_for_secrets(js_file):
    try:
        response = requests.get(js_file)
        content = response.text
    except:
        return []

    # Search for secrets using regular expressions
    secrets = re.findall(r'(token|api_key|password|username|secret)', content, re.IGNORECASE)

    return secrets

# Read the list of domains from the input file
with open("domains.txt", "r") as f:
    domains = f.read().splitlines()

# Get the JavaScript files and search for secrets
output_js = []
for domain in domains:
    js_files = get_js_files(domain)
    for js_file in js_files:
        secrets = search_for_secrets(js_file)
        if secrets:
            output_js.append("[+] Secrets found in " + js_file)
            output_js.append("    Secrets: " + ", ".join(secrets))

# Write the results to the output file
with open("outputjs.txt", "w") as f:
    f.write("\n".join(output_js))
