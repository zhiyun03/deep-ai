# Copyright 2022-2023 XProbe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import random
from typing import TYPE_CHECKING, List, Tuple

from transformers import AutoTokenizer, PreTrainedTokenizerFast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase

# A fast LLaMA tokenizer with the pre-processed `tokenizer.json` file.
_FAST_LLAMA_TOKENIZER = "hf-internal-testing/llama-tokenizer"


def get_tokenizer(
    tokenizer_name: str,
    *args,
    tokenizer_mode: str = "auto",
    trust_remote_code: bool = False,
    **kwargs,
) -> "PreTrainedTokenizerBase":
    """Gets a tokenizer for the given model name via Huggingface."""
    if tokenizer_mode == "slow":
        if kwargs.get("use_fast", False):
            raise ValueError("Cannot use the fast tokenizer in slow tokenizer mode.")
        kwargs["use_fast"] = False

    if (
        "llama" in tokenizer_name.lower()
        and kwargs.get("use_fast", True)
        and tokenizer_name != _FAST_LLAMA_TOKENIZER
    ):
        logger.info(
            "For some LLaMA-based models, initializing the fast tokenizer may "
            "take a long time. To eliminate the initialization time, consider "
            f"using '{_FAST_LLAMA_TOKENIZER}' instead of the original "
            "tokenizer."
        )
    try:
        tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name, *args, trust_remote_code=trust_remote_code, **kwargs
        )
    except TypeError as e:
        # The LLaMA tokenizer causes a protobuf error in some environments.
        err_msg = (
            "Failed to load the tokenizer. If you are using a LLaMA-based "
            f"model, use '{_FAST_LLAMA_TOKENIZER}' instead of the original "
            "tokenizer."
        )
        raise RuntimeError(err_msg) from e
    except ValueError as e:
        # If the error pertains to the tokenizer class not existing or not
        # currently being imported, suggest using the --trust-remote-code flag.
        if not trust_remote_code and (
            "does not exist or is not currently imported." in str(e)
            or "requires you to execute the tokenizer file" in str(e)
        ):
            err_msg = (
                "Failed to load the tokenizer. If the tokenizer is a custom "
                "tokenizer not yet available in the HuggingFace transformers "
                "library, consider setting `trust_remote_code=True` in LLM "
                "or using the `--trust-remote-code` flag in the CLI."
            )
            raise RuntimeError(err_msg) from e
        else:
            raise e

    if not isinstance(tokenizer, PreTrainedTokenizerFast):
        logger.warning(
            "Using a slow tokenizer. This might cause a significant "
            "slowdown. Consider using a fast tokenizer instead."
        )
    return tokenizer


def sample_requests(
    dataset_path: str,
    num_requests: int,
    tokenizer: "PreTrainedTokenizerBase",
    prompt_len_limit: int = 1024,
) -> List[Tuple[str, int, int]]:
    # Load the dataset.
    with open(dataset_path) as f:
        dataset = json.load(f)
    # Filter out the conversations with less than 2 turns.
    dataset = [data for data in dataset if len(data["conversations"]) >= 2]
    # Only keep the first two turns of each conversation.
    dataset = [
        (data["conversations"][0]["value"], data["conversations"][1]["value"])
        for data in dataset
    ]

    # Tokenize the prompts and completions.
    prompts = [prompt for prompt, _ in dataset]
    prompt_token_ids = tokenizer(prompts).input_ids
    completions = [completion for _, completion in dataset]
    completion_token_ids = tokenizer(completions).input_ids
    tokenized_dataset = []
    for i in range(len(dataset)):
        output_len = len(completion_token_ids[i])
        tokenized_dataset.append((prompts[i], prompt_token_ids[i], output_len))

    # Filter out too long sequences.
    filtered_dataset: List[Tuple[str, int, int]] = []
    for prompt, prompt_token_ids, output_len in tokenized_dataset:
        prompt_len = len(prompt_token_ids)
        if prompt_len < 4 or output_len < 4:
            # Prune too short sequences.
            # This is because TGI causes errors when the input or output length
            # is too short.
            continue
        if (
            prompt_len > prompt_len_limit
            or prompt_len + output_len > prompt_len_limit * 2
        ):
            # Prune too long sequences.
            continue
        filtered_dataset.append((prompt, prompt_len, output_len))

    # Sample the requests.
    sampled_requests = random.sample(filtered_dataset, num_requests)
    return sampled_requests


def generate_sorting_prompts(
    num_prompts: int,
    context_length: int,
    prompt_len_limit: int,
    tokenizer: "PreTrainedTokenizerBase",
) -> List[Tuple[str, int, int]]:
    prompts = []
    for i in range(0, num_prompts):
        random_nums = []
        _prompt_len = 0
        while True:
            r_str = "%s" % random.randint(0, 99)
            r_len = len(r_str) + 1
            if r_len + _prompt_len > prompt_len_limit:
                break
            random_nums.append(r_str)
            _prompt_len += r_len
        prompt = "Sort the numbers:" + ",".join(random_nums)
        prompts.append(prompt)
    prompt_token_ids = tokenizer(prompts).input_ids
    dataset = []
    for i in range(0, len(prompts)):
        prompt_len = len(prompt_token_ids[i])
        dataset.append((prompts[i], prompt_len, context_length - prompt_len))
    return dataset
