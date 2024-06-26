import streamlit as st
from zipfile import ZipFile
from bs4 import BeautifulSoup
import re
import os
from PIL import Image
import base64

# Function to separate Liquid, HTML, CSS, and JS and remove Liquid inside HTML tags
def separate_code(template):
    liquid_code = re.findall(r'{%.*?%}', template, re.DOTALL)
    html_code = re.sub(r'{%.*?%}', '', template)
    soup = BeautifulSoup(html_code, 'html.parser')

    # Remove Liquid code inside HTML tags
    for tag in soup.find_all(True):
        for liquid in tag.find_all(string=re.compile(r'{%.*?%}')):
            liquid.extract()

    css_code = '\n'.join([style.string for style in soup.find_all('style')])
    for style in soup.find_all('style'):
        style.decompose()

    js_code = '\n'.join([script.string for script in soup.find_all('script')])
    for script in soup.find_all('script'):
        script.decompose()

    return liquid_code, str(soup), css_code, js_code

# Function to update the template with edited HTML and CSS
def update_template(liquid_code, html_code, css_code, js_code):
    soup = BeautifulSoup(html_code, 'html.parser')

    # Add CSS back
    style_tag = soup.new_tag('style')
    style_tag.string = css_code
    soup.head.append(style_tag)

    # Add JS back
    script_tag = soup.new_tag('script')
    script_tag.string = js_code
    soup.body.append(script_tag)

    # Add Liquid code back
    for idx, tag in enumerate(soup.find_all(True)):
        liquid_placeholder = f'{{{{ liquid_{idx} }}}}'
        tag.insert_before(liquid_placeholder)
        tag.insert_after(liquid_placeholder)

    template = soup.prettify()
    for idx, liquid in enumerate(liquid_code):
        template = template.replace(f'{{{{ liquid_{idx} }}}}', liquid)

    return template

# Function to process uploaded files from ZIP archive
def process_zip_file(zip_file):
    with ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('temp_zip')

    file_paths = []
    for root, dirs, files in os.walk('temp_zip'):
        for file in files:
            if file.endswith(('.html', '.css', '.js')):
                file_paths.append(os.path.join(root, file))

    return file_paths

