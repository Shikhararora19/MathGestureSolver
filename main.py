import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from openai import OpenAI
import dotenv
import os
from PIL import Image
import io
import base64
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.set_page_config(page_title="Gesture AI", page_icon="🧊", layout="wide")
st.title("Gesture AI")

col1, col2 = st.columns([2, 1])

with col1:
    run = st.checkbox("Run", value=True)
    FRAME_WINDOW = st.image([])

with col2:
    output_text_area = st.title("Answer")
    output_text_area = st.subheader("")

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize HandDetector
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)

prev_pos = None
canvas = None


class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.prev_pos = None
        self.canvas = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)

        if self.canvas is None:
            self.canvas = np.zeros_like(img)

        info = getHandInfo(img)
        if info:
            fingers, lmlist = info
            self.prev_pos, self.canvas = draw(info, self.prev_pos, self.canvas, img)
            output_text = sendToAI(self.canvas, fingers)
            if output_text:
                output_text_area.text(output_text)

        # Combine the live video feed and the canvas
        img_combo = cv2.addWeighted(img, 0.65, self.canvas, 0.35, 0)

        return img_combo

# Streamlit WebRTC Component
webrtc_streamer(
    key="gesture-ai",
    video_transformer_factory=VideoTransformer,
    media_stream_constraints={"video": True, "audio": False},
)


def getHandInfo(img):
    hands, img = detector.findHands(img, draw=True, flipType=True)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)
        return fingers, lmList
    return None


def draw(info, prev_pos, canvas, img):
    fingers, lmlist = info
    curr_position = None
    if fingers == [0, 1, 0, 0, 0]:  # Index finger up
        curr_position = lmlist[8][0:2]
        if prev_pos is None:
            prev_pos = curr_position
        cv2.line(canvas, tuple(prev_pos), tuple(curr_position), (255, 0, 255), 10)
    elif fingers == [1, 1, 1, 1, 1]:  # Thumb up
        canvas = np.zeros_like(img)
    return curr_position, canvas


def sendToAI(canvas, fingers):
    if fingers == [1, 1, 1, 1, 0]:  # Trigger condition
        pil_image = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        buffered = io.BytesIO()
        pil_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Send the image to the AI API
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Solve this Math problem and return answer in plain text."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_str}",
                            },
                        },
                    ],
                }
            ],
        )

        response_text = completion.choices[0].message.content
        return clean_response(response_text.strip())


def clean_response(response):
    """
    Cleans up AI-generated responses by formatting LaTeX properly
    and removing unnecessary escape sequences.
    """
    # Remove Markdown-like code block delimiters
    cleaned_response = response.replace("```", "").strip()
    return cleaned_response
