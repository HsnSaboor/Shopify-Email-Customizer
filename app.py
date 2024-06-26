import streamlit as st
from bs4 import BeautifulSoup
import re

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

# Streamlit app
st.title('Advanced Shopify Email Template GUI Editor')

template = st.text_area("Enter Shopify Email Template Code", height=300)

if st.button('Separate Code'):
    liquid_code, html_code, css_code, js_code = separate_code(template)
    
    st.subheader('Liquid Code')
    st.code('\n'.join(liquid_code))
    
    st.subheader('HTML Code')
    st.code(html_code, language='html')
    
    st.subheader('CSS Code')
    st.code(css_code, language='css')

    st.subheader('Combined HTML/CSS Code')
    combined_code = update_template(liquid_code, html_code, css_code, js_code)
    st.code(combined_code, language='html')
