#!/usr/bin/env python3
"""
Joi Avatar Animation System
Allows uploading custom avatar images and animating them with talking effects
"""

import base64
from pathlib import Path
from typing import Dict, Any, Optional

AVATAR_DIR = Path(__file__).parent / "assets" / "avatars"
AVATAR_DIR.mkdir(parents=True, exist_ok=True)

def save_avatar_image(image_data: str, name: str = "custom_avatar") -> Dict[str, Any]:
    """
    Save an uploaded avatar image
    
    Args:
        image_data: Base64 encoded image data
        name: Name for the avatar
    
    Returns:
        Dict with status and file path
    """
    try:
        # Remove data URL prefix if present
        if ',' in image_data:
            header, data = image_data.split(',', 1)
            
            # Determine file extension from header
            if 'image/png' in header:
                ext = '.png'
            elif 'image/jpeg' in header or 'image/jpg' in header:
                ext = '.jpg'
            elif 'image/gif' in header:
                ext = '.gif'
            elif 'image/webp' in header:
                ext = '.webp'
            else:
                ext = '.png'
        else:
            data = image_data
            ext = '.png'
        
        # Save the image
        image_bytes = base64.b64decode(data)
        avatar_path = AVATAR_DIR / f"{name}{ext}"
        
        with open(avatar_path, 'wb') as f:
            f.write(image_bytes)
        
        return {
            "ok": True,
            "path": str(avatar_path),
            "filename": f"{name}{ext}",
            "size": len(image_bytes)
        }
    
    except Exception as e:
        return {
            "ok": False,
            "error": f"Failed to save avatar: {str(e)}"
        }

def list_avatars() -> Dict[str, Any]:
    """List all available avatars"""
    try:
        avatars = []
        for avatar_file in AVATAR_DIR.glob("*"):
            if avatar_file.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
                stat = avatar_file.stat()
                avatars.append({
                    "name": avatar_file.stem,
                    "filename": avatar_file.name,
                    "path": str(avatar_file),
                    "size": stat.st_size
                })
        
        return {
            "ok": True,
            "avatars": avatars,
            "count": len(avatars)
        }
    
    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }

def get_avatar_data(filename: str) -> Optional[str]:
    """
    Get avatar image as base64 data URL
    
    Args:
        filename: Avatar filename
    
    Returns:
        Base64 data URL or None
    """
    try:
        avatar_path = AVATAR_DIR / filename
        if not avatar_path.exists():
            return None
        
        with open(avatar_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Determine MIME type
        ext = avatar_path.suffix.lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(ext, 'image/png')
        
        return f"data:{mime_type};base64,{image_data}"
    
    except Exception as e:
        print(f"Error loading avatar: {e}")
        return None

def delete_avatar(filename: str) -> Dict[str, Any]:
    """Delete an avatar"""
    try:
        avatar_path = AVATAR_DIR / filename
        
        if not avatar_path.exists():
            return {
                "ok": False,
                "error": "Avatar not found"
            }
        
        avatar_path.unlink()
        
        return {
            "ok": True,
            "message": f"Deleted avatar: {filename}"
        }
    
    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }

