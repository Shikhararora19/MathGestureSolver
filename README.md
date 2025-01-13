# 📐 Math Gesture Solver

**Math Gesture Solver** is an interactive web application powered by **Streamlit** and **OpenAI** that recognizes hand gestures and solves math problems drawn in the air. By combining **computer vision** and **AI**, this project allows users to interact with math problems in a completely new way! 🙌

![Python](https://img.shields.io/badge/Language-Python-brightgreen?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/Computer%20Vision-OpenCV-blue?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/AI-OpenAI-lightgrey?style=for-the-badge)
![CVZone](https://img.shields.io/badge/Helper%20Library-CVZone-green?style=for-the-badge)
![streamlit-webrtc](https://img.shields.io/badge/WebRTC-streamlit--webrtc-orange?style=for-the-badge)



---

## 🎥 Demo Video

[![Watch the demo](https://img.youtube.com/vi/lFRdm6IchgQ/0.jpg)](https://www.youtube.com/watch?v=lFRdm6IchgQ)

---

## 🚀 Features

- ✋ **Gesture Recognition**: Detects hand gestures using a webcam and tracks movements in real time.
- 🖌️ **Air Drawing Canvas**: Draw math problems in the air using your index finger, and it appears on a digital canvas. Then you can erase them by showing all five fingers and you send your problem to AI by raising four fingers
- 🧠 **AI-Powered Solver**: Uses OpenAI's GPT model to analyze and solve math problems drawn on the canvas.
- 🎥 **Browser-based Webcam Support**: No installation required; use your browser's webcam.
- 🌐 **Responsive Design**: Fully functional on desktop and mobile browsers.

---

## 🛠️ Tech Stack

### **Frontend**
![Streamlit](https://img.shields.io/badge/Streamlit-Interactive-red?style=for-the-badge)
![streamlit-webrtc](https://img.shields.io/badge/WebRTC-streamlit--webrtc-orange?style=for-the-badge)

### **Backend**
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-blue?style=for-the-badge)
![CVZone](https://img.shields.io/badge/CVZone-Helper%20Library-green?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT%20API-lightgrey?style=for-the-badge)

---

## 💻 Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Shikhararora19/MathGestureSolver.git
   cd MathGestureSolver
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your OpenAI API Key to a `.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Run the application locally:
   ```bash
   streamlit run app.py
   ```

5. Open the app in your browser at `http://localhost:8501`.

---

## 🌟 How It Works

1. **Start the App**: The app will ask for webcam access.
2. **Draw Gestures**: Use your finger to draw math problems in the air (e.g., `3 + 5`).
3. **Trigger AI Solver**: Perform the `[1, 1, 1, 1, 0]` gesture (all fingers except the pinky up) to process and solve the problem.
4. **Get the Answer**: The AI will analyze the problem and display the solution in the "Answer" section.

---

## ✨ Features Roadmap (Future Work)

- 🔍 **Enhanced Gesture Detection**: Improve the accuracy of gesture tracking for complex shapes.
- 🧮 **Advanced Math Support**: Add support for equations, calculus, and graphs.
- 🌐 **Cloud Deployment**: Deploy the app on **Streamlit Cloud** or similar services.
- 🤖 **Custom AI Models**: Integrate a fine-tuned GPT model for better math problem-solving.
- 📱 **Mobile App**: Create a dedicated mobile app for gesture recognition and AI interaction.

---

## 🛡️ License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgments

- **Streamlit** for making interactive apps simple.
- **OpenCV** and **CVZone** for robust computer vision tools.
- **OpenAI** for their powerful GPT model.


---

## 📬 Contact

For questions or feedback, feel free to reach out:
- GitHub: [@Shikhararora19](https://github.com/Shikhararora19)
- Email: [shikhar3@ualberta.ca](mailto:shikhar3@ualberta.ca)
