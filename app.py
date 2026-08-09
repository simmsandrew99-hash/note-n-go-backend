{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs24 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import os import tempfile import requests from flask import Flask, request, jsonify import openai import whisper importsubprocess app = Flask(__name__) # Set your OpenAI API key openai.api_key = os.getenv("OPENAI_API_KEY") # Load Whisper model once model = whisper.load_model("base") @app.route("/process", methods=["POST"]) defprocess_file(): data = request.json file_url = data.get("file_url") if not file_url: return jsonify(\{"error": "No file_url provided"\}), 400 try: # Download file video_path = tempfile.mktemp(suffix=".mp4") audio_path =tempfile.mktemp(suffix=".mp3") r = requests.get(file_url) with open(video_path, "wb") as f: f.write(r.content) # Extract audio using ffmpeg subprocess.run([ "ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path ]) # Transcribe with Whisper result = model.transcribe(audio_path) transcript = result["text"] # Generate notes with GPT completion =openai.ChatCompletion.create( model="gpt-4o-mini", messages=[ \{"role": "system", "content": "You create clean study notes."\}, \{"role": "user", "content": f"Turn this into bullet point notes and a study guide:\\n\\n\{transcript\}"\} ] ) notes =completion["choices"][0]["message"]["content"] return jsonify(\{ "transcript": transcript, "notes": notes \}) exceptException as e: return jsonify(\{"error": str(e)\}), 500 if __name__ == "__main__": app.run()}