import os, sys, json, re, shutil, subprocess, tempfile, traceback
import threading, time, smtplib, imaplib, email as email_lib
import hashlib, base64, platform, glob, zipfile, tarfile
from npmai import Ollama, Memory
from pathlib import Path
from datetime import datetime
from typing import Callable, Optional
from abc import ABC, abstractmethod
from .npmai_agents import AgentBrain
from .core import CredStore, Workspace, ToolResult, LLMBackend, Ollama_Local, OpenAIBackend, AnthropicBackend, GeminiBackend, GroqBackend, MistralBackend, CohereBackend, AzureOpenAIBackend, BedrockBackend, HuggingFaceBackend, LlamaCppBackend
import typer
import json

app = typer.Typer()


@app.command()
def save_credentials(name:str,data:str):
  data_parsed = json.loads(data)
  cred = CredStore()
  saved = cred.save(name=name,data=data_parsed)

@app.command()
def load_credentials(name:str):
  cred = CredStore()
  load = cred.load(name=name)
  print(load)

@app.command()
def all_credentials():
  cred = CredStore()
  all_keys = cred.all_keys()
  print(all_keys)

@app.command()
def workspace_scan():
  workspace = Workspace()
  scan = workspace.scan()
  print(scan)

@app.command()
def workspace_update(key, value):
  workspace = Workspace()
  update = workspace.update_profile(key=key,value=value)

@app.command()
def workspace_context():
  workspace = Workspace()
  ctx_summary = workspace.context_summary()
  print(ctx_summary)

def build_backend(provider: str, model: str):
        p = provider.lower()
        if p == "npmai":       return Ollama(model=model)
        elif p == "local":     return Ollama_Local(model=model)
        elif p == "openai":    return OpenAIBackend(model=model, api_key=CredStore.load("openai")["api_key"])
        elif p == "groq":      return GroqBackend(model=model, api_key=CredStore.load("groq")["api_key"])
        elif p == "anthropic": return AnthropicBackend(model=model, api_key=CredStore.load("anthropic")["api_key"])
        elif p == "gemini":    return GeminiBackend(model=model, api_key=CredStore.load("gemini")["api_key"])
        elif p == "mistral":   return MistralBackend(model=model, api_key=CredStore.load("mistral")["api_key"])
        elif p == "cohere":    return CohereBackend(model=model, api_key=CredStore.load("cohere")["api_key"])
        elif p == "azure":     return AzureOpenAIBackend(model=model, **CredStore.load("azure"))
        elif p == "bedrock":   return BedrockBackend(model=model, **CredStore.load("bedrock"))
        elif p == "hf":        return HuggingFaceBackend(model=model, api_key=CredStore.load("hf")["api_key"])
        elif p == "llamacpp":  return LlamaCppBackend(model=model)
        else: raise typer.BadParameter(f"Unknown provider '{provider}'. Use: npmai, local, openai, groq, anthropic, gemini, mistral, cohere, azure, bedrock, hf, llamacpp")
   

@app.command()
def run(
    task:str,
    planner_model: str = "llama3.2:3b",
    planner_provider: str = "npmai",
    tool_manager_provider: str = "npmai",
    tool_manager_model: str ="granite3.3:2b",
    coder_model: str = "codellama:7b-instruct", 
    coder_provider: str = "npmai",
    auditor_model: str = "qwen2.5-coder:7b",
    auditor_provider: str = "npmai",
    verifier_model: str = "llama3.2:3b",
    verifier_provider: str = "npmai",
    chatter_model: str = "granite3.3:2b",
    chatter_provider: str = "npmai",
):

  agent = AgentBrain(
        planner  = build_backend(planner_provider,  planner_model),
        tool_manager = build_backend(tool_manager_provider, tool_manager_model),
        coder    = build_backend(coder_provider,    coder_model),
        auditor  = build_backend(auditor_provider,  auditor_model),
        verifier = build_backend(verifier_provider, verifier_model),
        chatter  = build_backend(chatter_provider,  chatter_model),
    )
    
  task_result = agent.run_task(task=task)
  return task_result

@app.command()
def chat(
    user_msg:str,
    chatter_model: str = "granite3.3:2b",
    chatter_provider: str = "npmai",
):
  agent = AgentBrain(
        chatter  = build_backend(chatter_provider,  chatter_model),
  )
    
  chat_resp = agent.chat(user_msg=user_msg)
  print(chat_resp)
  return chat_resp

def main():
    app()
if __name__ == "__main__":
    main()
