import streamlit as st
from googletrans import Translator

def chatbot_response(user_input, lang='en'):
    responses = {
        "How can the chatbot help me market my product?": "The chatbot can assist with marketing by automatically responding to customer inquiries, sending special offers, collecting customer data, scheduling promotional messages, and enhancing user experience to boost sales.",
        "Can the chatbot reply to customers on my behalf?": "Yes! The chatbot can answer frequently asked questions 24/7, guide customers to the right products, and help facilitate purchases easily.",
        "Can the chatbot help me sell products?": "Absolutely! It can display your products in an organized manner, respond to customer inquiries, and direct them to purchase the product directly, whether from your website, WhatsApp, or Facebook.",
        "Can I use the chatbot to send offers to customers?": "Yes, you can send automated messages with exclusive offers and discounts to all your customers.",
        "Can the chatbot help me collect customer feedback?": "Yes! The chatbot can ask customers for reviews and feedback after a purchase, helping you improve your products and services.",
        "Can the chatbot remind customers about abandoned carts?": "Absolutely! The chatbot can send automated reminders to customers who left items in their cart, encouraging them to complete their purchase.",
        "Can the chatbot handle multiple customer inquiries at the same time?": "Yes! Unlike human agents, the chatbot can chat with multiple customers simultaneously, ensuring quick responses and better customer satisfaction.",
        "Can the chatbot personalize recommendations for customers?": "Of course! By analyzing customer preferences and purchase history, the chatbot can suggest relevant products to increase sales.",
        "Can the chatbot integrate with my social media pages?": "Yes, the chatbot can be linked to platforms like Facebook Messenger, WhatsApp, and Instagram, allowing seamless customer interaction across multiple channels.",
        
        "What are the types of digital advertisements?": "Digital advertisements can be classified into display ads, social media ads, search engine ads, video ads, email ads, and mobile app ads.",
        "How can I create a successful ad campaign?": "To create a successful ad campaign, identify your target audience, define clear goals, choose the right platform, create engaging content, and track performance metrics to optimize the campaign.",
        "What are the best advertising platforms for online marketing?": "Some of the best platforms for online advertising include Google Ads, Facebook Ads, Instagram Ads, LinkedIn Ads, and Twitter Ads.",
        "What is the difference between advertising on Facebook and Instagram?": "Facebook Ads are often used for a wider range of audiences and more detailed targeting options, while Instagram Ads are highly visual, ideal for engaging younger audiences with images and videos.",
        "How can I set a budget for ad campaigns?": "To set a budget, start with a daily or lifetime budget based on your campaign goals. Consider your target audience size, platform costs, and expected performance to estimate a reasonable budget.",
        "What is paid advertising vs. organic advertising?": "Paid advertising involves paying for ad space to reach your audience, while organic advertising relies on natural content and engagement to attract viewers without spending money.",
        "What advertising strategies can I use to increase sales?": "Strategies include targeting specific demographics, using retargeting ads, offering promotions, running seasonal campaigns, and utilizing user-generated content.",
        "How can I use Google Ads effectively?": "Use Google Ads by targeting specific keywords, creating compelling ad copy, optimizing landing pages, and continually monitoring and adjusting bids for the best return on investment.",
        "What is targeted advertising? How can I optimize it?": "Targeted advertising focuses on reaching a specific audience based on factors like location, behavior, and interests. You can optimize it by analyzing data, adjusting targeting parameters, and refining ad creatives.",
        "How can I track ad performance using measurement tools?": "Tools like Google Analytics, Facebook Insights, and platform-specific tracking features allow you to measure metrics such as click-through rates, conversions, and return on ad spend.",
        "What is ad retargeting? How do I use it?": "Ad retargeting involves showing ads to users who have interacted with your brand previously. You can use it by setting up retargeting campaigns on platforms like Google Ads and Facebook Ads.",
        "How can I optimize my ad campaign to be more effective?": "Optimize your campaign by testing different ad creatives, adjusting your target audience, improving landing pages, and analyzing performance to make data-driven adjustments."
    }
    response = responses.get(user_input, "Sorry, I don't understand that question.")
    
    translator = Translator()
    translated_response = translator.translate(response, dest=lang).text
    
    return translated_response

# Streamlit UI
st.title("Chatbot - AD CRAFT")

questions = list({
    "How can the chatbot help me market my product?",
    "Can the chatbot reply to customers on my behalf?",
    "Can the chatbot help me sell products?",
    "Can I use the chatbot to send offers to customers?",
    "Can the chatbot help me collect customer feedback?",
    "Can the chatbot remind customers about abandoned carts?",
    "Can the chatbot handle multiple customer inquiries at the same time?",
    "Can the chatbot personalize recommendations for customers?",
    "Can the chatbot integrate with my social media pages?",
    "What are the types of digital advertisements?",
    "How can I create a successful ad campaign?",
    "What are the best advertising platforms for online marketing?",
    "What is the difference between advertising on Facebook and Instagram?",
    "How can I set a budget for ad campaigns?",
    "What is paid advertising vs. organic advertising?",
    "What advertising strategies can I use to increase sales?",
    "How can I use Google Ads effectively?",
    "What is targeted advertising? How can I optimize it?",
    "How can I track ad performance using measurement tools?",
    "What is ad retargeting? How do I use it?",
    "How can I optimize my ad campaign to be more effective?"
})

question = st.selectbox("Choose a question:", questions)
language = st.selectbox("Choose a language:", ["en", "ar", "fr", "es", "de", "zh-cn", "ru", "it", "ja"])  # Add more languages if needed

if st.button("Ask Chatbot"):
    response = chatbot_response(question, language)
    st.write("**Chatbot:**", response)
