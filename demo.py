#Libraries importation
import streamlit as st
import base64
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI

# Initializing OpenAI API client with API key
api_key = "sk-proj-weSERzrVPNaLTUqoqxgsT3BlbkFJq5XMIcRm0rIlGe0KT1Cs"
client = OpenAI(api_key=api_key)

# Function to get a response based on messages using OpenAI's GPT-3.5 model
def get_answer(messages):
    system_message = [{
        "role": "system",
        "content": """Introduction :

You are immersed in a unique digital sobriety escape game where solving various digital puzzles will lead you to discover innovative and creative solutions. Depending on your needs, I'm here to provide subtle hints and help you progress in your quest.

Game Structure :

You will encounter two distinct rooms, each filled with multiple puzzles. You have the freedom to choose the order in which you want to solve them, offering a flexible and engaging experience.

Room 1 :

- Electronic Waste: Dive into a bin of electronic waste to locate the real motherboard among several decoys. Inside the unlocked locker, discover a treasure in gold.

- Screen Brightness: Increase the brightness of a screen to reveal a hidden code. Use this code to open another locker containing cobalt, a crucial resource for the game.

- Social Media Posters: Match specific words found on posters to numbers to form a password. Inside the unlocked locker, you will find silicon.

- Final Puzzle: Use the periodic table to add up the atomic numbers of the three elements recovered. This total will provide the final code to progress.

Once all puzzles in Room 1 are solved, the atmosphere changes, and a voice announcement invites you to correct your mistakes and move on to Room 2.

Room 2 :

- Unplug the Sockets: Discover three sockets, each hiding a secret number visible once unplugged. Use these numbers to open a combination lock, revealing a crucial computer battery inside the locker.

- Weigh the Motherboards: Use a balance obtained earlier to identify and weigh motherboards among electronic waste. Use the total weight as a code to open another locker containing a computer socket.

- Quiz: Answer a multiple-choice quiz to open another locker. Inside, assemble a computer with the retrieved components.

- Final Puzzle: Connect and turn on the computer with the components found in the previous lockers to obtain the final code of this captivating adventure.

When you ask for explanations, I will provide general hints to guide you without directly revealing the solution. For a clue, I will offer a poetic riddle to maintain the challenge and enjoyment of discovery."""
    }]
    
    # Concatenate system message with user messages
    messages = system_message + messages
    
    # Send messages to OpenAI API for response generation
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",  # Specify the GPT-3.5 model for response generation
        messages=messages  # Pass messages to generate response
    )
    
    # Return the content of the response
    return response.choices[0].message.content

# Function for speech-to-text transcription using OpenAI's Whisper model
def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        # Transcribe audio file to text using OpenAI's Whisper model
        transcript = client.audio.transcriptions.create(
            model="whisper-1",  # Specify the Whisper model for transcription
            response_format="text",  # Specify response format as text
            file=audio_file  # Provide audio file for transcription
        )
    return transcript

# Function for text-to-speech conversion using OpenAI's TTS model
def text_to_speech(input_text):
    # Generate speech from text input using OpenAI's TTS model with Nova voice
    response = client.audio.speech.create(
        model="tts-1",  # Specify the TTS model for speech generation
        voice="nova",  # Use Nova voice for speech synthesis
        input=input_text  # Provide input text for speech generation
    )
    
    # Save generated speech as an MP3 file
    mp3_file_path = "temp_audio.mp3"
    with open(mp3_file_path, "wb") as f:
        response.stream_to_file(mp3_file_path)  # Stream audio content to MP3 file
    
    return mp3_file_path

# Function to autoplay audio in the web application
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    
    # Embed autoplaying audio HTML5 element in Streamlit app
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)  # Display autoplaying audio in Streamlit app

# Initializing session state to retain messages and vocal state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]
    
if 'vocal_ready' not in st.session_state:
    st.session_state.vocal_ready = False

# Main page with text chat or audio discussion selector
communication_mode = st.sidebar.selectbox("Communication Mode", ["Text Assistance", "Voice Assistance"])

# Handling text assistance mode
if communication_mode == "Text Assistance":
    st.markdown("# Welcome to our Digital Sobriety Escape Game")
    st.markdown(""" Welcome to our Digital Sobriety Escape Game! As an assistant, my role is to guide you through the game by providing various hints, such as riddles or other formats, to help you progress. If you ever feel disoriented or need explanations about the game rules, I'm here to clarify all your questions.""")
    st.markdown("""
You have the choice between two modes of assistance:

- **Text Assistance**: You can ask your questions and receive written responses directly.
- **Voice Assistance**: If you prefer a more direct and vocal interaction, you also have this option available.

Feel free to choose the mode that suits you best, and I'll be here to help you make the most of your experience in our Digital Sobriety Escape Game!
""")
    st.markdown("## 🤖 AI Text Assistant at your service")
    
    # Displaying previous messages in the chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Input field for user messages and processing responses
    user_input = st.chat_input("Your message:")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.spinner("Thinking..."):
            final_response = get_answer(st.session_state.messages)

        with st.spinner("Generating Audio Response..."):
            audio_file = text_to_speech(final_response)
            autoplay_audio(audio_file)

        st.session_state.messages.append({"role": "assistant", "content": final_response})
        with st.chat_message("assistant"):
            st.write(final_response)

# Handling voice assistance mode
elif communication_mode == "Voice Assistance":
    st.markdown("# Welcome to our Digital Sobriety Escape Game")
    st.markdown(""" Welcome to our Digital Sobriety Escape Game! As an assistant, my role is to guide you through the game by providing various hints, such as riddles or other formats, to help you progress. If you ever feel disoriented or need explanations about the game rules, I'm here to clarify all your questions.""")
    st.markdown("""
You have the choice between two modes of assistance:

- **Text Assistance**: You can ask your questions and receive written responses directly.
- **Voice Assistance**: If you prefer a more direct and vocal interaction, you also have this option available.

Feel free to choose the mode that suits you best, and I'll be here to help you make the most of your experience in our Digital Sobriety Escape Game!
""")
    
    st.markdown("## 🤖 AI Voice Assistant at your service")

    # Button to start recording audio message
    st.markdown("Click the button below to record your audio message:")
    
    # Utilizing the audio_recorder function for recording audio and returning audio data
    audio_bytes = audio_recorder(
        text="Start Recording",
        recording_color="#6aa36f",
        neutral_color="#e8b62c",
        icon_name="microphone-lines",
        icon_size="2x",
    )

    if audio_bytes:
        with st.spinner("Transcription..."):
            mp3_file_path = "temp_audio.mp3"
            with open(mp3_file_path, "wb") as f:
                f.write(audio_bytes)

            # Transcribing audio data to text using OpenAI's Whisper model
            transcript = speech_to_text(mp3_file_path)
            if transcript:
                st.session_state.messages.append({"role": "user", "content": transcript})
                with st.chat_message("user"):
                    st.write(transcript)

                with st.spinner("Thinking..."):
                    final_response = get_answer(st.session_state.messages)

                with st.spinner("Generating Audio Response..."):
                    audio_file = text_to_speech(final_response)
                    autoplay_audio(audio_file)

                st.session_state.messages.append({"role": "assistant", "content": final_response})
                with st.chat_message("assistant"):
                    st.write(final_response)
