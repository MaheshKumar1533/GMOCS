from django.shortcuts import render
import subprocess
import hmac
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Replace this with your GitHub Webhook Secret
GITHUB_SECRET = b"Thisissecretcode"

def verify_signature(payload, signature):
    mac = hmac.new(GITHUB_SECRET, payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest("sha256=" + mac, signature)

@csrf_exempt  # Disable CSRF for webhook requests
def github_webhook(request):
    if request.method == "POST":
        signature = request.headers.get("X-Hub-Signature-256")

        # Validate the request
        if not signature or not verify_signature(request.body, signature):
            return JsonResponse({"error": "Unauthorized"}, status=403)

        # Run git pull command
        try:
            subprocess.run(["git", "-C", "/home/GMOCS/GMOCS", "pull"], check=True)
            return JsonResponse({"message": "Updated successfully"}, status=200)
        except subprocess.CalledProcessError:
            return JsonResponse({"error": "Update failed"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


# Create your views here.
def index(request):
    return render(request, 'index.html')

# Just Updated