#!/usr/bin/env python3
"""
Joi Advanced Voice System
Provides multiple TTS options for more natural-sounding voice
"""

import os
import base64
from pathlib import Path
from typing import Dict, Any, Optional
import tempfile

# OpenAI TTS (if available)
try:
    from openai import OpenAI
    HAVE_OPENAI = True
except ImportError:
    HAVE_OPENAI = False

# ElevenLabs (if available)
try:
    import elevenlabs
    HAVE_ELEVENLABS = True
except ImportError:
    HAVE_ELEVENLABS = False

VOICE_CACHE_DIR = Path(__file__).parent / "assets" / "voice_cache"
VOICE_CACHE_DIR.mkdir(parents=True, exist_ok=True)

class JoiVoiceEngine:
    """Advanced voice synthesis with multiple TTS engines"""
    
    def __init__(self, openai_key: Optional[str] = None, elevenlabs_key: Optional[str] = None):
        self.openai_key = openai_key or os.getenv("OPENAI_API_KEY")
        self.elevenlabs_key = elevenlabs_key or os.getenv("ELEVENLABS_API_KEY")
        
        self.openai_client = None
        if HAVE_OPENAI and self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
        
        self.current_engine = "browser"  # Default to browser-based TTS
        self.current_voice = "alloy"  # Default OpenAI voice
    
    def set_engine(self, engine: str) -> Dict[str, Any]:
        """
        Set the TTS engine
        
        Args:
            engine: 'browser', 'openai', or 'elevenlabs'
        
        Returns:
            Status dict
        """
        if engine == "openai" and not self.openai_client:
            return {
                "ok": False,
                "error": "OpenAI TTS not available. Check API key."
            }
        
        if engine == "elevenlabs" and not (HAVE_ELEVENLABS and self.elevenlabs_key):
            return {
                "ok": False,
                "error": "ElevenLabs not available. Install with: pip install elevenlabs"
            }
        
        self.current_engine = engine
        return {
            "ok": True,
            "engine": engine
        }
    
    def generate_speech_openai(self, text: str, voice: str = "nova") -> Dict[str, Any]:
        """
        Generate speech using OpenAI TTS API
        
        OpenAI voices: alloy, echo, fable, onyx, nova, shimmer
        'nova' and 'shimmer' are female voices
        
        Args:
            text: Text to convert to speech
            voice: Voice name (nova is warm and expressive, shimmer is refined)
        
        Returns:
            Dict with audio data or error
        """
        if not self.openai_client:
            return {
                "ok": False,
                "error": "OpenAI client not initialized"
            }
        
        try:
            response = self.openai_client.audio.speech.create(
                model="tts-1-hd",  # High quality model
                voice=voice,
                input=text,
                speed=0.95  # Slightly slower for clarity
            )
            
            # Save to temporary file
            audio_file = VOICE_CACHE_DIR / f"tts_{hash(text)}.mp3"
            response.stream_to_file(str(audio_file))
            
            # Read and encode as base64
            with open(audio_file, 'rb') as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            
            return {
                "ok": True,
                "audio_data": f"data:audio/mpeg;base64,{audio_data}",
                "engine": "openai",
                "voice": voice
            }
        
        except Exception as e:
            return {
                "ok": False,
                "error": f"OpenAI TTS error: {str(e)}"
            }
    
    def generate_speech_elevenlabs(self, text: str, voice_id: str = None) -> Dict[str, Any]:
        """
        Generate speech using ElevenLabs API
        
        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID
        
        Returns:
            Dict with audio data or error
        """
        if not HAVE_ELEVENLABS or not self.elevenlabs_key:
            return {
                "ok": False,
                "error": "ElevenLabs not configured"
            }
        
        try:
            # Set API key
            elevenlabs.set_api_key(self.elevenlabs_key)
            
            # Use default voice if none specified
            if not voice_id:
                # Rachel - a calm, natural female voice
                voice_id = "21m00Tcm4TlvDq8ikWAM"
            
            # Generate audio
            audio = elevenlabs.generate(
                text=text,
                voice=voice_id,
                model="eleven_multilingual_v2"
            )
            
            # Save to file
            audio_file = VOICE_CACHE_DIR / f"tts_{hash(text)}.mp3"
            elevenlabs.save(audio, str(audio_file))
            
            # Read and encode as base64
            with open(audio_file, 'rb') as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            
            return {
                "ok": True,
                "audio_data": f"data:audio/mpeg;base64,{audio_data}",
                "engine": "elevenlabs",
                "voice_id": voice_id
            }
        
        except Exception as e:
            return {
                "ok": False,
                "error": f"ElevenLabs error: {str(e)}"
            }
    
    def generate_speech(self, text: str) -> Dict[str, Any]:
        """
        Generate speech using the current engine
        
        Args:
            text: Text to convert to speech
        
        Returns:
            Dict with audio data or instructions for browser TTS
        """
        if self.current_engine == "openai":
            return self.generate_speech_openai(text, self.current_voice)
        
        elif self.current_engine == "elevenlabs":
            return self.generate_speech_elevenlabs(text)
        
        else:  # browser
            return {
                "ok": True,
                "engine": "browser",
                "text": text,
                "instructions": "Use browser's Speech Synthesis API"
            }

