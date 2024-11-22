import streamlit as st
import base64
import io
import wave

def audio_recorder():
    """
    Custom audio recorder using Web Audio API
    """
    st.markdown("""
    <script>
    let mediaRecorder;
    let audioChunks = [];

    async function startRecording() {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        
        audioChunks = [];
        mediaRecorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
        });

        mediaRecorder.start();
        document.getElementById('status').innerText = 'Recording...';
    }

    async function stopRecording() {
        mediaRecorder.stop();
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const reader = new FileReader();
        
        reader.onloadend = () => {
            const base64data = reader.result.split(',')[1];
            window.parent.postMessage({
                type: 'streamlit:setComponentValue', 
                payload: base64data
            }, '*');
        }
        
        reader.readAsDataURL(audioBlob);
        document.getElementById('status').innerText = 'Recording Stopped';
    }

    window.startRecording = startRecording;
    window.stopRecording = stopRecording;
    </script>
    <div id="status"></div>
    <button onclick="startRecording()" type="button">Start Recording</button>
    <button onclick="stopRecording()" type="button">Stop Recording</button>
    """, unsafe_allow_html=True)

def main():
    st.title("Web Audio Recorder")
    
    # Get audio data from browser
    audio_base64 = audio_recorder()
    
    if audio_base64:
        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_base64)
        
        # Option to play back
        st.audio(audio_bytes, format='audio/wav')
        
        # Save option
        st.download_button(
            label="Download Recording",
            data=audio_bytes,
            file_name='recording.wav',
            mime='audio/wav'
        )

if __name__ == "__main__":
    main()
