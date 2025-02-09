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

st.set_page_config(page_title="Gesture AI", page_icon="🧊", layout="wide")
st.title("Gesture AI")

col1, col2 = st.columns([2,1])

with col1:
    run = st.checkbox("Run", value=True)
    FRAME_WINDOW = st.image([])

with col2:
    output_text_area = st.title("Answer")
    output_text_area = st.subheader("")

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"));

# Initialize webcam for video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)  # Height

# Initialize HandDetector
detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.7, minTrackCon=0.5)

prev_pos = None
canvas = None

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


# Streamlit main loop
canvas_placeholder = st.empty()  # Placeholder for the canvas
while cap.isOpened():
    success, img = cap.read()
    if not success:
        st.error("Failed to capture image from webcam.")
        break

    img = cv2.flip(img, 1)
    if canvas is None:
        canvas = np.zeros_like(img)

    info = getHandInfo(img)
    if info:
        fingers, lmlist = info
        prev_pos, canvas = draw(info, prev_pos, canvas, img)
        output_text = sendToAI(canvas, fingers)
        if output_text:
            output_text_area.text(output_text)
    

    # Combine images
    img_combo = cv2.addWeighted(img, 0.65, canvas, 0.35, 0)

    # Convert BGR to RGB for Streamlit
    img_rgb = cv2.cvtColor(img_combo, cv2.COLOR_BGR2RGB)
    canvas_rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)

    # Display in Streamlit
    canvas_placeholder.image(img_rgb, channels="RGB", use_container_width=True)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()