from fastapi.responses import HTMLResponse,JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
#from modules.request import SpeechRequest,modelanswer
from fastapi import FastAPI ,Form, UploadFile, File ,Request
from fastapi import HTTPException, status
from tempfile import NamedTemporaryFile
from transformers import pipeline
import torch
import tempfile
import numpy as np
#from pathlib import Path
from typing import Any, List, Union, Optional
import os
import whisper
import io
import asyncio
app = FastAPI()
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")


# # Define Gemini Pro API endpoint and API key (replace with your actual endpoint and API key)
# GEMINI_PRO_API_ENDPOINT = "https://api.gemini.com/pro"
# API_KEY = "your_api_key_here"


# Define the device
# Checking if NVIDIA GPU is available
pytorch_device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#print("Current PyTorch device is set to", pytorch_device)

# Load the pipeline
#model = pipeline(model="openai/whisper-small", device=pytorch_device)
#model = whisper.load_model("base", device=pytorch_device ,precision="fp16")

model = whisper.load_model("base", device=pytorch_device)
# Convert model parameters to FP32 if running on CPU
if pytorch_device == "cpu":
    model = model.float()

# pipe = pipeline(model="openai/whisper-small", device=pytorch_device)

# # Process the audio file
# predictions = pipe(audio_path, chunk_length_s=20, stride_length_s=5)

# # Extract the recognized text from the predictions
# recognized_text = predictions["text"]


# @app.post("/recognize/")
# def model_answer(request_to_class:modelanswer):
    
#     is_process_successful = model_answer(request_to_class)

#     if is_process_successful:
#         logger.info(f"Successfully parsed job description for incoming_request : {request_to_class}")
#     else:
#         logger.info(f"Failed to parse job description for incoming_request : {request_to_class}")
    
#     return {"is_process_successful" : is_process_successful}

# @app.post("/speech_recognize/")
# def speech_analysis(request_to_class:SpeechRequest):
    
#     is_process_successful = speech_analysis(request_to_class)

#     if is_process_successful:
#         logger.info(f"Successfully parsed job description for incoming_request : {request_to_class}")
#     else:
#         logger.info(f"Failed to parse job description for incoming_request : {request_to_class}")
    
#     return {"is_process_successful" : is_process_successful}


@app.post("/speech_recognize/")
async def handler(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files were provided")

    # For each file, let's store the results in a list of dictionaries.
    results = []

    for file in files:
        # Create a temporary file in the custom temporary directory.
        temp_file_path = os.path.join(temp_dir.name, file.filename)
        with open(temp_file_path, "wb") as temp_file:
            # Write the user's uploaded file to the temporary file.
            temp_file.write(file.file.read())
            
            # Let's get the transcript of the temporary file.
            result = model.transcribe(temp_file_path)
            
            # Now we can store the result object for this file.
            results.append({
                'filename': file.filename,
                'transcript': result['text'],
            })

    return {'results': results}
# Create a custom temporary directory
temp_dir = tempfile.TemporaryDirectory()

# @app.get("/create", response_class=RedirectResponse)
# async def redirect_to_docs():
#     return "/docs"


# async def handler(files: List[UploadFile] = File(...)):
#     if not files:
#         raise HTTPException(status_code=400, detail="No files were provided")

#     # For each file, let's store the results in a list of dictionaries.
#     results = []

#     for file in files:
#         # Create a temporary file.
#         with NamedTemporaryFile(delete=True) as temp:
#             # Write the user's uploaded file to the temporary file.
#             with open(temp.name, "wb") as temp_file:
#                 temp_file.write(file.file.read())
            
#             # Let's get the transcript of the temporary file.
#             result = model.transcribe(temp.name)

#             # Now we can store the result object for this file.
#             results.append({
#                 'filename': file.filename,
#                 'transcript': result['text'],
#             })

#     return JSONResponse(content={'results': results})

# @app.get("create", response_class=RedirectResponse)
# async def redirect_to_docs():
#     return "/docs"
#get model answer 
@app.post("/model_answer")
def update_item(question):
    if question == '1':
        return "Data Science Answer 1."
    if question == '2':
        return "Data Science Answer 2."
    else:
        return "No answer available."
    
    

#check scroe input video and model answer 
# @app.post("/get_score")
# def update_item(ans1, ans2):
#     return "100"



@app.post("/match_score")
async def get_match_score(speech: str, modelanswer: str):
    try:
        # Call the Gemini Pro API to get the matching score
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        }
        payload = {
            "speech": speech,
            "modelanswer": modelanswer
        }
        response = requests.post(f"{GEMINI_PRO_API_ENDPOINT}/match", headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        match_score = response.json()["match_score"]
        return {"match_score": match_score}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to call Gemini Pro API: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
