"""
sign_animation — Text/Speech-to-Sign communication module.

This package implements the Bidirectional Communication Module with
Intelligent Sign Animation for the Smart SLSL Research System.

Pipeline stages:
    text_processing    → normalise user input
    gloss_generation   → map tokens to sign IDs
    gesture_selection  → load and query the sign database
    video_renderer     → resolve video URLs for the frontend
    animation_service  → orchestrate the full pipeline
    animation_renderer → stub interface for future 3D animation
    speech_processing  → speech-to-text helpers
    evaluate           → pipeline coverage evaluation
"""
