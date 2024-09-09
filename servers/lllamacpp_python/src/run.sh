#!/bin/bash
if [ ${CONFIG_PATH} ] || [[ ${MODEL_PATH} && ${CONFIG_PATH} ]]; then
    python -m llama_cpp.server --config_file ${CONFIG_PATH}
    exit 0
fi

if [ "${MODEL_HF_PRETRAINED_MODEL}" == "None" ]; then
    MODEL_HF_PRETRAINED_MODEL=""
fi

if [ ${MODEL_PATH} ]; then
    python -m llama_cpp.server \
        --model ${MODEL_PATH} \
        --host ${HOST:=0.0.0.0} \
        --port ${PORT:=8001} \
        --n_gpu_layers ${GPU_LAYERS:=0} \
        --clip_model_path ${CLIP_MODEL_PATH:=None} \
        --chat_format ${MODEL_CHAT_FORMAT:=llama-2} \
        ${PRETRAINED_MODEL_PATH:=} \
        ${MODEL_HF_PRETRAINED_MODEL:+--hf_pretrained_model_name_or_path ${MODEL_HF_PRETRAINED_MODEL}} \
        --interrupt_requests ${INTERRUPT_REQUESTS:=False}
    exit 0
fi

echo "Please set either a CONFIG_PATH or a MODEL_PATH"
exit 1

