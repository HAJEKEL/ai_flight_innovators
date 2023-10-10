import requests
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
app = Flask(__name__)
 
from elevenlabs import generate, set_api_key
set_api_key("redacted")
voice_id = "redacted"
 
# OpenAI API key
import openai
openai.api_key = "sk-redacted"
 
account_sid = "redacted"
auth_token = "redacted"
client = Client(account_sid, auth_token)
 
# Chat history - simple dictionary will work just fine
chat_history = {}
 
@app.route("/twiliowebhook", methods=['GET', 'POST'])
def voice():
    # Get the caller's phone number and make sure it's in the chat history
    from_number = request.values.get('From')
    if from_number not in chat_history:
        chat_history[from_number] = []
 
    # Start our TwiML response
    resp = VoiceResponse()
    
    # Use the 'say' verb to read a message aloud to the caller
    resp.say("Ask a question to our chatbot called Henk Jekel")

 
    # Read a message aloud to the caller
    #resp.play("https://trentk.xyz/audio/welcome.mp3")
 
    # Save the audio file of what the caller said
    resp.record(maxLength='5', action='/twiliorecord', finish_on_key='1')
 
    return str(resp)
 
@app.route("/twiliorecord", methods=['GET', 'POST'])
def record():
    # Get the audio file of what the caller said
    #print(request.values)
    recording_url = request.values['RecordingUrl']
    recording_sid = request.values['RecordingSid']
    recording_duration = request.values['RecordingDuration']
 
    from_user = request.values['From']
 
    # Get the mp3 file from `client`
    recording = client.recordings(recording_sid).fetch()
    full_url = "https://api.twilio.com" + recording.uri.replace(".json", ".mp3")
    r = requests.get(full_url, auth=(account_sid, auth_token))
    with open(f"recordings/{recording_sid}.mp3", "wb+") as f:
        f.write(r.content)
 
    # Send the audio file to OpenAI
    f = open(f"recordings/{recording_sid}.mp3", "rb")
    transcript = openai.Audio.transcribe("whisper-1", file=f)["text"]
    f.close()
    print(from_user,"says:",transcript)
 
    # Get a response from ChatGPT
    message_buffer = [
            {
                "role":"system",
                "content":"You are named Abby Shapiro. Respond in a slightly rude way to the user's inquiries, as though you're stuck helping them but don't really want to do so."
            },
    ]
    for i in range(len(chat_history[from_user])):
        message_buffer.append({
            "role":"user" if i % 2 == 0 else "assistant",
            "content":chat_history[from_user][i]
        })
    message_buffer.append({
        "role":"user",
        "content":transcript
    })
 
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=message_buffer,
        max_tokens=256
    )
    chatgpt_response = resp["choices"][0]["message"]["content"].strip()
    print("TrentBot says:",chatgpt_response)
 
    # Generate TTS audio with Eleven Labs
    audio = generate(text=chatgpt_response, voice=voice_id, model="eleven_multilingual_v2")
    with open(f"/var/www/html/audio/{recording_sid}_response.mp3", "wb+") as f:
        f.write(audio)
 
    # Build the response
    resp = VoiceResponse()
    resp.play(f"https://trentk.xyz/audio/{recording_sid}_response.mp3")
    resp.record(maxLength='5', action='/twiliorecord', finish_on_key='1')
 
    # Add these messages to the chat history
    chat_history[from_user].append(transcript)
    chat_history[from_user].append(chatgpt_response)
 
    return str(resp)
 
 
if __name__ == "__main__":
    # Run on port 5001
    app.run(debug=True, port=5001)