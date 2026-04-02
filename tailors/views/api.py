import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tailors.chatbot import get_chatbot_response

@csrf_exempt
def chatbot_api(request):
    """API endpoint to handle AJAX requests from the floating chatbot widget."""
    if request.method == 'POST':
        try:
            # Handle both JSON body or form data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                user_msg = data.get('message', '')
            else:
                user_msg = request.POST.get('message', '')
                
            if not user_msg:
                return JsonResponse({'error': 'Message is empty'}, status=400)
                
            bot_reply = get_chatbot_response(user_msg)
            return JsonResponse({'reply': bot_reply})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=405)
