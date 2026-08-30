# Voice-to-Video Generation using Speech Recognition and ComfyUI

## 📌 Project Overview

This project is a real-time **Voice-to-Video Generation System** that converts a user's spoken prompt into an AI-generated video.

The system combines:

- 🎤 Real-time microphone input
- 🗣️ Speech-to-Text using Google Speech Recognition
- 📝 Automatic prompt generation/storage
- 🤖 ComfyUI as the AI video-generation engine
- 🎬 Wan 2.1 T2V 1.3B GGUF model for text-to-video generation
- ⚡ GPU acceleration using NVIDIA CUDA
- 📁 Automatic video output through ComfyUI

The main objective is to allow a user to simply **speak a description**, instead of manually typing a prompt, and receive a generated video.

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │       USER           │
                    │   🎤 Speaks Prompt   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Speech Recognition │
                    │   speech_recognition │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Text Prompt        │
                    │   Generated from     │
                    │   Speech Input       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   ComfyUI API        │
                    │   Workflow / Prompt   │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌──────────────────────────────────┐
              │       Wan 2.1 T2V 1.3B           │
              │             GGUF                 │
              │                                  │
              │   Text → Latent Video Frames    │
              └────────────────┬─────────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       Wan VAE        │
                    │   Video Decoding     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Video Output       │
                    │       🎬             │
                    └──────────────────────┘
```

---

## ✨ Features

### 1. Real-Time Voice Input
The system captures speech directly from the user's microphone.

### 2. Speech-to-Text Conversion
The spoken sentence is converted into text using the `SpeechRecognition` Python library and Google Speech Recognition.

### 3. Text-to-Video Generation
The recognized text is passed as the generation prompt to the ComfyUI workflow.

### 4. GGUF Model Support
The project uses the `ComfyUI-GGUF` custom node to load a quantized Wan 2.1 model.

### 5. GPU Acceleration
The system uses an NVIDIA GPU through CUDA to accelerate model execution.

### 6. Automatic Video Generation
After processing the spoken prompt, ComfyUI generates and saves the resulting video.

---

## 🧠 AI Model

### Wan 2.1 T2V 1.3B

The project uses:

```text
wan2.1_t2v_1.3b-q3_k_m.gguf
```

The model is a quantized GGUF version of the Wan 2.1 1.3B text-to-video model.

The model receives a natural-language prompt such as:

```text
A cinematic shot of a futuristic city at night with flying cars.
```

and generates video frames based on that description.

### Text Encoder

The project also uses:

```text
umt5-xxl-encoder-q4_k_m.gguf
```

The text encoder converts the input prompt into representations that can be used by the video-generation model.

### VAE

The Wan VAE is used to decode the generated latent representation into video frames.

---

## 🔧 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| SpeechRecognition | Speech-to-text interface |
| Google Speech Recognition | Converts speech into text |
| ComfyUI | AI workflow and inference engine |
| Wan 2.1 T2V 1.3B | Text-to-video generation |
| GGUF | Quantized model format |
| ComfyUI-GGUF | GGUF model loading support |
| PyTorch | Deep learning framework |
| CUDA | GPU acceleration |
| FFmpeg | Video processing |
| VAE | Latent-to-video decoding |
| JSON | Workflow/prompt configuration |

---

## 💻 Hardware / Environment

The project was tested on a Windows environment with an NVIDIA GPU.

The ComfyUI environment reported:

```text
OS: Windows
Python: 3.11.9
PyTorch: 2.7.1+cu118
CUDA: Available
GPU: NVIDIA GeForce RTX 3050 Laptop GPU
VRAM: ~4 GB
ComfyUI: 0.34.0
```

Because the GPU has limited VRAM, the project uses a quantized GGUF model and ComfyUI low-VRAM configuration.

Example ComfyUI launch configuration:

```text
--lowvram --cpu-vae
```

This reduces GPU memory requirements by moving/offloading some processing when necessary.

---

## 📂 Project Structure

A recommended project structure is:

```text
demo/
│
├── ComfyUi/
│   ├── main.py
│   ├── execution.py
│   │
│   ├── custom_nodes/
│   │   └── ComfyUI-GGUF/
│   │       ├── nodes.py
│   │       ├── loader.py
│   │       ├── ops.py
│   │       ├── dequant.py
│   │       └── requirements.txt
│   │
│   ├── models/
│   │   ├── diffusion_models/
│   │   │   └── wan2.1_t2v_1.3b-q3_k_m.gguf
│   │   │
│   │   ├── text_encoders/
│   │   │   └── umt5-xxl-encoder-q4_k_m.gguf
│   │   │
│   │   └── vae/
│   │       └── wan_2.1_vae.safetensors
│   │
│   └── output/
│       └── generated videos
│
├── voice_to_video.py
└── README.md
```

---

## ⚙️ Installation

### 1. Create / activate the Python environment

From the project directory:

```powershell
cd D:\os_backup\PROJECTS\demo
.\venv\Scripts\Activate.ps1
```

If PowerShell activation is unavailable, Python can still be executed directly from the virtual environment.

---

### 2. Install required Python packages

Install SpeechRecognition:

```powershell
pip install SpeechRecognition
```

Install microphone support:

```powershell
pip install PyAudio
```

Install requests:

```powershell
pip install requests
```

The ComfyUI-GGUF requirements can be installed with:

```powershell
pip install -r .\ComfyUi\custom_nodes\ComfyUI-GGUF\requirements.txt
```

---

## 🎙️ Speech-to-Text Component

The basic speech recognition component is:

```python
import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak something...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)

    print("You said:")
    print(text)

