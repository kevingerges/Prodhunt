#!/bin/bash

# Variables
model_name="llama3:8b"
custom_model_name="llama3"

# Get the base model
ollama pull $model_name

# Create the model file
ollama create $custom_model_name -f ./Llama3Modelfile