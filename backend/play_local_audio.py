from flask import Flask, request, Response, send_from_directory
from twilio.twiml.voice_response import VoiceResponse, Play

app = Flask(__name__)

# Replace this with your Ngrok URL
NGROK_URL = "https://8bb5-109-38-153-99.ngrok-free.app"

@app.route("/twiliowebhook", methods=['GET', 'POST'])
def voice():
    # Create a TwiML response
    response = VoiceResponse()

    # Play the audio file directly from your local directory
    audio_url = "/past_audio/my_audio.mp3"

    # Construct the full URL using Ngrok's public URL
    full_audio_url = f"{NGROK_URL}{audio_url}"

    # Play the audio file
    response.play(full_audio_url)

    return str(response)

@app.route("/past_audio/<path:filename>")
def serve_audio(filename):
    # Serve audio files from the 'audio' directory
    return send_from_directory("past_audio", filename)

if __name__ == "__main__":
    app.run(debug=True)