except sr.UnknownValueError:
    print("Sorry, I could not understand you.")

except sr.RequestError:
    print("Could not connect to the speech recognition service.")
```

This component:

1. Opens the microphone.
2. Waits for the user to speak.
3. Captures the audio.
4. Sends the audio for speech recognition.
5. Returns the recognized text.

---

## 🔗 Connecting Speech-to-Text with ComfyUI

The complete pipeline connects the recognized text to a ComfyUI workflow.

```text
Microphone
    ↓
Speech Recognition
    ↓
Recognized Text
    ↓
ComfyUI API
    ↓
Wan 2.1 T2V
    ↓
VAE Decode
    ↓
Video
```

The important concept is that the speech recognizer does **not** generate the video itself.

Instead:

```text
Speech → Text → ComfyUI Prompt → Wan 2.1 → Video
```

---

## 🌐 ComfyUI API

ComfyUI runs locally, for example:

```text
http://127.0.0.1:8188
```

The Python application can communicate with ComfyUI through its API.

For example:

```python
import requests

response = requests.get(
    "http://127.0.0.1:8188/system_stats"
)

print(response.status_code)
```

A successful response confirms that ComfyUI is available.

---

## 🔌 GGUF Model Configuration

The project uses the `ComfyUI-GGUF` custom node.

The following nodes were verified in the ComfyUI API:

```text
UnetLoaderGGUF
CLIPLoaderGGUF
DualCLIPLoaderGGUF
TripleCLIPLoaderGGUF
QuadrupleCLIPLoaderGGUF
UnetLoaderGGUFAdvanced
```

The main model loader is:

```text
Unet Loader (GGUF)
```

configured with:

```text
wan2.1_t2v_1.3b-q3_k_m.gguf
```

The text encoder uses:

```text
umt5-xxl-encoder-q4_k_m.gguf
```

---

## 🎬 Generation Workflow

The text-to-video workflow follows these major stages:

```text
1. Receive voice input
        ↓
2. Convert voice → text
        ↓
3. Send text to ComfyUI
        ↓
4. Load Wan GGUF model
        ↓
5. Encode text prompt
        ↓
6. Generate video latent
        ↓
7. Decode latent using Wan VAE
        ↓
8. Combine video frames
        ↓