# JavaScript code for enhanced avatar animation
AVATAR_ANIMATION_JS = """
// Enhanced Avatar Animation System
class JoiAvatar {
    constructor(containerSelector) {
        this.container = document.querySelector(containerSelector);
        this.canvas = document.getElementById('avatar-canvas');
        this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
        this.image = null;
        this.isAnimating = false;
        this.currentMode = 'particle'; // 'particle' or 'image'
        this.particles = [];
        
        if (this.canvas) {
            this.canvas.width = 300;
            this.canvas.height = 300;
            this.initParticles();
        }
    }
    
    initParticles() {
        this.particles = [];
        for (let i = 0; i < 50; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                size: Math.random() * 3 + 1
            });
        }
    }
    
    loadImage(imageDataUrl) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => {
                this.image = img;
                this.currentMode = 'image';
                resolve(img);
            };
            img.onerror = reject;
            img.src = imageDataUrl;
        });
    }
    
    animate() {
        if (!this.ctx) return;
        
        if (this.currentMode === 'particle') {
            this.animateParticles();
        } else if (this.currentMode === 'image' && this.image) {
            this.animateImage();
        }
        
        requestAnimationFrame(() => this.animate());
    }
    
    animateParticles() {
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;
            
            if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;
            
            this.ctx.fillStyle = 'rgba(255, 0, 255, 0.8)';
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            this.ctx.fill();
        });
    }
    
    animateImage() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Calculate scaling to fit and center
        const scale = Math.min(
            this.canvas.width / this.image.width,
            this.canvas.height / this.image.height
        ) * 0.9;
        
        const width = this.image.width * scale;
        const height = this.image.height * scale;
        const x = (this.canvas.width - width) / 2;
        const y = (this.canvas.height - height) / 2;
        
        // Add talking effect when speaking
        const visualizer = document.getElementById('avatar-visual');
        if (visualizer && visualizer.classList.contains('speaking')) {
            // Pulsing effect
            const pulse = Math.sin(Date.now() / 100) * 5;
            this.ctx.save();
            this.ctx.translate(this.canvas.width / 2, this.canvas.height / 2);
            this.ctx.scale(1 + pulse / 100, 1 + pulse / 100);
            this.ctx.translate(-this.canvas.width / 2, -this.canvas.height / 2);
        }
        
        // Draw image
        this.ctx.drawImage(this.image, x, y, width, height);
        
        if (visualizer && visualizer.classList.contains('speaking')) {
            // Add glow effect when speaking
            this.ctx.shadowBlur = 20;
            this.ctx.shadowColor = 'rgba(255, 0, 255, 0.8)';
            this.ctx.drawImage(this.image, x, y, width, height);
            this.ctx.restore();
        }
    }
    
    switchToParticleMode() {
        this.currentMode = 'particle';
        this.initParticles();
    }
    
    switchToImageMode(imageDataUrl) {
        this.loadImage(imageDataUrl).then(() => {
            console.log('Avatar image loaded successfully');
        }).catch(err => {
            console.error('Failed to load avatar image:', err);
            this.switchToParticleMode();
        });
    }
}

// Initialize avatar when DOM is ready
let joiAvatar = null;

function initJoiAvatar() {
    joiAvatar = new JoiAvatar('#avatar-visual');
    joiAvatar.animate();
    
    // Load saved avatar if exists
    const savedAvatar = localStorage.getItem('joi-current-avatar');
    if (savedAvatar) {
        joiAvatar.switchToImageMode(savedAvatar);
    }
}

// Call this in your existing DOMContentLoaded handler
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initJoiAvatar);
} else {
    initJoiAvatar();
}
"""

# CSS for avatar display
AVATAR_CSS = """
/* Enhanced Avatar Styles */
#avatar-visual {
    position: relative;
    overflow: hidden;
}

#avatar-visual canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

#avatar-visual.speaking {
    animation: avatar-pulse 0.5s ease-in-out infinite;
}

@keyframes avatar-pulse {
    0%, 100% {
        box-shadow: 0 0 50px var(--primary-color);
        transform: scale(1);
    }
    50% {
        box-shadow: 0 0 80px var(--primary-color), 0 0 40px var(--secondary-color);
        transform: scale(1.05);
    }
}

.avatar-controls {
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 0 20px;
}

.avatar-controls button {
    padding: 10px;
    background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
    border: none;
    border-radius: 8px;
    color: white;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s;
}

.avatar-controls button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 0, 255, 0.4);
}

#avatar-upload-input {
    display: none;
}
"""

if __name__ == "__main__":
    print("Joi Avatar System")
    print("=================\n")
    
    print("Available functions:")
    print("- save_avatar_image(image_data, name)")
    print("- list_avatars()")
    print("- get_avatar_data(filename)")
    print("- delete_avatar(filename)")
    
    print(f"\nAvatar directory: {AVATAR_DIR}")
    
    avatars = list_avatars()
    if avatars["ok"] and avatars["count"] > 0:
        print(f"\nExisting avatars: {avatars['count']}")
        for a in avatars["avatars"]:
            print(f"  - {a['filename']} ({a['size']} bytes)")
    else:
        print("\nNo avatars yet. Upload one through the interface!")
