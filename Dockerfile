# Stage 1: Build Cuda toolkit
<<<<<<< HEAD
FROM ubuntu:22.04 as cuda-setup


ARG DEBIAN_FRONTEND=noninteractive

# Install necessary libraries including libxml2
RUN apt-get update && \
    apt-get install -y gcc libxml2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY cuda_12.4.0_550.54.14_linux.run .

# Install wget, download cuda-toolkit and run
RUN chmod +x cuda_12.4.0_550.54.14_linux.run && \
    ./cuda_12.4.0_550.54.14_linux.run --silent --toolkit --override

# Second Stage: Copy necessary CUDA directories install flash-attn
FROM ubuntu:22.04 as base-layer

# Copy the CUDA toolkit from the first stage
COPY --from=cuda-setup /usr/local/cuda-12.4 /usr/local/cuda-12.4

# Set environment variables to enable CUDA commands
ENV PATH=/usr/local/cuda-12.4/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64:${LD_LIBRARY_PATH}

# Install Python, pip, and virtualenv
RUN apt-get update && \ 
    apt-get install -y python3 python3-pip python3-venv git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment and install dependencies
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
FROM ubuntu:22.04 as cuda-setup


ARG DEBIAN_FRONTEND=noninteractive

# Install necessary libraries including libxml2
RUN apt-get update && \
    apt-get install -y gcc libxml2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY cuda_12.4.0_550.54.14_linux.run .

# Install wget, download cuda-toolkit and run
RUN chmod +x cuda_12.4.0_550.54.14_linux.run && \
    ./cuda_12.4.0_550.54.14_linux.run --silent --toolkit --override

# Second Stage: Copy necessary CUDA directories install flash-attn
FROM ubuntu:22.04 as base-layer

# Copy the CUDA toolkit from the first stage
COPY --from=cuda-setup /usr/local/cuda-12.4 /usr/local/cuda-12.4

# Set environment variables to enable CUDA commands
ENV PATH=/usr/local/cuda-12.4/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64:${LD_LIBRARY_PATH}

# Install Python, pip, and virtualenv
RUN apt-get update && \ 
    apt-get install -y python3 python3-pip python3-venv git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment and install dependencies
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Llama.cpp requires the ENV variable be set to signal the CUDA build and be built with the CMAKE variables from pip for python use
ENV LLAMA_CUBLAS=1
RUN pip install --no-cache-dir torch packaging wheel && \
    pip install flash-attn && \
RUN pip install --no-cache-dir torch packaging wheel && \
    pip install flash-attn && \
    pip install gradio && \
    CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama_cpp_python==0.2.55 && \
    CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama_cpp_python==0.2.55 && \
=======
FROM drakosfire/cuda-base:latest as base-layer

# Llama.cpp requires the ENV variable be set to signal the CUDA build and be built with the CMAKE variables from pip for python use
ENV LLAMA_CUBLAS=1
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    pip install gradio && \
    CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python && \
>>>>>>> 9a956dd (Polished and launch to Hugging Face)
    pip install pillow && \ 
    pip install diffusers && \
    pip install accelerate && \
    pip install transformers && \
<<<<<<< HEAD
    pip install peft && \
    pip install pip install PyGithub


FROM ubuntu:22.04 as final-layer

COPY --from=base-layer /usr/local/cuda-12.4 /usr/local/cuda-12.4
COPY --from=base-layer /venv /venv

ENV PATH=/usr/local/cuda-12.4/bin:/venv/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64:${LD_LIBRARY_PATH}
ENV LLAMA_CPP_LIB=/venv/lib/python3.10/site-packages/llama_cpp/libllama.so
ENV VIRTUAL_ENV=/venv

# Install Python and create a user
RUN apt-get update && apt-get install -y python3 python3-venv && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    useradd -m -u 1000 user
    

# Install Python and create a user
RUN apt-get update && apt-get install -y python3 python3-venv && apt-get clean && rm -rf /var/lib/apt/lists/* && \
    useradd -m -u 1000 user
    
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Set working directory and user
COPY . /home/user/app
# Set working directory and user
COPY . /home/user/app
WORKDIR /home/user/app
RUN chown -R user:user /home/user/app/ && \
    mkdir -p /home/user/app/output && \
    chown -R user:user /home/user/app/image_temp && \
    chown -R user:user /home/user/app/output 
=======
    pip install peft

FROM base-layer as final-layer

RUN useradd -m -u 1000 user 
   
    # mkdir -p /home/user/.cache && \  
    # chmod 777 /home/user/.cache && \  
    # chown -R user:user /home/user/app/ 
# Set environment variables for copied builds of cuda and flash-attn in /venv


ENV PATH=/usr/local/cuda-12.4/bin:/venv/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda-12.4/lib64:${LD_LIBRARY_PATH}

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Set working directory and user
WORKDIR /home/user/app
>>>>>>> 9a956dd (Polished and launch to Hugging Face)

USER user
    
# Set the entrypoint
EXPOSE 8000

ENTRYPOINT ["python", "main.py"]

<lora:CyborgsXL:..3> <lora:RBTS_STYLE:.2> <lora:ral-fluff:1.3> <lora:zhibi:.5>