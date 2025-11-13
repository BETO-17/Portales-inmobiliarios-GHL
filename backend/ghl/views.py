import requests, os, json
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
BASE_GHL_URL = os.getenv("BASE_GHL_URL")

class InstallView(View):
    def get(self, request):
        auth_url = f"https://marketplace.gohighlevel.com/oauth/chooselocation?response_type=code&redirect_uri={REDIRECT_URI}&client_id={CLIENT_ID}"
        return HttpResponseRedirect(auth_url)

class CallbackView(View):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "No code provided"}, status=400)

        token_url = f"{BASE_GHL_URL}/oauth/token"
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        }

        res = requests.post(token_url, json=data)
        if res.status_code == 200:
            tokens = res.json()
            with open("tokens.json", "w") as f:
                json.dump(tokens, f)
            return JsonResponse({"status": "ok", "tokens": tokens})
        else:
            return JsonResponse({"error": res.text}, status=400)