# Enhanced JavaScript for voice handling
VOICE_JS = """
// Enhanced Voice System for Joi

class JoiVoice {
    constructor() {
        this.engine = 'browser'; // 'browser', 'openai', or 'elevenlabs'
        this.browserVoice = null;
        this.isSpeaking = false;
        
        // Load saved preferences
        this.engine = localStorage.getItem('joi-voice-engine') || 'browser';
        this.loadBrowserVoices();
    }
    
    loadBrowserVoices() {
        const voices = window.speechSynthesis.getVoices();
        
        // Try to find a good female voice
        const preferredVoices = [
            'Microsoft Zira',
            'Google UK English Female',
            'Samantha',
            'Victoria',
            'Karen',
            'Moira',
            'Fiona'
        ];
        
        for (const preferred of preferredVoices) {
            const voice = voices.find(v => v.name.includes(preferred));
            if (voice) {
                this.browserVoice = voice;
                break;
            }
        }
        
        // Fallback to any female voice
        if (!this.browserVoice) {
            this.browserVoice = voices.find(v => 
                v.name.toLowerCase().includes('female') ||
                v.name.toLowerCase().includes('woman')
            );
        }
        
        // Last resort: first available voice
        if (!this.browserVoice && voices.length > 0) {
            this.browserVoice = voices[0];
        }
    }
    
    async speak(text, audioData = null) {
        if (this.isSpeaking) {
            window.speechSynthesis.cancel();
        }
        
        this.isSpeaking = true;
        document.getElementById('avatar-visual')?.classList.add('speaking');
        
        if (audioData && this.engine !== 'browser') {
            // Play pre-generated audio
            await this.playAudio(audioData);
        } else {
            // Use browser TTS
            await this.speakBrowser(text);
        }
        
        this.isSpeaking = false;
        document.getElementById('avatar-visual')?.classList.remove('speaking');
    }
    
    speakBrowser(text) {
        return new Promise((resolve) => {
            const utterance = new SpeechSynthesisUtterance(text);
            
            if (this.browserVoice) {
                utterance.voice = this.browserVoice;
            }
            
            // Adjust for more natural speech
            utterance.rate = 0.9;   // Slightly slower
            utterance.pitch = 1.1;  // Slightly higher for female voice
            utterance.volume = 1.0;
            
            utterance.onend = () => resolve();
            utterance.onerror = () => resolve();
            
            window.speechSynthesis.speak(utterance);
        });
    }
    
    playAudio(dataUrl) {
        return new Promise((resolve) => {
            const audio = new Audio(dataUrl);
            audio.onended = () => resolve();
            audio.onerror = () => resolve();
            audio.play().catch(() => resolve());
        });
    }
    
    setEngine(engine) {
        this.engine = engine;
        localStorage.setItem('joi-voice-engine', engine);
    }
    
    async getVoiceOptions() {
        const response = await fetch('/voice/engines');
        return await response.json();
    }
    
    async setVoicePreference(engine, voiceName) {
        const response = await fetch('/voice/preference', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({engine, voice: voiceName})
        });
        return await response.json();
    }
}

// Initialize voice system
let joiVoice = new JoiVoice();

// Load voices when available
if (window.speechSynthesis.onvoiceschanged !== undefined) {
    window.speechSynthesis.onvoiceschanged = () => {
        joiVoice.loadBrowserVoices();
    };
}

// Replace the existing speak function
window.originalSpeak = window.speak;
window.speak = function(text, audioData = null) {
    joiVoice.speak(text, audioData);
};
"""

def get_available_engines() -> Dict[str, Any]:
    """Get list of available TTS engines"""
    engines = {
        "browser": {
            "available": True,
            "name": "Browser TTS",
            "description": "Built-in browser text-to-speech (free)",
            "quality": "medium"
        },
        "openai": {
            "available": HAVE_OPENAI and bool(os.getenv("OPENAI_API_KEY")),
            "name": "OpenAI TTS",
            "description": "High-quality neural voices (requires OpenAI API key)",
            "quality": "high",
            "voices": ["nova", "shimmer", "alloy", "echo", "fable", "onyx"],
            "recommended": "nova"
        }
    }
    
    if HAVE_ELEVENLABS:
        engines["elevenlabs"] = {
            "available": bool(os.getenv("ELEVENLABS_API_KEY")),
            "name": "ElevenLabs",
            "description": "Ultra-realistic AI voices (requires ElevenLabs API key)",
            "quality": "ultra-high",
            "note": "pip install elevenlabs"
        }
    
    return {
        "ok": True,
        "engines": engines
    }

if __name__ == "__main__":
    print("Joi Advanced Voice System")
    print("=========================\n")
    
    engines = get_available_engines()
    print("Available TTS Engines:\n")
    
    for engine_id, info in engines["engines"].items():
        status = "✓" if info["available"] else "✗"
        print(f"{status} {info['name']}")
        print(f"   {info['description']}")
        print(f"   Quality: {info['quality']}")
        if 'voices' in info:
            print(f"   Voices: {', '.join(info['voices'])}")
        print()
    
    print("\nRecommended Setup:")
    print("1. For best quality (free): Use OpenAI TTS with 'nova' voice")
    print("2. For ultra-realistic: Use ElevenLabs (paid)")
    print("3. For quick setup: Use browser TTS (built-in)")
    
    print("\nTo enable OpenAI TTS:")
    print("- You already have an OpenAI API key for GPT")
    print("- TTS costs ~$0.015 per 1000 characters")
    print("- Set voice engine in Joi's settings")
