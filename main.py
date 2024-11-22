import streamlit as st
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os

class AudioRecorder:
    def __init__(self):
        self.recording = None
        self.sample_rate = 44100
        self.temp_audio_file = None

    def start_recording(self):
        st.session_state.is_recording = True
        self.recording = sd.rec(int(self.sample_rate * 5), 
                                samplerate=self.sample_rate, 
                                channels=1, 
                                dtype='float64')

    def stop_recording(self):
        sd.stop()
        st.session_state.is_recording = False
        
        # Create a temporary file to save the recording
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            sf.write(temp_file.name, self.recording, self.sample_rate)
            self.temp_audio_file = temp_file.name

    def play_recording(self):
        if self.temp_audio_file and os.path.exists(self.temp_audio_file):
            data, _ = sf.read(self.temp_audio_file)
            sd.play(data, self.sample_rate)
            sd.wait()
        else:
            st.warning("No recording available. Please record first.")

def main():
    st.title("Speech Recorder")
    
    # Initialize session state
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    
    # Create AudioRecorder instance
    recorder = AudioRecorder()

    # Recording controls
    col1, col2 = st.columns(2)
    
    with col1:
        if not st.session_state.is_recording:
            if st.button("Start Recording", type="primary"):
                recorder.start_recording()
                st.experimental_rerun()
        else:
            if st.button("Stop Recording", type="secondary"):
                recorder.stop_recording()
                st.experimental_rerun()
    
    with col2:
        if st.button("Play Recording"):
            recorder.play_recording()

    # Display recording status
    if st.session_state.is_recording:
        st.info("Recording in progress...")
    elif recorder.temp_audio_file:
        st.success("Recording completed. Click 'Play Recording' to listen.")

if __name__ == "__main__":
    main()
