import streamlit as st
from bs4 import BeautifulSoup
import re
from streamlit_elements import elements, mui, html

# Function to separate Liquid, HTML, CSS, and JS
def separate_code(template):
    liquid_code = re.findall(r'{%.*?%}', template, re.DOTALL)
    html_code = re.sub(r'{%.*?%}', '', template)
    soup = BeautifulSoup(html_code, 'html.parser')

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
    template = ''.join(liquid_code) + str(soup)

    return template

# Function to generate editable HTML elements
def generate_editable_elements(soup):
    elements_dict = {}
    for tag in soup.find_all(True):
        elements_dict[tag.name] = elements_dict.get(tag.name, 0) + 1

    return elements_dict

# Function to create an editable block
def create_editable_block(tag, idx, element):
    with mui.Box(mb=2, p=2, border=1, borderColor="grey.400", borderRadius=2):
        element_content = str(element)
        element_html = st.text_area(f"{tag.upper()} {idx + 1} HTML", element_content, height=100)
        element_style = st.text_area(f"{tag.upper()} {idx + 1} CSS", '', height=50)
        return element_html, element_style

# Streamlit app
st.title('Advanced Shopify Email Template GUI Editor')

template = st.text_area("Enter Shopify Email Template Code", height=300)

if st.button('Separate Code'):
    liquid_code, html_code, css_code, js_code = separate_code(template)
    st.subheader('Liquid Code')
    st.code('\n'.join(liquid_code))
    
    st.subheader('HTML Code')
    soup = BeautifulSoup(html_code, 'html.parser')
    editable_elements = generate_editable_elements(soup)
    
    updated_html_blocks = []
    updated_css_blocks = []

    with elements("html_editor"):
        for tag, count in editable_elements.items():
            st.subheader(f'Edit {tag.upper()} elements ({count} found)')
            for idx, element in enumerate(soup.find_all(tag)):
                element_html, element_style = create_editable_block(tag, idx, element)
                updated_html_blocks.append(element_html)
                updated_css_blocks.append(element_style)
    
    st.subheader('CSS Code')
    css_code = st.text_area("Edit CSS Code", css_code, height=200)
    updated_css_blocks.append(css_code)
    final_css_code = "\n".join(updated_css_blocks)
    
    if st.button('Update Template'):
        updated_html_code = ''.join(updated_html_blocks)
        updated_template = update_template(liquid_code, updated_html_code, final_css_code, js_code)
        st.subheader('Updated Shopify Email Template')
        st.code(updated_template)
