#!/bin/bash

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the Llama model
"$DIR/Llama-3.2-1B-Instruct.Q6_K.llamafile" --server
