import speech_recognition as sr
import requests
import json
import time
import os


# ============================================================
# CONFIGURATION
# ============================================================

COMFY_URL = "http://127.0.0.1:8188"

WORKFLOW_FILE = "voice_to_video_api.json"

OUTPUT_FOLDER = os.path.join(
    os.getcwd(),
    "output"
)


# ============================================================
# SPEECH TO TEXT
# ============================================================

def speech_to_text():

    recognizer = sr.Recognizer()

    print()
    print("=" * 60)
    print("             🎤 VOICE TO VIDEO")
    print("=" * 60)
    print()

    with sr.Microphone() as source:

        print("🎤 Speak your video prompt now...")
        print("Example: A golden retriever running on the beach")
        print()

        # Reduce background noise
        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        audio = recognizer.listen(source)

    print()
    print("🔄 Converting speech to text...")

    try:

        text = recognizer.recognize_google(audio)

        print()
        print("✅ You said:")
        print(text)

        return text

    except sr.UnknownValueError:

        print("❌ Could not understand your speech.")
        return None

    except sr.RequestError as e:

        print("❌ Speech recognition service error:")
        print(e)

        return None


# ============================================================
# SAVE SPEECH TEXT TO JSON
# ============================================================

def save_voice_input(text):

    data = {
        "voice_prompt": text
    }

    with open(
        "voice_input.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print()
    print("💾 Voice input saved to:")
    print("   voice_input.json")


# ============================================================
# LOAD COMFYUI WORKFLOW
# ============================================================

def load_workflow():

    if not os.path.exists(WORKFLOW_FILE):

        print()
        print("❌ Workflow file not found:")
        print(WORKFLOW_FILE)

        print()
        print("Put voice_to_video_api.json inside:")
        print(os.getcwd())

        return None

    with open(
        WORKFLOW_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        workflow = json.load(f)

    return workflow


# ============================================================
# UPDATE POSITIVE PROMPT
# ============================================================

def update_positive_prompt(workflow, text):

    positive_node = None

    for node_id, node in workflow.items():

        if node.get("class_type") == "CLIPTextEncode":

            current_text = node.get(
                "inputs",
                {}
            ).get(
                "text",
                ""
            )

            # Detect the positive prompt
            if current_text != "":

                if not any(
                    word in current_text.lower()
                    for word in [
                        "blurry",
                        "ugly",
                        "distorted",
                        "low quality",
                        "bad anatomy"
                    ]
                ):

                    positive_node = node_id
                    break

    if positive_node is None:

        print("❌ Could not find positive CLIPTextEncode node.")
        return False

    workflow[positive_node]["inputs"]["text"] = text

    print()
    print("✅ Positive prompt node:", positive_node)
    print("📝 New prompt:", text)

    return True


# ============================================================
# SEND WORKFLOW TO COMFYUI
# ============================================================

def send_to_comfyui(workflow):

    print()
    print("🚀 Sending workflow to ComfyUI...")

    try:

        response = requests.post(
            f"{COMFY_URL}/prompt",
            json={
                "prompt": workflow
            }
        )

        response.raise_for_status()

        result = response.json()

        prompt_id = result.get("prompt_id")

        print()
        print("✅ Workflow submitted!")
        print("Prompt ID:", prompt_id)

        return prompt_id

    except Exception as e:

        print()
        print("❌ Could not send workflow to ComfyUI.")
        print(e)

        return None


# ============================================================
# WAIT FOR VIDEO GENERATION
# ============================================================

def wait_for_generation(prompt_id):

    print()
    print("🎬 Generating video...")
    print("This may take several minutes.")
    print()

    while True:

        try:

            response = requests.get(
                f"{COMFY_URL}/history/{prompt_id}"
            )

            history = response.json()

            if prompt_id in history:

                result = history[prompt_id]

                status = result.get(
                    "status",
                    {}
                )

                if status.get("completed"):

                    print()
                    print("✅ Video generation completed!")

                    return result

                if status.get("status_str") == "error":

                    print()
                    print("❌ ComfyUI reported an error.")

                    print(
                        json.dumps(
                            result,
                            indent=4
                        )
                    )

                    return None

        except Exception as e:

            print("Waiting for ComfyUI...", e)

        time.sleep(3)


# ============================================================
# FIND GENERATED VIDEO
# ============================================================

def find_output_files():

    print()
    print("🔍 Searching for generated video...")

    if not os.path.exists(OUTPUT_FOLDER):

        print("❌ Output folder not found.")

        return []

    files = []

    for root, dirs, filenames in os.walk(
        OUTPUT_FOLDER
    ):

        for filename in filenames:

            if filename.lower().endswith(
                (
                    ".webp",
                    ".webm",
                    ".mp4",
                    ".gif"
                )
            ):

                full_path = os.path.join(
                    root,
                    filename
                )

                files.append(full_path)

    return files


# ============================================================
# MAIN
# ============================================================

def main():

    # --------------------------------------------------------
    # STEP 1: SPEAK
    # --------------------------------------------------------

    text = speech_to_text()

    if not text:

        return

    # --------------------------------------------------------
    # STEP 2: SAVE VOICE INPUT
    # --------------------------------------------------------

    save_voice_input(text)

    # --------------------------------------------------------
    # STEP 3: LOAD WORKFLOW
    # --------------------------------------------------------

    workflow = load_workflow()

    if workflow is None:

        return

    # --------------------------------------------------------
    # STEP 4: INSERT SPEECH TEXT INTO PROMPT
    # --------------------------------------------------------

    success = update_positive_prompt(
        workflow,
        text
    )

    if not success:

        return

    # --------------------------------------------------------
    # STEP 5: SEND TO COMFYUI
    # --------------------------------------------------------

    prompt_id = send_to_comfyui(
        workflow
    )

    if prompt_id is None:

        return

    # --------------------------------------------------------
    # STEP 6: WAIT FOR GENERATION
    # --------------------------------------------------------

    wait_for_generation(
        prompt_id
    )

    # --------------------------------------------------------
    # STEP 7: FIND OUTPUT
    # --------------------------------------------------------

    files = find_output_files()

    print()

    if files:

        print("🎉 OUTPUT FILES:")
        print()

        for file in files[-10:]:

            print(file)

    else:

        print("⚠️ No output video found yet.")

    print()
    print("=" * 60)
    print("             DONE")
    print("=" * 60)


if __name__ == "__main__":

    main()