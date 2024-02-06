import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

def transcribe_audio_chunk(audio_chunk):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_chunk) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")

def split_audio_into_chunks(audio_file_path, chunk_duration=30):
    audio = AudioSegment.from_file(audio_file_path)

    # Split the audio into chunks of specified duration
    chunks = split_on_silence(audio, silence_thresh=-40)

    # Ensure each chunk is at least the specified duration
    chunks = [chunk if len(chunk) >= chunk_duration * 1000 else chunk + AudioSegment.silent(duration=chunk_duration * 1000 - len(chunk)) for chunk in chunks]

    return chunks

if __name__ == "__main__":
    audio_file_path = "IELTS-16-test-1-section-1.mp3"  # Replace with your audio file path
    chunks = split_audio_into_chunks(audio_file_path)

    for i, chunk in enumerate(chunks):
        chunk.export(f"chunk_{i + 1}.wav", format="wav")
        text = transcribe_audio_chunk(f"chunk_{i + 1}.wav")
        print(f"Chunk {i + 1} Text: {text}")
