# 🎭 Advanced Emotion Detection App

A sophisticated emotion detection application powered by **YOLOv7** for face detection and **RepVGG** for emotion classification, wrapped in a beautiful Streamlit interface.

## 🌟 Features

### 🎯 **Advanced Detection Technology**
- **YOLOv7-tiny**: State-of-the-art face detection
- **RepVGG**: High-accuracy emotion classification
- **8 Emotion Classes**: anger, contempt, disgust, fear, happy, neutral, sad, surprise
- **Two-Stage Detection**: First detect faces, then classify emotions

### 📱 **User Interface**
- **📸 Image Upload**: Analyze emotions in uploaded images
- **🎬 Video Processing**: Process video files with emotion tracking
- **📹 Live Webcam**: Real-time emotion detection (planned)
- **📊 Emotion Statistics**: Detailed analysis and history
- **🎨 Beautiful UI**: Modern, responsive design with emojis and colors

### ⚙️ **Customizable Settings**
- **Face Detection Confidence**: Adjust sensitivity (0.1 - 1.0)
- **IoU Threshold**: Control detection overlap (0.1 - 1.0)
- **Video Processing**: Control frame sampling and processing limits
- **Real-time Controls**: Dynamic parameter adjustment

## 🚀 Quick Start

### 1. **Installation**
```bash
# Clone the repository
cd /home/Documents/aimoodmate/YOLO/emotion

# Install dependencies
pip install -r requirements.txt
pip install streamlit
```

### 2. **Run the App**
```bash
streamlit run streamlit_app.py
```

### 3. **Access the App**
Open your browser and go to: `http://localhost:8501`

## 📋 How to Use

### **📸 Image Analysis**
1. Click "📸 Image Upload"
2. Upload an image (PNG, JPG, JPEG)
3. Click "🔍 Analyze Emotions"
4. View detection results with bounding boxes and emotion labels
5. See detailed emotion analysis with confidence scores

### **🎬 Video Processing**
1. Click "🎬 Video Upload"
2. Upload a video file (MP4, AVI, MOV)
3. Set processing parameters:
   - **Max frames**: How many frames to process
   - **Frame skip**: Process every N frames
4. Click "🎬 Process Video"
5. View processed frames and emotion statistics

### **⚙️ Settings**
- **Face Detection Confidence**: Higher values = fewer false positives
- **IoU Threshold**: Controls overlap between detections
- **Load Models**: Initialize the detection models

## 🎨 Emotion Detection

### **Supported Emotions**
| Emotion | Emoji | Description |
|---------|-------|-------------|
| 😠 **Anger** | Red | Aggressive, frustrated expressions |
| 😏 **Contempt** | Purple | Disdainful, superior expressions |
| 🤢 **Disgust** | Green | Repulsed, revolted expressions |
| 😨 **Fear** | Yellow | Scared, anxious expressions |
| 😊 **Happy** | Lime | Joyful, cheerful expressions |
| 😐 **Neutral** | Gray | Calm, expressionless faces |
| 😢 **Sad** | Blue | Sorrowful, depressed expressions |
| 😲 **Surprise** | Cyan | Shocked, amazed expressions |

### **Detection Process**
1. **Face Detection**: YOLOv7 identifies face regions
2. **Face Cropping**: Extract face regions with bounding boxes
3. **Emotion Classification**: RepVGG analyzes facial features
4. **Confidence Scoring**: Provides reliability scores for each detection
5. **Visualization**: Draws colored bounding boxes with emotion labels

## 🔧 Technical Details

### **Models Used**
- **YOLOv7-tiny**: `weights/yolov7-tiny.pt` (Face detection)
- **RepVGG**: `weights/repvgg.pth` (Emotion classification)
- **Trained on**: WIDER FACE dataset + AffectNet dataset

### **Performance**
- **Face Detection**: ~13.2 GFLOPS
- **Emotion Classification**: High accuracy on 8 emotion classes
- **GPU Acceleration**: CUDA support for faster processing
- **Memory Efficient**: Optimized for real-time applications

### **Architecture**
```
Input Image/Video
       ↓
   YOLOv7-tiny
   (Face Detection)
       ↓
   Face Cropping
       ↓
   RepVGG Model
   (Emotion Classification)
       ↓
   Results + Visualization
```

## 📊 Features Breakdown

### **Image Processing**
- ✅ Upload and analyze single images
- ✅ Multiple face detection
- ✅ Emotion classification with confidence scores
- ✅ Visual results with colored bounding boxes
- ✅ Detailed emotion analysis cards

### **Video Processing**
- ✅ Frame-by-frame emotion analysis
- ✅ Configurable processing parameters
- ✅ Emotion statistics and distribution
- ✅ Sample frame display
- ✅ Average confidence calculations

### **User Experience**
- ✅ Modern, responsive UI design
- ✅ Real-time parameter adjustment
- ✅ Emotion history tracking
- ✅ Progress indicators
- ✅ Error handling and user feedback

## 🎯 Use Cases

### **Research & Development**
- Emotion recognition research
- Facial expression analysis
- Human-computer interaction studies
- Psychology and behavioral analysis

### **Applications**
- **Security Systems**: Emotion-based access control
- **Healthcare**: Patient mood monitoring
- **Education**: Student engagement analysis
- **Entertainment**: Interactive games and apps
- **Marketing**: Customer sentiment analysis

## 🔍 Troubleshooting

### **Common Issues**

1. **Models not loading**
   - Ensure all weight files are present in `weights/` folder
   - Check PyTorch installation and CUDA compatibility

2. **Low detection accuracy**
   - Adjust confidence threshold in sidebar
   - Ensure good lighting and face visibility
   - Try different IoU threshold values

3. **Performance issues**
   - Use GPU acceleration if available
   - Reduce video processing frame count
   - Increase frame skip interval

### **System Requirements**
- **Python**: 3.8+
- **PyTorch**: 1.7.0+
- **CUDA**: Optional but recommended
- **RAM**: 4GB+ recommended
- **Storage**: 2GB+ for models

## 📈 Future Enhancements

- [ ] **Live Webcam Support**: Real-time emotion detection
- [ ] **Batch Processing**: Multiple image processing
- [ ] **Export Results**: Save detection results to files
- [ ] **Model Comparison**: Compare different emotion models
- [ ] **Advanced Analytics**: Detailed emotion trend analysis
- [ ] **API Integration**: REST API for external applications

## 🤝 Contributing

This project is based on the excellent work by [George-Ogden/emotion](https://github.com/George-Ogden/emotion). The original repository provides the core emotion detection functionality, while this Streamlit app adds a user-friendly interface.

## 📄 License

This project is licensed under the GPL-3.0 license, following the original repository's licensing terms.

---

**🎭 Enjoy exploring emotions with AI!** 

For questions or issues, please refer to the original repository or create an issue in this project.