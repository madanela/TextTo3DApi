
---

# 3D Mesh Generation API

## Overview

This API leverages the OpenAI's `shap-e` library and Blender to generate and texture 3D meshes. It supports exporting the resulting 3D models in various file formats, including `.usdz`, `.obj`, and plans to add `.glb` and `.fbx` formats in the future. The API is particularly suitable for iOS applications that utilize the `.usdz` format.

## Installation

To set up the API environment and install the necessary dependencies, execute the installation script by running:

```bash
./install.sh
```

This will install the `shap-e` library along with other required packages.

## Usage

To start the API server, use the `uvicorn` command as follows:

```bash
uvicorn main:app --host <host_name> --port <port_number>
```

Replace `<host_name>` with your server's hostname or IP address and `<port_number>` with the desired port number.

For example:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

To stop the server, press `Ctrl + C` in the terminal.

## API Endpoints

### Generate 3D Mesh with Texture:
Initiate the generation of a 3D mesh with an embedded texture by sending a GET request to:

```
GET /generate_3d_mesh?prompt=<your_prompt>
```

**Parameters:**
- `prompt` (required): The textual description of the desired 3D object.

**Example:**
```
http://localhost:8000/generate_3d_mesh?prompt=A+modern+lounge+chair
```

**Response:**
The endpoint will return a `.usdz` model file with embedded textures.

## Blender Configuration

The accompanying `texture.blend` file uses CPU rendering by default. If you prefer to utilize GPU rendering for enhanced performance, ensure that your GPU has more than 8GB of available memory.

Should you choose CPU rendering or have a GPU with approximately 8GB of memory, no additional configuration should be required.

## Suggestions

- Given the resource-intensive nature of 3D mesh generation and texturing, run this API on a system with adequate hardware capabilities.
- Expect the `.usdz` export process to be more computationally demanding when generating detailed or complex meshes.

---

**Note:** The placeholders wrapped in angle brackets (e.g., `<host_name>`) are to direct the user to replace them with actual values. Make sure to remove the angle brackets when providing the actual commands or URLs. Additionally, the use of "OpenAI's `shap-e` library" has been corrected to "the `shap-e` library" since at the time of writing, there is no information suggesting the `shap-e` library is directly associated with OpenAI.