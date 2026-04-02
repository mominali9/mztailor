import os
from openai import OpenAI

def get_chatbot_response(message):
    """
    Get a response from Hugging Face Inference Providers.
    Using moonshotai/Kimi-K2-Instruct-0905 via unified OpenAI-compatible endpoint.
    """
    hf_token = os.environ.get("HF_TOKEN")
    
    if not hf_token:
        # Mock response if token is not set
        lower_msg = message.lower()
        if 'size' in lower_msg or 'measure' in lower_msg:
            return "Our AI Measurement Studio allows you to upload a photo and get highly accurate size recommendations! Just click on 'AI Tailor' in the menu."
        elif 'shipping' in lower_msg or 'delivery' in lower_msg:
            return "We offer Free Express Shipping on all orders. (Note: HF_TOKEN is missing. Currently in mock mode.)"
        else:
            return "Thank you for your message! I'm the MZ Tailors AI Assistant. (Note: HF_TOKEN is missing. Currently in mock mode.)"
            
    try:
        client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=hf_token,
        )
        
        response = client.chat.completions.create(
            model="moonshotai/Kimi-K2-Instruct-0905",
            messages=[
                {"role": "system", "content": "You are a helpful customer support chatbot for MZ Tailors, a premium clothing brand. You help users with sizes, fabrics, shopping, and orders. Keep your answers concise, friendly, and persuasive."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error connecting to our AI brain: {str(e)}"
