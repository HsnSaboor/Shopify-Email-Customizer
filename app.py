import streamlit as st
from bs4 import BeautifulSoup

# Function to apply global styles to the email template
def apply_global_styles(template, global_styles):
    soup = BeautifulSoup(template, 'html.parser')

    # Apply background color
    if global_styles['bg_color']:
        soup.body['style'] = f'background-color: {global_styles["bg_color"]};'

    # Apply text color
    if global_styles['text_color']:
        for tag in soup.find_all(['p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            tag['style'] = f'{tag.get("style", "")} color: {global_styles["text_color"]};'

    # Apply button styles
    if global_styles['button_bg_color'] or global_styles['button_text_color']:
        for tag in soup.find_all('a'):
            if global_styles['button_bg_color']:
                tag['style'] = f'{tag.get("style", "")} background-color: {global_styles["button_bg_color"]};'
            if global_styles['button_text_color']:
                tag['style'] = f'{tag.get("style", "")} color: {global_styles["button_text_color"]};'

    return str(soup)

# Streamlit app
st.title('Shopify Email Template Editor')

st.sidebar.header('Global Styles')

# Global Style Options
global_styles = {
    'bg_color': st.sidebar.color_picker('Background Color'),
    'text_color': st.sidebar.color_picker('Text Color'),
    'button_bg_color': st.sidebar.color_picker('Button Background Color'),
    'button_text_color': st.sidebar.color_picker('Button Text Color')
}

st.sidebar.markdown('---')
st.sidebar.text('© 2024 Shopify Editor')

# Original Email Template Input
st.header('Original Email Template')

original_code = st.text_area('Enter Original Email Template HTML Code', height=300)

# Apply Global Styles
if st.button('Apply Global Styles'):
    updated_template = apply_global_styles(original_code, global_styles)
    st.subheader('Updated Template with Global Styles')
    st.code(updated_template, language='html')

# Prompt Generation
st.header('ChatGPT Prompt')

# Generate ChatGPT prompt
prompt = f"Adds CTA to the email template using emojis. Uses customer-related Liquid variables to address the customer's first name, etc. Applies the following global styles:\n\n"
prompt += f"- Background Color: {global_styles['bg_color']}\n"
prompt += f"- Text Color: {global_styles['text_color']}\n"
prompt += f"- Button Background Color: {global_styles['button_bg_color']}\n"
prompt += f"- Button Text Color: {global_styles['button_text_color']}\n\n"
prompt += f"If this email is only sent to those who have purchased at least once, give them discount code 'NEXTORDER'. Make it copyable and add a copy to clipboard function for elements like tracking number, discount codes, etc."

st.code(prompt)

# Clear Input and Output Fields
if st.button('Clear Input and Output'):
    st.text_area('Enter Original Email Template HTML Code', value='', height=300)
    st.subheader('Updated Template with Global Styles')
    st.code('', language='html')
