# Stage 1: Build Cuda toolkit
FROM drakosfire/cuda-base:latest as base-layer

# Llama.cpp requires the ENV variable be set to signal the CUDA build and be built with the CMAKE variables from pip for python use
ENV LLAMA_CUBLAS=1
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    pip install gradio && \
    CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python && \
    pip install pillow && \ 
    pip install diffusers && \
    pip install accelerate && \
    pip install transformers && \
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

USER user
    
# Set the entrypoint
EXPOSE 8000

ENTRYPOINT ["python", "main.py"]