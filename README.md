<h1 align="center">🎬 Pixelle-Video —— AI Fully Automated Short Video Engine</h1>

<p align="center"><a href="README_EN.md">English</a> | <a href="README.md">中文</a></p>

<p align="center">
  <a href="https://www.bilibili.com/video/BV1WzyGBnEVp/?vd_source=e7e7d4ca8db9a18c80f17a24a6582fca" target="_blank"><img src="https://img.shields.io/badge/🎥 Video%20Tutorial-EA4C89" alt="Video Tutorial"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/releases" target="_blank"><img src="https://img.shields.io/badge/📦 Windows%20Package-50C878" alt="Windows Package"></a>
  <a href="https://aidc-ai.github.io/Pixelle-Video/zh" target="_blank"><img src="https://img.shields.io/badge/📘 Documentation-4A90E2" alt="Documentation"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/stargazers"><img src="https://img.shields.io/github/stars/AIDC-AI/Pixelle-Video.svg" alt="Stargazers"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/issues"><img src="https://img.shields.io/github/issues/AIDC-AI/Pixelle-Video.svg" alt="Issues"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/network/members"><img src="https://img.shields.io/github/forks/AIDC-AI/Pixelle-Video.svg" alt="Forks"></a>
  <a href="https://github.com/AIDC-AI/Pixelle-Video/blob/main/LICENSE"><img src="https://img.shields.io/github/license/AIDC-AI/Pixelle-Video.svg" alt="License"></a>
</p>

https://github.com/user-attachments/assets/a42e7457-fcc8-40da-83fc-784c45a8b95d

<br/>

Just input a **topic**, and Pixelle-Video will automatically:
- ✍️ Write video script
- 🎨 Generate AI images/videos
- 🗣️ Synthesize voice narration
- 🎵 Add background music
- 🎬 Compose video with one click

**Zero threshold, zero editing experience required** - Make video creation as simple as typing a sentence!


## 🖥️ Web Interface Preview

![Web UI Interface](resources/webui.png)


## 📋 Recent Updates

- ✅ **2026-06-01**: Added direct API media model configuration in WebUI, including image/video provider credentials, Base URLs, and per-provider proxy toggles
- ✅ **2026-01-26**: Added the Motion Transfer pipeline — upload a reference video and an image to transfer motion.
- ✅ **2026-01-14**: Added "AI Digital Avatar" and "Image-to-Video" pipelines, multi-language TTS voices support
- ✅ **2026-01-06**: Added RunningHub 48G VRAM machine support
- ✅ **2025-12-28**: Configurable RunningHub concurrency limit, improved LLM structured data response handling
- ✅ **2025-12-17**: Added ComfyUI API Key configuration, Nano Banana model support, API template custom parameters
- ✅ **2025-12-10**: Built-in FAQ in sidebar, fixed edge-tts version to resolve TTS service instability
- ✅ **2025-12-08**: Support multiple script split modes (paragraph/line/sentence), improved template selection with direct preview
- ✅ **2025-12-06**: Fixed video generation API URL path handling with cross-platform compatibility
- ✅ **2025-12-05**: Added Windows all-in-one package download, optimized image and video analysis workflows
- ✅ **2025-12-04**: New "Custom Media" feature - upload your photos/videos with AI-powered analysis and script generation
- ✅ **2025-11-18**: Parallel processing for RunningHub, added history page, batch video task creation support


## ✨ Key Features

