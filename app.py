from flask import Flask, render_template, request
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import os

app = Flask(__name__)

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        siteURL = request.form.get("url")
        try:
            key_path = os.getenv("GOOGLE_API_KEY_PATH")
            if not key_path or not os.path.exists(key_path):
                return "Google API key path is not configured correctly.", 500

            credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scopes=SCOPES)
            http = credentials.authorize(httplib2.Http())

            content = str({'url': siteURL, 'type': 'URL_UPDATED'})
            response, _ = http.request(ENDPOINT, method="POST", body=content)
            status = response['status']
            message = "✅ Successfully pinged Google Indexing API!" if status == '200' else f"❌ Error Code: {status}"
        except Exception as e:
            message = f"⚠️ Error: {str(e)}"
    return render_template("index.html", message=message)

if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
