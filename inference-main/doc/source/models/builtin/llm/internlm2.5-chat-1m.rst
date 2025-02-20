.. _models_llm_internlm2.5-chat-1m:

========================================
internlm2.5-chat-1m
========================================

- **Context Length:** 262144
- **Model Name:** internlm2.5-chat-1m
- **Languages:** en, zh
- **Abilities:** chat
- **Description:** InternLM2.5 series of the InternLM model supports 1M long-context

Specifications
^^^^^^^^^^^^^^


Model Spec 1 (pytorch, 7 Billion)
++++++++++++++++++++++++++++++++++++++++

- **Model Format:** pytorch
- **Model Size (in billions):** 7
- **Quantizations:** none
- **Engines**: vLLM, Transformers
- **Model ID:** internlm/internlm2_5-7b-chat-1m
- **Model Hubs**:  `Hugging Face <https://huggingface.co/internlm/internlm2_5-7b-chat-1m>`__, `ModelScope <https://modelscope.cn/models/Shanghai_AI_Laboratory/internlm2_5-7b-chat-1m>`__

Execute the following command to launch the model, remember to replace ``${quantization}`` with your
chosen quantization method from the options listed above::

   xinference launch --model-engine ${engine} --model-name internlm2.5-chat-1m --size-in-billions 7 --model-format pytorch --quantization ${quantization}


Model Spec 2 (gptq, 7 Billion)
++++++++++++++++++++++++++++++++++++++++

- **Model Format:** gptq
- **Model Size (in billions):** 7
- **Quantizations:** Int4
- **Engines**: vLLM, Transformers
- **Model ID:** ModelCloud/internlm-2.5-7b-chat-1m-gptq-4bit
- **Model Hubs**:  `Hugging Face <https://huggingface.co/ModelCloud/internlm-2.5-7b-chat-1m-gptq-4bit>`__

Execute the following command to launch the model, remember to replace ``${quantization}`` with your
chosen quantization method from the options listed above::

   xinference launch --model-engine ${engine} --model-name internlm2.5-chat-1m --size-in-billions 7 --model-format gptq --quantization ${quantization}


Model Spec 3 (ggufv2, 7 Billion)
++++++++++++++++++++++++++++++++++++++++

- **Model Format:** ggufv2
- **Model Size (in billions):** 7
- **Quantizations:** q2_k, q3_k_m, q4_0, q4_k_m, q5_0, q5_k_m, q6_k, q8_0, fp16
- **Engines**: llama.cpp
- **Model ID:** internlm/internlm2_5-7b-chat-1m-gguf
- **Model Hubs**:  `Hugging Face <https://huggingface.co/internlm/internlm2_5-7b-chat-1m-gguf>`__

Execute the following command to launch the model, remember to replace ``${quantization}`` with your
chosen quantization method from the options listed above::

   xinference launch --model-engine ${engine} --model-name internlm2.5-chat-1m --size-in-billions 7 --model-format ggufv2 --quantization ${quantization}

