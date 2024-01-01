# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 20:43:43 2023

@author: kuany
"""

### 1. This program takes in a either video or audio 
### 2. If the given file is a video, extracts the audio from the video
### 3. Convert audio to text
### 4. Feed the text to Gemini Pro and ask it to summarize the text
### 5. Generate output (both raw text and summarize text)

import io
import os
import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
import moviepy.editor as mpe
import google.generativeai as genai

import tempfile

### Loading all the environmental variables
from dotenv import load_dotenv
load_dotenv() 

def convert_video_to_audio(temp_video_file):
    """
    Function extracts and returns audio from a given video
    
    Input: Video file path
    Output: Audio
    """
        
    # Create a VideoFileClip object
    video = mpe.VideoFileClip(temp_video_file.name)
    
    # Extract the audio from the video
    audio = video.audio

    return audio, video

def convert_audio_to_text(audio_path, video_path=None):
    """
    Function extracts and returns text from given audio
    
    Input: Audio
    Output: Converted Text
    """
    
    # Export audio to a temporary WAV file
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_audio_file_path = temp_audio_file.name
    audio_path.write_audiofile(temp_audio_file_path, codec='pcm_s16le')
    temp_audio_file.close()
    
    # Convert audio clip to a format compatible with speech recognition
    audio_data = AudioSegment.from_file(temp_audio_file_path)
    converted_text = ''

    # Export audio to a temporary WAV file
    temp_wav_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_wav_file_path = temp_wav_file.name
    audio_data.export(temp_wav_file_path, format="wav")
    temp_wav_file.close()

    # Initialize the speech recognition recognizer
    recognizer = sr.Recognizer()

    # Convert the audio to text
    with sr.AudioFile(temp_wav_file_path) as audio_record:
        audio = recognizer.record(audio_record)

        try:
            converted_text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            st.warning("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            st.warning(f"Could not request results from Google Speech Recognition service; {e}")

    # Remove the temporary files
    os.remove(temp_audio_file_path)
    os.remove(temp_wav_file_path)
    if video_path is not None:
        video_path.close()
    return converted_text

def gemini_summarize_text(text, text_model):
    """
    Function returns the summarized response from Gemini Pro after feeding the text from the audio/video input.
    
    Input: Text from audio/video
    Output: Summarized text
    """
    text = 'You are a language expert, provide a detailed summary of the following passage: {}'.format(text)
    response = text_model.generate_content(text)
    return response.text

def save_text_to_file(file_path, text):
    """
    Function saves the text into txt files
    
    Input: Save path of the new txt file and the text to save
    Output: .txt file saved in the given save path
    """
    # Open the file in write mode
    file = open(file_path, "w")
    file.write(text)
    file.close()

def main():
    st.title('Video/Audio to text summarization')
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    text_model = genai.GenerativeModel('gemini-pro')
    
    input_path = os.path.dirname(os.path.abspath(__file__)) + '/input/'
    output_path = os.path.dirname(os.path.abspath(__file__)) + '/output/'
    
    input_data = st.file_uploader('Choose a video/audio file', type=['mp4', 'mp3', 'wav'])
    
    video_file_extensions = [".mp4", ".mov", ".avi", ".wmv", ".flv", ".3gp"]
    audio_file_extensions = [".wav", ".mp3", ".ogg", ".flac", ".alac"]
    
    if input_data is not None:
        input_data_ext = '.' + input_data.name.split(".")[-1] 
        video = None
        # Create a temporary file
        temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=input_data_ext)
        temp_video_file_path = temp_video_file.name
        # Write the contents of the uploaded file to the temporary file
        with open(temp_video_file_path, 'wb') as temp_file:
            temp_file.write(input_data.read())
        temp_video_file.close()
    
        if input_data_ext in video_file_extensions:
            ### Convert video to audio
            audio, video = convert_video_to_audio(temp_video_file)
        if input_data_ext in audio_file_extensions:
            audio = mpe.AudioFileClip(temp_video_file.name)
        
        if video is not None:
            text = convert_audio_to_text(audio, video)
        else:
            text = convert_audio_to_text(audio)
        # Add a download button for the transcribed text
        st.download_button(
            label="Download Transcribed Text",
            data=text,
            key="download_transcribed_text",
            file_name="transcribed.txt",
            mime="text/plain")
        
        response = gemini_summarize_text(text, text_model)
        # Add a download button for the summarized text
        st.download_button(
            label="Download Summarized Text",
            data=response,
            key="download_summarized_text",
            file_name="summarized.txt",
            mime="text/plain")
        
        st.success('Successfully transcribe and summarize.')
        
        os.remove(temp_video_file_path)
        audio, video = None, None

if __name__ == "__main__":
    main()