# Function to detect common CSS fields across all files
def detect_common_css(file_paths):
    common_css = set()

    if len(file_paths) > 0:
        first_file = file_paths[0]
        with open(first_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            style_tags = soup.find_all('style')
            for tag in style_tags:
                if tag.string:
                    for line in tag.string.split('\n'):
                        line = line.strip()
                        if line.startswith(('.', '#')):
                            selector = line.split('{')[0].strip()
                            common_css.add(selector)

    for file_path in file_paths[1:]:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            style_tags = soup.find_all('style')
            current_file_css = set()
            for tag in style_tags:
                if tag.string:
                    for line in tag.string.split('\n'):
                        line = line.strip()
                        if line.startswith(('.', '#')):
                            selector = line.split('{')[0].strip()
                            current_file_css.add(selector)

            common_css.intersection_update(current_file_css)

    return sorted(list(common_css))

# Function to apply global styles
def apply_global_styles(html_code, css_code, global_styles):
    soup = BeautifulSoup(html_code, 'html.parser')
    style_tag = soup.new_tag('style')
    
    # Apply global CSS styles
    global_css = ""
    if 'bg_color' in global_styles:
        global_css += f'body {{ background-color: {global_styles["bg_color"]}; }}\n'
    if 'text_color' in global_styles:
        global_css += f'body {{ color: {global_styles["text_color"]}; }}\n'
    if 'button_bg_color' in global_styles:
        global_css += f'.button {{ background-color: {global_styles["button_bg_color"]}; }}\n'
    if 'button_text_color' in global_styles:
        global_css += f'.button {{ color: {global_styles["button_text_color"]}; }}\n'

    style_tag.string = css_code + '\n' + global_css
    soup.head.append(style_tag)

    return str(soup)

# Function to update HTML elements with new properties (radius, margin, padding)
def update_html_elements(html_code, selected_elements, radius, margin, padding):
    soup = BeautifulSoup(html_code, 'html.parser')
    for element in selected_elements:
        selected_tags = soup.find_all(element)
        for tag in selected_tags:
            if radius:
                tag['style'] = f'{tag.get("style", "")} border-radius: {radius}px;'
            if margin:
                tag['style'] = f'{tag.get("style", "")} margin: {margin}px;'
            if padding:
                tag['style'] = f'{tag.get("style", "")} padding: {padding}px;'

    return str(soup)

# Streamlit app
st.title('Advanced Shopify Email Template Editor')

st.sidebar.header('Input Options')
input_option = st.sidebar.selectbox('Choose Input Option:', ['Manual Input', 'Upload ZIP File'])

global_styles = {}
st.sidebar.header('Global Styles')

# Logo Upload Option
logo_option = st.sidebar.radio('Logo Option:', ['Upload Logo', 'URL'])
if logo_option == 'Upload Logo':
    logo_file = st.sidebar.file_uploader('Upload Logo Image (PNG/JPG)', type=['png', 'jpg'])
    if logo_file is not None:
        logo_image = Image.open(logo_file)
        st.sidebar.image(logo_image, caption='Uploaded Logo', use_column_width=True)
elif logo_option == 'URL':
    logo_url = st.sidebar.text_input('Enter Logo URL')

# Global Style Options
global_styles['bg_color'] = st.sidebar.color_picker('Background Color')
global_styles['text_color'] = st.sidebar.color_picker('Text Color')
global_styles['button_bg_color'] = st.sidebar.color_picker('Button Background Color')
global_styles['button_text_color'] = st.sidebar.color_picker('Button Text Color')

# Detect common CSS fields
file_paths = []
common_css_fields = []
if input_option == 'Upload ZIP File':
    uploaded_zip_file = st.file_uploader('Upload ZIP File Containing HTML, CSS, and JS Files', type='zip')
    if uploaded_zip_file is not None:
        if st.button('Process ZIP File'):
            file_paths = process_zip_file(uploaded_zip_file)
            st.success(f'{len(file_paths)} files extracted from ZIP.')

            common_css_fields = detect_common_css(file_paths)
            st.success(f'Detected Common CSS Fields: {", ".join(common_css_fields)}')

# Process Input
selected_file_index = st.selectbox('Select File to Edit:', range(len(file_paths)), index=0) if file_paths else None
if input_option == 'Manual Input' and selected_file_index is not None:
    selected_file = file_paths[selected_file_index]

    with open(selected_file, 'r', encoding='utf-8') as file:
        original_code = file.read()
        liquid_code, html_code, css_code, js_code = separate_code(original_code)

        st.subheader('Liquid Code')
        st.code('\n'.join(liquid_code))

        st.subheader('HTML Code')
        st.code(html_code, language='html')

        st.subheader('CSS Code')
        st.code(css_code)

        st.subheader('JavaScript Code')
        st.code(js_code)

        st.success('Code separated successfully!')

        # Get Final Template
        if st.button('Get Final Template'):
            updated_html_code = st.text_area('Enter Updated HTML Code', value=html_code, height=300)
            updated_css_code = st.text_area('Enter Updated CSS Code', value=css_code, height=200)

            final_template = update_template(liquid_code, updated_html_code, updated_css_code, js_code)
            st.subheader('Updated Shopify Email Template')
            st.code(final_template)

elif input_option == 'Upload ZIP File' and len(file_paths) > 0:
    if selected_file_index is not None:
        selected_file = file_paths[selected_file_index]

        with open(selected_file, 'r', encoding='utf-8') as file:
            file_content = file.read()

            liquid_code, html_code, css_code, js_code = separate_code(file_content)

            st.subheader('Liquid Code')
            st.code('\n'.join(liquid_code))

            st.subheader('HTML Code')
            st.code(html_code, language='html')

            st.subheader('CSS Code')
            st.code(css_code)

            st.subheader('JavaScript Code')
            st.code(js_code)

            st.success('Code separated successfully!')

            # Update HTML elements with properties
            elements_to_edit = st.multiselect('Select Elements to Edit:', ['button', 'a', 'p', 'div', 'span'])
            if st.button('Apply Properties'):
                radius = st.slider('Border Radius (px)', min_value=0, max_value=50, value=0)
                margin = st.slider('Margin (px)', min_value=0, max_value=50, value=0)
                padding = st.slider('Padding (px)', min_value=0, max_value=50, value=0)

                updated_html = update_html_elements(html_code, elements_to_edit, radius, margin, padding)
                st.subheader('Updated HTML Code')
                st.code(updated_html, language='html')

            # Apply Global Styles
            if st.button('Apply Global Styles'):
                updated_template = apply_global_styles(html_code, css_code, global_styles)
                st.subheader('Updated Template with Global Styles')
                st.code(updated_template, language='html')

st.sidebar.markdown('---')
st.sidebar.text('© 2024 Shopify Editor')
