# Celer Sight AI

<img width="390" alt="celer_sight_splash" src="https://github.com/user-attachments/assets/0f103da2-b16a-42ed-a424-7be803588a89">


**Celer Sight AI** is a high-throughput imaging analysis solution that is easy to use and improves with use for everyone. Celer Sight AI is ideal for anyone looking to analyse their image data quickly without needed to dive deep into coding.

---

## 🚀 Highlights

- 🚀 **High-Throughput Image Analysis**: Streamlined workflows for fluorescent image analysis with up to 95% faster processing.
- ⚡️ **Self-Improving Models**: A community-powered hub of AI models that improve with use and constantly expand.
- 🛠️ **Reproducable Experiments**: Save and load states of your experiements as .bmics files.
- 🖥️ **Multi-Platform Support**: For Mac OS and Windows OS.
- 🤓 **Beginner-Friendly**: No need for coding experience, AI segmentation models are pretrained and analysis is performed automatically.
- 💾 **Memory efficient**: Large tifs are loaded directly from disk and cached versions of them allow for fast scrabing through
- 🔬 **Whole Slide Image Support**: Pyramidal images are supported for segmentation
- 🌐 **Open Source Model Library**: Version of our segmentation models will be made available to HuggingFace for anyone to download and use.
- 🗂️ **Easy Image Imports**: Drag and Drop multiple directories as treatments. 
---

## See it in action:

### 1) Sample Experiment
![sample_worms](https://github.com/user-attachments/assets/86b64040-7dd7-4560-b06b-e237ac888cdd)

### 2) Easy importing
![import patterns](https://github.com/user-attachments/assets/1c421c9c-51aa-4d36-a180-a797eeae67b2)

### 3) Easily create new class / models && improve them
![Create new model](https://github.com/user-attachments/assets/7230a2eb-afad-4004-88dd-f5fb371070b3)

## Why Celer Sight?
Even though there are plenty of image analysis software out there, they often require users to dive deeper and spend time learning how to use them or even learn how to code. On top of that there is also the need for a model catalogue that has plenty and well generalizing models. Celer Sight attempts to solve both of those problems by providing one of the simplest interfaces. On the backend, we take care of model training and deployment. Models are created by the community, improved by the community and used by the community


## 🔧 How to install
For normal use, just download the compiled application from www.biomarkerimaging.com/download


## 🔧 Installation for development

1. Clone the repository:

   `git clone https://github.com/BioMarkerImaging/SelerSightAI`
   `cd celer-sight-ai`
   
2. Create and activate a virtual environment:

   **Windows**:

      `
      python -m venv .venv
      .venv\Scripts\activate
      `

   **macOS/Linux**:

      `
      python -m venv .venv
      source .venv/bin/activate
      `

3. Install dependencies:

   `
   pip install -r requirements.txt
   pip install -v -e .
   `

## Model training / inference is expensive, how can this be free?
Initially, all users will have access to cloud compute, however, within the next year this will change. For free users Celer Sight will download version of the requested models and they will run on the users laptop. This way of serving models allow us to handle ai model inference for free! If you still need cloud inference though, there will be a paid option available for those who can support it.

