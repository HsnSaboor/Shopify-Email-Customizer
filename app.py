import streamlit as st

# Streamlit app
st.title('Shopify Email Template Editor')

st.sidebar.header('Global Styles')

# Global Style Options
global_styles = {
    'bg_color': st.sidebar.color_picker('Background Color'),
    'text_color': st.sidebar.color_picker('Text Color'),
    'button_bg_color': st.sidebar.color_picker('Button Background Color'),
    'button_text_color': st.sidebar.color_picker('Button Text Color'),
    'button_radius': st.sidebar.slider('Button Corner Radius', min_value=0, max_value=20, value=0),
    'logo_url': st.sidebar.text_input('Logo URL')
}

st.sidebar.markdown('---')
st.sidebar.text('© 2024 Shopify Editor')

# Original Email Template Input
st.header('Original Email Template')

original_code = st.text_area('Enter Original Email Template HTML Code', height=300)

# Original Email Template Subject
st.header("Original Email Template's Subject")

original_subject = st.text_area("Enter Original Email Template's Subject", height=50)

# Prompt Generation
st.header('ChatGPT Prompt')

# Generate ChatGPT prompt
prompt = f"Enhance the Shopify email template with the following modifications:\n\n"
prompt += f"8. keep the code structure the same:\n"
prompt += f"9. Align everything in the centre\n"
prompt += f"1. Apply global styles:\n"
prompt += f"   - Background Color: {global_styles['bg_color']}\n"
prompt += f"   - Text Color: {global_styles['text_color']}\n"
prompt += f"   - Button Background Color: {global_styles['button_bg_color']}\n"
prompt += f"   - Button Text Color: {global_styles['button_text_color']}\n"
prompt += f"   - Button Corner Radius: {global_styles['button_radius']}px\n"
prompt += f"   - Logo In HEADER in centre: add the shop's logo or use this link{global_styles['logo_url']}\n\n"
prompt += f"2. Add a Attractive greetings at start / first line of email and add customers name in it as well  of email and add emojis to it  (CTA) to the email template using emojis.\n"
prompt += f"7. Add customer first name in subject and a emoji with a greeting like Hi! customer's name SUBJECT. \n"
prompt += f"3. Add a call-to-action (CTA) to the email template using emojis.\n"
prompt += f"4. Use customer-related Liquid variables to personalize the email.\n"
prompt += f"5. If this email is only sent to those who have purchased at least once, give them a discount code 'NEXTORDER'. Make it copyable and add a copy to clipboard function for elements like tracking number, discount codes, etc.\n\n"
prompt += f"6. Add some left padding to all items keep buttons in the centre and remove the my comapnies address if mentioned anywhere i.e 28 Mosedale Way .... UK\n\n"
prompt += f"Original Email Template's Subject:\n\n"
prompt += f"```\n{original_subject}\n```\n"
prompt += f"Original Email Template HTML Code:\n\n"
prompt += f"```\n{original_code}\n```\n"

st.code(prompt, language='markdown')

# Clear Input Field
if st.button('Clear Input'):
    st.text_area('Enter Original Email Template HTML Code', value='', height=300)
