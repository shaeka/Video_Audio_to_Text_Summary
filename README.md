# Video/Audio to Text Summarization
Create a streamlit app that takes in video/audio converts it into text using Google Speech Recognition and provide summarized version of the text using Gemini Pro API.

The deployed app can be accessed [here](https://video-audio-to-text-summary.streamlit.app/)

![image](https://github.com/shaeka/Video_Audio_to_Text_Summary/assets/56749928/c07d54eb-f3c6-4336-bdc8-c0db34dfaed5)

![image](https://github.com/shaeka/Video_Audio_to_Text_Summary/assets/56749928/b6a956c9-0e73-4885-ad51-b54b71589eed)

# How to get your Gemini Pro API key:
Follow the instruction [here](https://ai.google.dev/pricing) to get your free API key

# Instruction on how to use this app locally
1. Download the file
2. Extract the file
3. Open up notepad, key in the following details and save the file as .env inside the extracted folder
```
GOOGLE_API_KEY="YOUR_API_KEY"
```
4. Open up anaconda prompt or command prompt and activate anaconda environment
5. Create a new conda environment
```
conda create --name new_env python==3.10 -y
```
6. Activate the environment
```
conda activate new_env
```
7. Change directory to the location of the extracted folder (e.g. in Downloads)
```
cd C:/Users/enter_your_user/Downloads/extracted_filename
```
8. Install the required libraries
```
pip install -r requirements.txt
```
9. Run streamlit app
```
streamlit run app.py
```

