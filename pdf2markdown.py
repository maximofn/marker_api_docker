import requests
import os
import argparse
import base64
import re
import time

parser = argparse.ArgumentParser(description='Convert PDF to Markdown')
parser.add_argument('--pdf_file_path', type=str, required=True, help='Path to the PDF file to convert')


url = "http://localhost:8000/convert"


def main(args):
    pdf_file = args.pdf_file_path
    if not os.path.exists(pdf_file):
        raise FileNotFoundError(f'File not found: {pdf_file}')
    pdf_file_path = pdf_file.split('.')[:-1][0]
    if '/' in pdf_file:
        pdf_file_name = pdf_file_path.split('/')[-1]
    else:
        pdf_file_name = pdf_file_path

    with open(pdf_file, 'rb') as pdf_file:
        pdf_content = pdf_file.read()
    files = {'pdf_file': (os.path.basename(pdf_file_path), pdf_content, 'application/pdf')}
    params = {'extract_images': True}  # Optional parameter
    response = requests.post(url, files=files, params=params)

    if response.status_code == 200:
        # Convert the response to JSON
        response_json = response.json()

        # Create folder to save images and markdown file
        os.makedirs(pdf_file_name, exist_ok=True)

        # Save images
        for image in response_json['images']:
            image_name = f"{image}.png"
            image_content = response_json['images'][image]
            image_bytes = base64.b64decode(image_content)
            with open(f"{pdf_file_name}/{image_name}", 'wb') as image_file:
                image_file.write(image_bytes)
        
        # Find all reference to images in markdown text
        markdown_text = response_json['markdown']
        image_tags = re.findall(r'\[\d+_image_\d.png\]+', markdown_text)

        # Replace image tags by image names
        for i, image_tag in enumerate(image_tags):
            # print(f"replace {image_tag[1:-1]} by image_{i+1}.png")
            markdown_text = markdown_text.replace(image_tag[1:-1], f"image_{i+1}.png")

        # Save markdown file
        with open(f"{pdf_file_name}/{pdf_file_name}.md", 'w') as md_file:
            md_file.write(markdown_text)

    return 0

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)


