# Stringo 🎸

> Upload any MP3 — get guitar tabs instantly.
> No chords. No approximations. Real tabs with string and fret numbers.

## What this is
An audio-to-tabs engine that analyzes any audio file and
generates playable guitar tablature. Built on Spotify's
basic-pitch model for note detection, with a custom
fret-mapping algorithm on top.

## How it works
MP3 → basic-pitch detects notes → algorithm maps to
guitar fretboard → tabs displayed in browser

## Stack
- Python 3.11
- basic-pitch (Spotify) — note detection
- FastAPI — backend API
- HTML/CSS/JS — frontend interface

## Run locally
pip install basic-pitch fastapi uvicorn python-multipart
uvicorn main:app --reload

## Results
*Coming soon*
