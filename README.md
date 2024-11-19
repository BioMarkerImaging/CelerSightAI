# Celer Sight AI

<p align="center" style="margin: -30px 0;">
  <img width="390" alt="celer_sight_splash" src="https://github.com/user-attachments/assets/0f103da2-b16a-42ed-a424-7be803588a89">
</p>


Celer Sight AI is a free high-throughput imaging analysis solution that leverages AI to simplify microscopy image analysis through a community powered AI model segmentation catalogue that is constantly improving. Perfect for researchers and professionals who need powerful image analysis without coding expertise.

---

## 🚀 Key Features

- 🚀 **High-Throughput Analysis**: Process fluorescent images up to 95% faster than traditional methods
- ⚡️ **Adaptive AI Models**: Community-driven model hub that continuously improves through collective usage
- 🛠️ **Experiment Reproducibility**: Save and load sessions with `.bmics` files
- 🖥️ **Cross-Platform**: Fully supported on macOS and Windows
- 🤓 **User-Friendly Interface**: Pre-trained AI models and automated analysis - no coding required
- 💾 **Optimized Performance**: Efficient handling of large TIF files with smart disk caching
- 🔬 **WSI Compatible**: Full support for pyramidal whole slide images
- 🌐 **Open Source Models**: All models available through HuggingFace for community use
- 🗂️ **Intuitive Data Import**: Simple drag-and-drop interface for batch processing

---

## Why Choose Celer Sight?
Traditional image analysis tools often require extensive training or programming knowledge. Celer Sight revolutionizes this workflow by providing:
- Intuitive interface for immediate productivity
- Community-driven model development
- Automated analysis pipelines


### Quick Start
#### App download
1) Download the latest release from our [official website](https://www.biomarkerimaging.com/download)
2) No account? No worries! Just select "Offline" in the log in screen and you can use the app without needing an account.
#### Registration (For access to our models we require registration to avoid abuse).
1) Sign up for the [waitlist](https://www.biomarkerimaging.com/waitlist) . Please specify if you will be able to provide us with annotated data or are interested in buying a paid version in the future.
2) Once you are accepted from the waitlist, you can [register](https://www.biomarkerimaging.com/register)
3) Once registered, you will have access to all of the community models when you sign in the app.


## See it in action:

### 1) Sample Experiment
![sample_worms](https://github.com/user-attachments/assets/86b64040-7dd7-4560-b06b-e237ac888cdd)

### 2) Easy importing
![import patterns](https://github.com/user-attachments/assets/1c421c9c-51aa-4d36-a180-a797eeae67b2)

### 3) Easily create new class / models && improve them
![Create new model](https://github.com/user-attachments/assets/7230a2eb-afad-4004-88dd-f5fb371070b3)

### 3) High resolution / pyramidal image support
![Untitled](https://github.com/user-attachments/assets/78e72a4a-c659-4b4c-a2f8-99dc94f92724)




## 🔧 Installation for development

1. Clone the repository:

   `git clone https://github.com/BioMarkerImaging/SelerSightAI`

   `cd celer-sight-ai`
   
2. Create and activate a virtual environment:

   **Windows**:

      `
      python -m venv .venv`

      `.venv\Scripts\activate`

   **macOS/Linux**:

      `python -m venv .venv`

      `source .venv/bin/activate`

3. Install dependencies:

   `
   pip install -r requirements.txt
   pip install -v -e .
   `

## Model training / inference is expensive, how can this be free?
Initially, all users will have access to cloud compute, however, within the next year this will change. For free users Celer Sight will download version of the requested models and they will run on the users laptop. This way of serving models allow us to handle ai model inference for free! If you still need cloud inference though, there will be a paid option available for those who can support it.

## 💝 Support Celer Sight

### Contributing
We welcome contributions from the community! Here are some ways you can help:
- Submit bug reports and feature requests through GitHub Issues
- Contribute code improvements via Pull Requests
- Share annotated datasets to help improve our models through the app or by email
- Help document and improve our wiki

### Support Our Work
If you find Celer Sight useful, consider supporting its development:
- ☕️ Buy us a coffee on [Ko-fi](https://ko-fi.com/celersight)
- 💖 Become a patron on [Patreon](https://www.patreon.com/c/celersightai/membership)
- 🌟 Star us on GitHub

Your support helps us maintain and improve Celer Sight for everyone!

## License

Celer Sight AI is available under two licensing options:

### 1. Academic/Research License
- Free for academic and research use under Creative Commons Attribution-NonCommercial 4.0 International License
- Allows sharing and adaptation of the material for non-commercial purposes
- Requires appropriate attribution
- See [LICENSE](LICENSE) file for full terms

### 2. Commercial License
- Required for any commercial or non-academic use
- Includes private model / data options and cloud inference.
- Contact us for pricing and terms:
  - Email: [manoschaniotakis@biomarkerimaging.com](mailto:manoschaniotakis@biomarkerimaging.com)
  - Email: [manos.chaniotakis.n@gmail.com](mailto:manos.chaniotakis.n@gmail.com)

Note: The software includes third-party components under various open-source licenses (LGPL, BSD) - see the `extra_libs` directory for individual component licenses.