9. Save video
```

---

## 📁 Output

ComfyUI stores generated files inside:

```text
ComfyUi/output/
```

For example:

```text
D:\os_backup\PROJECTS\demo\ComfyUi\output\
```

Generated files can include:

```text
ComfyUI_00001.mp4
ComfyUI_00002.mp4
```

depending on the workflow and output node configuration.

---

## ⚠️ Important Configuration Notes

### Low VRAM

The system uses:

```text
--lowvram
```

because the test system has approximately 4 GB of GPU VRAM.

This allows the model to operate by reducing GPU memory usage and offloading parts of the workload.

### CPU VAE

The configuration also used:

```text
--cpu-vae
```

which reduces GPU memory usage during VAE processing.

---

## 🛠️ Troubleshooting

### ComfyUI connection refused

Error:

```text
ConnectionRefusedError: [WinError 10061]
```

This usually means that ComfyUI is not currently running.

Start ComfyUI and verify:

```text
http://127.0.0.1:8188
```

Then run the API test again.

---

### GGUF node not found

Verify that:

```text
ComfyUi/custom_nodes/ComfyUI-GGUF/
```

contains:

```text
nodes.py
loader.py
ops.py
dequant.py
__init__.py
```

Then restart ComfyUI.

---

### Verify GGUF nodes

```powershell
python -c "import requests; d=requests.get('http://127.0.0.1:8188/object_info').json(); print([x for x in d if 'GGUF' in x or 'gguf' in x])"
```

Expected nodes include:

```text
UnetLoaderGGUF
CLIPLoaderGGUF
UnetLoaderGGUFAdvanced
```

---

### FFmpeg not found

Check:

```powershell
ffmpeg -version
```

If FFmpeg was installed using `winget`, restart PowerShell so the updated PATH is loaded.

---

## 🚀 Future Improvements

The current implementation successfully demonstrates the complete:

```text
Voice → Text → Video
```

pipeline.

Possible improvements include:

### 1. Longer Video Duration

Increase the number of generated frames and adjust the workflow to create longer clips.

### 2. Better Video Quality

Use a higher-quality Wan model quantization if sufficient VRAM is available.

Possible model variants include:

```text
q4
q5
q6
q8
```

Higher-quality variants generally require more memory.

### 3. Voice Activity Detection

Instead of waiting for a fixed listening operation, add voice activity detection so the application automatically detects when the user starts and stops speaking.

### 4. Local Speech Recognition

Replace Google Speech Recognition with an offline model such as Whisper to reduce dependency on an external speech-recognition service.

### 5. Web Interface

Create a web UI containing:

```text
┌─────────────────────────────────┐
│       VOICE TO VIDEO             │
├─────────────────────────────────┤
│                                 │
│       🎤 Speak Prompt            │
│                                 │
│   Recognized Text:              │
│   "A car driving through..."    │
│                                 │
│       [ Generate Video ]        │
│                                 │
│       🎬 Video Output            │
│                                 │
└─────────────────────────────────┘
```

### 6. Prompt Enhancement

An LLM can be added between Speech-to-Text and ComfyUI:

```text
Voice
  ↓
Speech-to-Text
  ↓
Prompt Enhancement
  ↓
ComfyUI
  ↓
Wan 2.1
  ↓
Video
```

This can transform short spoken descriptions into detailed cinematic prompts.

---

## 📊 Project Result

The project successfully demonstrates a local AI-powered voice-to-video workflow:

```text
🎤 User Speech
       ↓
📝 Speech-to-Text
       ↓
🤖 ComfyUI
       ↓
🎞️ Wan 2.1 T2V 1.3B GGUF
       ↓
🎬 Generated Video
```

The system was tested successfully with:

- Real-time microphone input
- Speech recognition
- ComfyUI local API
- Wan 2.1 T2V GGUF
- UMT5 GGUF text encoder
- Wan VAE
- NVIDIA CUDA GPU acceleration
- FFmpeg video processing

---

## 👨‍💻 Project Objective

The objective of this project is to build an accessible generative-AI interface where users can create videos naturally using their voice.

Instead of requiring the user to:

```text
Open ComfyUI
     ↓
Type a prompt
     ↓
Configure workflow
     ↓
Generate video
```

the system provides:

```text
Speak
  ↓
Automatic Text Conversion
  ↓
Automatic Video Generation
```

This makes text-to-video generation more natural and user-friendly.

---

## 📜 License

This project integrates third-party open-source software and AI models. Refer to the respective licenses of ComfyUI, ComfyUI-GGUF, Wan 2.1, GGUF, and other dependencies before redistribution or commercial deployment.

---

## 👨‍💻 Author

**Aravind R**

AI & Data Science Student | AI/ML Enthusiast

Project: **Real-Time Voice-to-Video Generation System**
