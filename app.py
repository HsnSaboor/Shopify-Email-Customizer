import streamlit as st
from bs4 import BeautifulSoup
import re

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

# Streamlit app
st.title('Advanced Shopify Email Template Editor')

uploaded_file = st.file_uploader("Upload a Shopify Email Template File", type=['html', 'css', 'js'])

if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    st.text_area("File Content", value=file_content, height=300)

    if st.button('Separate Code'):
        liquid_code, html_code, css_code, js_code = separate_code(file_content)
        st.subheader('Liquid Code')
        st.code('\n'.join(liquid_code))

        st.subheader('HTML Code')
        st.code(html_code)

        st.subheader('CSS Code')
        st.code(css_code)

        st.subheader('JavaScript Code')
        st.code(js_code)

        st.success("Code separated successfully!")

    # Update Template Section
    if st.button('Get Final Template'):
        new_html_code = st.text_area("Enter Updated HTML Code", height=200, key='new_html')
        new_css_code = st.text_area("Enter Updated CSS Code", height=200, key='new_css')

        updated_template = update_template(liquid_code, new_html_code, new_css_code, js_code)
        st.subheader('Updated Shopify Email Template')
        st.code(updated_template)

st.markdown("""
<style>
.css-17skfb2 {
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 5px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)
