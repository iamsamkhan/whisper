import moviepy.editor as mp
import speech_recognition as sr
import time

def video_to_text(video_file_path):
    # Extract audio from the video
    video_clip = mp.VideoFileClip(video_file_path)
    audio_clip = video_clip.audio

    # Save the extracted audio as a temporary file
    temp_audio_file = "temp_audio.wav"
    audio_clip.write_audiofile(temp_audio_file)

    # Start the timer for audio extraction
    start_time = time.time()

    # Transcribe the audio to text
    recognize_speech(temp_audio_file)

    # Stop the timer
    end_time = time.time()

    elapsed_time = end_time - start_time
    print("Video-to-Text Time: {:.2f} seconds".format(elapsed_time))

# Function to recognize speech using the speech_recognition library
def recognize_speech(audio_file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as audio_file:
        audio_data = recognizer.record(audio_file)

    try:
        text = recognizer.recognize_google(audio_data)
        print("Recognized Text: {}".format(text))
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# Example usage
video_file_path = "Speech-to-Text-Converter\\VideoTotext\\video.py"
video_to_text(video_file_path)