- ✅ **Fully Automatic Generation** - Input a topic, automatically generate complete video
- ✅ **AI Smart Copywriting** - Intelligently create narration based on topic, no need to write scripts yourself
- ✅ **AI Generated Images** - Each sentence comes with beautiful AI illustrations
- ✅ **AI Generated Videos** - Support AI video generation models (like WAN 2.1) to create dynamic video content
- ✅ **Direct Model APIs** - Directly call image/video generation services from DashScope, OpenAI, Seedream, Seedance, Kling, and more
- ✅ **AI Generated Voice** - Support Edge-TTS, Index-TTS and many other mainstream TTS solutions
- ✅ **Background Music** - Support adding BGM to make videos more atmospheric
- ✅ **Visual Styles** - Multiple templates to choose from, create unique video styles
- ✅ **Flexible Dimensions** - Support portrait, landscape and other video dimensions
- ✅ **Multiple AI Models** - Support GPT, Qwen, DeepSeek, Ollama and more
- ✅ **Flexible Atomic Capability Combination** - Supports ComfyUI / RunningHub workflows and direct API models, allowing image, video, TTS, VLM and other capabilities to be swapped as needed


## 📊 Video Generation Pipeline

Pixelle-Video adopts a modular design, the entire video generation process is clear and concise:

![Video Generation Flow](resources/flow.png)

From input text to final video output, the entire process is clear and simple: **Script Generation → Image Planning → Frame-by-Frame Processing → Video Composition**

Each step supports flexible customization, allowing you to choose different AI models, audio engines, visual styles, etc., to meet personalized creation needs.


## 🎬 Video Examples

Here are actual cases generated using Pixelle-Video, showcasing video effects with different themes and styles:

### 📱 Extension Module Video Showcase

<table>
<tr>
<td width="33%">
<h3>👤 AI Digital Avatar</h3>
<video src="https://github.com/user-attachments/assets/7c122563-c2e0-4dcd-a73c-25ba1d4fa2dd" controls width="100%"></video>
<p align="center"><b>Korean-speaking AI Avatar</b></p>
</td>
<td width="33%">
<h3>🖼️ Image-to-Video</h3>
<video src="https://github.com/user-attachments/assets/5b4eef17-07d0-4bde-9748-2ed68cc9888e" controls width="100%"></video>
<p align="center"><b>Animated Cartoon Video</b></p>
</td>
<td width="33%">
<h3>💃 Motion Transfer</h3>
<video src="https://github.com/user-attachments/assets/7b1240bc-e965-434c-b343-118ec4793d4f" controls width="100%"></video>
<p align="center"><b>Dancing Kitten</b></p>
</td>
</tr>
</table>


### 📱 Portrait Video Showcase

<table>
<tr>
<td width="33%">
<h3>🌄 Documentary & Lifestyle – Default Template</h3>
<video src="https://github.com/user-attachments/assets/e6716c1d-78de-453d-84c2-10873c8c595f" controls width="100%"></video>
<p align="center"><b>The Scenery Along the Journey</b></p>
</td>
<td width="33%">
<h3>🔍 Cultural Deconstruction – Default Template</h3>
<video src="https://github.com/user-attachments/assets/f5de75f6-135a-4ab4-9f5f-079f649764d5" controls width="100%"></video>
<p align="center"><b>Santa ID</b></p>
</td>
<td width="33%">
<h3>🔭 Scientific Inquiry – Default Template</h3>
<video src="https://github.com/user-attachments/assets/ceb8b0df-8331-4e1f-88e7-db5b295a1c1d" controls width="100%"></video>
<p align="center"><b>Why Haven't We Found Alien Civilizations Yet?</b></p>
</td>
</tr>
<tr>
<td width="33%">
<h3>🌱 Personal Growth – Cloned Voice</h3>
<video src="https://github.com/user-attachments/assets/1bad9a49-df83-4905-9cc8-9a7640e9c7d8" controls width="100%"></video>
<p align="center"><b>How to Level Up Yourself</b></p>
</td>
<td width="33%">
<h3>🧠 Deep Thinking – Default Template</h3>
<video src="https://github.com/user-attachments/assets/663b705a-2aea-44bc-b266-4bb27aa255a8" controls width="100%"></video>
<p align="center"><b>Understanding Antifragility</b></p>
</td>
<td width="33%">
<h3>🏯 History & Culture – Static Frame</h3>
<video src="https://github.com/user-attachments/assets/56e0a018-fa99-47eb-a97f-fc2fa8915724" controls width="100%"></video>
<p align="center"><b>Zizhi Tongjian (Comprehensive Mirror for Aid in Governance)</b></p>
</td>
</tr>
<tr>
<td width="33%">
<h3>☀️ Emotional Storytelling – Cloned Voice</h3>
<video src="https://github.com/user-attachments/assets/4687df95-dd21-4a7b-b01e-f33a7b646644" controls width="100%"></video>
<p align="center"><b>Winter Sunlight</b></p>
</td>
<td width="33%">
<h3>📜 Novel Adaptation – Custom Script</h3>
<video src="https://github.com/user-attachments/assets/d354465e-3fa8-40b4-93e9-61ad75ef0697" controls width="100%"></video>
<p align="center"><b>Doupo Cangqiong (Battle Through the Heavens)</b></p>
</td>
<td width="33%">
<h3>🧬 Knowledge Explainer – Qwen Image Generation</h3>
<video src="https://github.com/user-attachments/assets/8ac21768-41ce-4d41-acdd-e3dd3eb9725a" controls width="100%"></video>
<p align="center"><b>Essential Wellness Tips</b></p>
</td>
</tr>
</table>

