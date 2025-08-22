# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Celer Sight AI is a high-throughput microscopy image analysis application that leverages AI for automated segmentation. It's a desktop application built with PyQt6 for scientific image analysis, particularly focused on fluorescent microscopy images.

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -v -e .
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_specific.py

# Run tests with markers
pytest -m "not online"  # Skip online tests
pytest -m "not long"     # Skip long-running tests
```

### Code Quality
```bash
# Format and lint with ruff
ruff format .
ruff check .
```

### Running the Application
```bash
# Run the main application
python celer_sight_ai/celer_sight_main.py

# Or after installing with pip -e
python -m celer_sight_ai
```

## Architecture

### Core Modules

- **celer_sight_ai/celer_sight_main.py**: Entry point and main application initialization
- **celer_sight_ai/gui/**: PyQt6-based GUI components
  - `custom_widgets/viewer/`: Image viewer and annotation tools
  - `designer_widgets/`: UI files and generated Python UI code
- **celer_sight_ai/io/**: Image I/O handlers
  - `image_reader.py`: Handles various image formats including TIF, VSI, NDPI
  - `bioformats_reader.py`: BioFormats integration for specialized formats
- **celer_sight_ai/core/**: Core processing logic
  - `ML_tools.py`: Machine learning inference and model management
  - `magic_box_tools.py`: Advanced segmentation algorithms
  - `Workers.py`: Async task handling
- **celer_sight_ai/inference_handler.py**: ML model inference coordination

### Key Dependencies

- **PyQt6**: GUI framework
- **opencv-python**: Image processing
- **scikit-image**: Advanced image analysis
- **torch/torchvision**: Deep learning models
- **onnxruntime**: Optimized inference
- **bioio/aicsimageio**: Multi-format image I/O
- **pyinstaller**: Application bundling

### Data Flow

1. Images loaded via `io/image_reader.py` supporting multiple formats
2. Viewer displays images through `gui/custom_widgets/viewer/`
3. Annotations handled by scene components (`PolygonAnnotation`, `BitMapAnnotation`)
4. ML inference through `inference_handler.py` using local or cloud models
5. Results saved as `.bmics` session files

## Key Features to Understand

- **Multi-format Support**: Handles standard formats (PNG, JPEG, TIF) plus specialized microscopy formats (VSI, NDPI, OME-TIFF)
- **Pyramidal Images**: Supports whole slide imaging with tiling and lazy loading
- **Annotation System**: Polygon and bitmap annotations with category management
- **Model Hub**: Community-driven models stored locally and on HuggingFace
- **Session Management**: Complete experiment state saved/loaded via `.bmics` files

## Testing Approach

Tests are in `tests/` with fixtures in `tests/fixtures/`. Key test categories:
- `base_image_testcase.py`: Base class for image-related tests
- `test_image_import.py`: Image format compatibility
- `test_inference.py`: ML model testing
- GUI tests using `pytest-qt`

## Platform Considerations

- Cross-platform (Windows, macOS, Linux)
- Platform-specific libraries in `extra_libs/` (VIPS, OpenSlide)
- PyInstaller specs for building executables
- Environment variable `CELER_SIGHT_AI_HOME` sets application root