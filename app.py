import streamlit as st

# Streamlit app
st.title('Shopify Email Template Editor')

# Option to choose global styles or manual CSS input
option = st.radio("Select CSS Input Method:", ('Global Styles (Sidebar)', 'Manual CSS Input'))

# Global Style Options
global_styles = {}
if option == 'Global Styles (Sidebar)':
    st.sidebar.header('Global Styles')
    global_styles = {
        'bg_color': st.sidebar.color_picker('Background Color'),
        'text_color': st.sidebar.color_picker('Text Color'),
        'button_bg_color': st.sidebar.color_picker('Button Background Color'),
        'button_text_color': st.sidebar.color_picker('Button Text Color'),
        'button_radius': st.sidebar.slider('Button Corner Radius', min_value=0, max_value=20, value=0),
        'table_color': st.sidebar.color_picker('Table lines color'),
        'link_color': st.sidebar.color_picker('Link color'),
        'product_title_color': st.sidebar.color_picker('Product Title color'),
        'logo_url': st.sidebar.text_input('Logo URL')
    }

# Option to input HTML <style> code manually
if option == 'Manual CSS Input':
    st.header('Manual CSS Input')
    html_styles_code = st.text_area('Enter CSS Styles Code', height=400)
    st.markdown(f"Example of CSS input:\n\n```html\n{html_styles_code}\n```")

# Original Email Template Input
st.header('Original Email Template')

original_code = st.text_area('Enter Original Email Template HTML Code', height=300)

# Original Email Template Subject
st.header("Original Email Template's Subject")

original_subject = st.text_area("Enter Original Email Template's Subject", height=50)

# Generate ChatGPT prompt
prompt = f"Enhance the Shopify email template with the following modifications:\n\n"
prompt += f"1. Keep the existing structure intact and centered.\n"

# Append global styles to prompt if selected
if option == 'Global Styles (Sidebar)' and any(global_styles.values()):
    prompt += f"2. Apply global styles:\n"
    prompt += f"   - Background Color: {global_styles['bg_color']}\n"
    prompt += f"   - Text Color: {global_styles['text_color']}\n"
    prompt += f"   - Button Background Color: {global_styles['button_bg_color']}\n"
    prompt += f"   - Button Text Color: {global_styles['button_text_color']}\n"
    prompt += f"   - Button Corner Radius: {global_styles['button_radius']}px\n"
    prompt += f"   - Table Lines Color: {global_styles['table_color']}\n"
    prompt += f"   - Link Color: {global_styles['link_color']}\n"
    prompt += f"   - Product Title Color: {global_styles['product_title_color']}\n"
    prompt += f"   - Logo in Header: Add the shop's logo using its liquid variable, default URL: {global_styles['logo_url']}\n\n"

# Append manual CSS input to prompt if selected
if option == 'Manual CSS Input' and html_styles_code:
    prompt += f"2. Apply custom styles from HTML <style> code:\n"
    prompt += f"```\n{html_styles_code}\n```\n"

prompt += f"3. Add an attractive greeting at the start of the email, incorporating the customer's name and emojis for Call-to-Action (CTA).\n"
prompt += f"4. Personalize the subject with the customer's first name and include a greeting and emoji (e.g., Hi! Customer's Name SUBJECT).\n"
prompt += f"5. Implement a Call-to-Action (CTA) using emojis.\n"
prompt += f"6. Utilize Liquid variables for personalized content.\n"
prompt += f"7. Provide a discount code 'NEXTORDER' for repeat customers, with a copy-to-clipboard feature for easy use.\n"
prompt += f"8. Ensure all styling is consistent and correct, fixing any discrepancies.\n"

st.markdown(prompt)

# Display inputted HTML styles code if manual CSS input is selected
if option == 'Manual CSS Input' and html_styles_code:
    st.header('Inputted CSS Styles Code')
    st.code(html_styles_code, language='html')

# Clear Input Field
if st.button('Clear Input'):
    st.text_area('Enter Original Email Template HTML Code', value='', height=300)
    if option == 'Manual CSS Input':
        st.text_area('Enter CSS Styles Code', value='', height=400)