### 🖥️ Landscape Video Showcase

<table>
<tr>
<td width="50%">
<h3>💰 Side Hustle Money Making – Movie Template</h3>
<video src="https://github.com/user-attachments/assets/c9209d4e-73a6-4b82-aaad-cf102248c9e2" controls width="100%"></video>
<p align="center"><b>Side Hustle Money Making</b></p>
</td>
<td width="50%">
<h3>🏛️ Historical Commentary – Custom Template</h3>
<video src="https://github.com/user-attachments/assets/a767c452-d5f1-4cff-bb34-b80fff0d4c3e" controls width="100%"></video>
<p align="center"><b>Insights from Zizhi Tongjian</b></p>
</td>
</tr>
</table>

> 💡 **Tip**: All these videos are fully automatically generated by AI just by inputting a topic keyword, without any video editing experience required!


<div id="tutorial-start" />


## 🚀 Quick Start

### 🪟 Windows All-in-One Package (Recommended for Windows Users)

**No need to install Python, uv, or ffmpeg - ready to use out of the box!**

👉 **[Download Windows All-in-One Package](https://github.com/AIDC-AI/Pixelle-Video/releases/latest)**

1. Download the latest Windows All-in-One Package and extract it
2. Double-click `start.bat` to launch the Web interface
3. Your browser will automatically open http://localhost:8501
4. Configure LLM API and image generation service under "⚙️ System Configuration"
5. Start generating videos!

> 💡 **Tip**: The package includes all dependencies - no manual environment setup needed. Just configure your API keys on first use.


### Install from Source (For macOS / Linux Users or Users Who Need Customization)

#### Prerequisites

Before getting started, you need to install the Python package manager `uv` and the video processing tool `ffmpeg`:

##### Install uv

Please visit the official uv documentation for installation methods for your system:  
👉 **[uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)**

After installation, run `uv --version` in the terminal to verify successful installation.

##### Install ffmpeg

**macOS**
```bash
brew install ffmpeg
```

**Ubuntu / Debian**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows**
- Download URL: https://ffmpeg.org/download.html
- After downloading, extract and add the `bin` directory to your system's PATH environment variable.

After installation, run `ffmpeg -version` in the terminal to verify successful installation.


#### Step 1: Download the Project

```bash
git clone https://github.com/AIDC-AI/Pixelle-Video.git
cd Pixelle-Video
```

#### Step 2: Launch the Web Interface

```bash
# Run with uv (recommended, automatically installs dependencies)
uv run streamlit run web/app.py
```

Your browser will automatically open http://localhost:8501

#### Step 3: Configure in the Web Interface

On first use, expand the "⚙️ System Configuration" panel and fill in:
- **LLM Configuration**: Select an AI model (such as Qwen, GPT, etc.) and enter the API Key
- **ComfyUI / RunningHub Configuration**: If you want to use workflows for image, video, or voice generation, configure your local ComfyUI address or RunningHub API Key.
- **API Media Model Configuration**: If you want to directly connect to image/video models, configure API Key, Base URL, and proxy options for providers such as DashScope, OpenAI, ARK, Kling.

After configuring, click "Save Configuration", and you can start generating videos!

<div id="tutorial-end" />

## 💻 Usage

After opening the Web interface, you'll see a three-column layout. Below is a detailed explanation of each part:


### ⚙️ System Configuration (Required on First Use)

Configuration is required on first use. Click to expand the "⚙️ System Configuration" panel:

#### 1. LLM Configuration (Large Language Model)
Used to generate video scripts.

**Quick Select Preset**  
- Select a preset model from the dropdown menu (Qwen, GPT-4o, DeepSeek, etc.)
- After selection, base_url and model will be filled in automatically
- Click the "🔑 Get API Key" link to register and obtain a key

**Manual Configuration**  
- API Key: Enter your key
- Base URL: API address
- Model: Model name

#### 2. ComfyUI / RunningHub Configuration
Used to generate video images, video clips, and voice via ComfyUI workflows.

**Local Deployment (Recommended)**  
- ComfyUI URL: Local ComfyUI service address (default http://127.0.0.1:8188)
- Click "Test Connection" to confirm the service is available

**Cloud Deployment**  
- RunningHub API Key: Key for the cloud image generation service

#### 3. API Media Model Configuration
Used to call image, video, or asset analysis model providers directly without relying on ComfyUI/RunningHub.

**Supported Providers**
- OpenAI / GPT Image: For GPT image generation models
- DashScope / Wan / HappyHorse: For Alibaba Tongyi Wan image and video generation
- Volcengine ARK / Seedream / Seedance: For ByteDance Seedream images and Seedance video generation
- Kling AI: For Kling video generation

**Configurable Options**
- API Key / Access Key / Secret Key: Provider authentication credentials
- Base URL: Model service endpoint; WebUI provides official defaults
- Local Proxy: e.g., `http://127.0.0.1:9090`
- Enable Proxy: Each provider can independently choose whether to route through the local proxy
- Print Model Request Parameters: For debugging, prints the prompt, model name, and input file paths sent to the model in the terminal

> 💡 If you only use ComfyUI or RunningHub, you can leave the API Media Model Configuration empty; if you select `api/...` workflows, you need to configure the corresponding provider's credentials.

After configuration, click "Save Configuration".


### 📝 Content Input (Left Column)

#### Generation Mode
- **AI Generated Content**: Input a topic and AI will automatically write the script.
  - Suitable for: Quickly generating videos and letting AI write the script
  - Example: "Why develop reading habits"
- **Fixed Script Content**: Directly input the complete script, skipping AI creation.
  - Suitable for: Already having a finished script and directly generating video

#### Background Music (BGM)
- **No BGM**: Pure voice narration
- **Built-in Music**: Select preset background music (e.g., default.mp3)
- **Custom Music**: Place your music files (MP3/WAV, etc.) in the `bgm/` folder
- Click "Preview BGM" to preview the music


### 🎤 Voice Settings (Middle Column)

#### TTS Workflow
- Select a TTS workflow from the dropdown menu (supports Edge-TTS, Index-TTS, etc.)
- The system will automatically scan TTS workflows in the `workflows/` folder
- If you know ComfyUI, you can customize TTS workflows

#### Reference Audio (Optional)
- Upload reference audio for voice cloning (supports MP3/WAV/FLAC and other formats)
- For TTS workflows that support voice cloning (e.g., Index-TTS)
- You can preview directly after uploading

#### Preview Function
- Enter test text and click "Preview Voice" to hear the effect
- Supports preview using reference audio


### 🎨 Visual Settings (Middle Column)

#### Image Generation
Determines what style of images AI generates.

**ComfyUI Workflow**  
- Select an image generation workflow from the dropdown menu
- Supports local deployment (selfhost) and cloud (RunningHub) workflows
- Also supports selecting `api/...` direct image model workflows (requires configuring provider credentials in System Configuration first)
- Default uses `image_flux.json`
- If you know ComfyUI, you can place your own workflows in the `workflows/` folder

**Image Dimensions**  
- Set the width and height of generated images (unit: pixels)
- Default 1024x1024, can be adjusted as needed
- Note: Different models have different dimension limitations

**Prompt Prefix**  
- Controls the overall image style (language needs to be English)
- Example: Minimalist black-and-white matchstick figure style illustration, clean lines, simple sketch style
- Click "Preview Style" to test the effect

#### Video Template
Determines the layout and design of the video.

**Template Naming Convention**  
- `static_*.html`: Static templates (no AI-generated media needed, pure text styles)
- `image_*.html`: Image templates (use AI-generated images as background)
- `video_*.html`: Video templates (use AI-generated video as background)

**Usage**  
- Select a template from the dropdown menu, grouped by dimension (portrait/landscape/square)
- Click "Preview Template" to test effects with custom parameters
- If you know HTML, you can create your own templates in the `templates/` folder
- 🔗 [View All Template Previews](https://aidc-ai.github.io/Pixelle-Video/zh/user-guide/templates/#_3)

#### API Video Generation
When selecting templates or extension workflows that support dynamic video, you can use direct API video models to generate clips.

- Supports DashScope Wan / HappyHorse, Kling, Seedance and other video models
- Displays model-aware parameters such as resolution, aspect ratio, duration, watermark, native audio
- Supports network/download retries and prompt neutralization retries after content moderation failures
- In the "Custom Media" workflow, API video clips try to match the narration audio duration and use adjacent clip information for better continuity


### 🎬 Generate Video (Right Column)

#### Generate Button
- After configuring all parameters, click "🎬 Generate Video"
- Real-time progress will be displayed (generating script → generating images → synthesizing voice → composing video)
- Video preview is automatically shown after completion

#### Progress Display
- Shows the current step in real-time
- Example: "Frame 3/5 - Generating Image"

#### Video Preview
- Auto-plays upon completion
- Shows video duration, file size, number of frames, etc.
- Video files are saved in the `output/` folder


### ❓ FAQ

**Q: How long does the first use take?**  
A: Generation time depends on the number of video frames, network conditions, and AI inference speed. It is usually completed within a few minutes.

**Q: What if I'm not satisfied with the video result?**  
A: You can try:
1. Change the LLM model (different models produce different script styles)
2. Adjust the image dimensions and prompt prefix (to change the image style)
3. Switch the TTS workflow or upload reference audio (to change the voice effect)
4. Try different video templates and dimensions

**Q: How much does it cost?**  
A: **This project fully supports free operation!**

- **Completely Free Solution**: LLM using Ollama (local) + ComfyUI local deployment = $0
- **Recommended Solution**: LLM using Qwen (extremely low cost, highly cost-effective) + ComfyUI local deployment
- **Cloud Solution**: LLM using OpenAI + Image using RunningHub (higher cost but no local environment needed)

**Selection Suggestion**: If you have a local GPU, the completely free solution is recommended; otherwise, Qwen is recommended (highly cost-effective).


## 🤝 Referenced Projects

Pixelle-Video's design is inspired by the following excellent open-source projects:

- [Pixelle-MCP](https://github.com/AIDC-AI/Pixelle-MCP) - ComfyUI MCP server that lets AI assistants directly invoke ComfyUI
- [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) - Excellent video generation tool
- [NarratoAI](https://github.com/linyqh/NarratoAI) - Film commentary automation tool
- [MoneyPrinterPlus](https://github.com/ddean2009/MoneyPrinterPlus) - Video creation platform
- [ComfyKit](https://github.com/puke3615/ComfyKit) - ComfyUI workflow wrapper library

Thanks to the open-source spirit of these projects! 🙏


## 💬 Community

Scan the QR code below to join our community for the latest updates and technical support:

| WeChat Group | Discord Community |
| ---- | ---- |
| <img src="resources/wechat.png" alt="WeChat Group" width="250" /> | <img src="resources/discord.png" alt="Discord Community" width="250" /> |


## 📢 Feedback & Support

- 🐛 **Encountered Issues**: Submit an [Issue](https://github.com/AIDC-AI/Pixelle-Video/issues)
- 💡 **Feature Suggestions**: Submit a [Feature Request](https://github.com/AIDC-AI/Pixelle-Video/issues)
- ⭐ **Give a Star**: If this project helps you, feel free to give it a Star for support!


## 📝 License

This project is licensed under the Apache 2.0 License. For details, see the [LICENSE](LICENSE) file.


## 📚 Research Series

| Framework | Paper |
|:---:|---|
| <img src="https://github.com/HITsz-TMG/VideoClaw/blob/main/FilmAgent-pics/framework.png" width="420" alt="FilmAgent framework"/> | **[SIGGRAPH Asia 2024] FilmAgent: Automating Virtual Film Production Through a Multi-Agent Collaborative Framework**<br>*Zhenran Xu, Longyue Wang, Jifang Wang, Zhouyi Li, Senbao Shi, Xue Yang, Yiyu Wang, Baotian Hu, Jun Yu, Min Zhang*<br>[[Paper](https://arxiv.org/pdf/2501.12909)] [[GitHub](https://github.com/HITsz-TMG/VideoClaw/blob/main/FilmAgent)] |
| <img src="https://github.com/HITsz-TMG/Anim-Director/blob/main/Anim-Director/assets/visualeg.png" width="420" alt="Anim-Director result"/> | **[SIGGRAPH Asia 2024] Anim-Director: A Large Multimodal Model Powered Agent for Controllable Animation Video Generation**<br>*Yunxin Li, Haoyuan Shi, Baotian Hu, Longyue Wang, Jiashun Zhu, Jinyi Xu, Zhen Zhao, Min Zhang*<br>[[Paper](https://doi.org/10.1145/3680528.3687688)] [[GitHub](https://github.com/HITsz-TMG/Anim-Director/tree/main/Anim-Director)] |
| <img src="https://github.com/AIDC-AI/ComfyUI-Copilot/blob/main/assets/Framework-v3.png" width="420" alt="Anim-Director result"/> | **[ACL 2025] ComfyUI-Copilot: An Intelligent Assistant for Automated Workflow Development**<br>*Zhenran Xu, Xue Yang, Yiyu Wang, Qingli Hu, Zijiao Wu, Longyue Wang, Weihua Luo, Kaifu Zhang, Baotian Hu, Min Zhang*<br>[[Paper](https://aclanthology.org/2025.acl-demo.61/)] [[GitHub](https://github.com/AIDC-AI/ComfyUI-Copilot)] |
| <img src="https://raw.githubusercontent.com/HITsz-TMG/Anim-Director/main/AniMaker/assets/pipeline.png" width="420" alt="AniMaker pipeline"/> | **[SIGGRAPH Asia 2025] AniMaker: Multi-Agent Animated Storytelling with MCTS-Driven Clip Generation**<br>*Haoyuan Shi, Yunxin Li, Xinyu Chen, Longyue Wang, Baotian Hu, Min Zhang*<br>[[Paper](https://doi.org/10.1145/3757377.3764009)] [[GitHub](https://github.com/HITsz-TMG/Anim-Director/tree/main/AniMaker)] |



## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=AIDC-AI/Pixelle-Video&type=Date)](https://star-history.com/#AIDC-AI/Pixelle-Video&Date)
