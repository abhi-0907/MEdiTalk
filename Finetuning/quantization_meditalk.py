# Install llama.cpp
!git clone https://github.com/ggerganov/llama.cpp
!cd llama.cpp && git pull && make clean && LLAMA_CUBLAS=1 make
%pip install -r llama.cpp/requirements.txt

# Variables
MODEL_ID = "abhiram973/MediTalk2"
QUANTIZATION_METHOD = "q4_1"

# Constants
MODEL_NAME = MODEL_ID.split('/')[-1]

# Download model
!git lfs install
!git clone https://huggingface.co/{MODEL_ID}

# Convert to fp16
!mkdir ./quantized_model/
!python llama.cpp/convert.py ./MediTalk2/ --outtype f16 --outfile ./FP16/Meditalk_FP16.gguf


# Quantize the model for each method in the QUANTIZATION_METHODS list
qtype = f"{MODEL_NAME}/{MODEL_NAME.lower()}.{QUANTIZATION_METHOD.upper()}.gguf"
!./llama.cpp/quantize {fp16filepath} {quantizedmodelname} {method}