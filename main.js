const { app, BrowserWindow, Tray, Menu, nativeImage, ipcMain, screen, session } = require('electron');
const path = require('path');

let avatarWin = null;
let chatWin   = null;
let tray      = null;

function getScreenSize() {
    return screen.getPrimaryDisplay().workAreaSize;
}

// ── AVATAR WINDOW ────────────────────────────────────────────────────────────
function createAvatarWindow() {
    const { width: sw, height: sh } = getScreenSize();

    avatarWin = new BrowserWindow({
        width:       260,
        height:      300,
        x:           sw - 280,
        y:           sh - 320,
        transparent: true,
        frame:       false,
        alwaysOnTop: true,
        hasShadow:   false,
        resizable:   false,
        movable:     true,
        focusable:   false,
        skipTaskbar: true,
        webPreferences: {
            nodeIntegration:  true,
            contextIsolation: false,
            preload:          path.join(__dirname, 'preload.js')
        }
    });

    avatarWin.loadURL('file://' + path.join(__dirname, 'avatar.html'));
    avatarWin.on('closed', () => { avatarWin = null; });
    avatarWin.setIgnoreMouseEvents(true, { forward: true });
}

// ── CHAT WINDOW (with mic permissions + DevTools) ───────────────────────────
function createChatWindow() {
    if (chatWin) { chatWin.focus(); return; }

    const { width: sw, height: sh } = getScreenSize();

    chatWin = new BrowserWindow({
        width:       420,
        height:      620,
        x:           sw - 440,
        y:           sh - 640,
        transparent: true,
        frame:       false,
        alwaysOnTop: true,
        hasShadow:   true,
        resizable:   true,
        minWidth:    320,
        minHeight:   400,
        focusable:   true,
        skipTaskbar: false,
        webPreferences: {
            nodeIntegration:  true,
            contextIsolation: false,
            preload:          path.join(__dirname, 'preload.js')
        }
    });

    // Grant microphone permission automatically
    session.defaultSession.setPermissionRequestHandler((webContents, permission, callback) => {
        if (permission === 'media' || permission === 'microphone') {
            callback(true);  // Always allow mic
        } else {
            callback(false);
        }
    });

    chatWin.loadURL('http://127.0.0.1:5001');
    chatWin.on('closed', () => { chatWin = null; });
    
    // Enable DevTools — press F12 or Ctrl+Shift+I to open
    chatWin.webContents.openDevTools({ mode: 'detach' });
}

// ── IPC ──────────────────────────────────────────────────────────────────────
ipcMain.on('avatar-clicked', () => {
    if (chatWin) { chatWin.close(); chatWin = null; }
    else         { createChatWindow(); }
});

ipcMain.on('hide-avatar', () => {
    if (avatarWin) avatarWin.hide();
});

// ── TRAY ─────────────────────────────────────────────────────────────────────
function createTray() {
    let icon;
    try {
        icon = nativeImage.createFromDataURL(
            'data:image/png;base64,' +
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=='
        );
    } catch (e) {
        console.warn('Tray icon failed, skipping');
        return;
    }

    tray = new Tray(icon);
    tray.setContextMenu(Menu.buildFromTemplate([
        { label: 'Show Joi',   click: () => { if (!avatarWin) createAvatarWindow(); else avatarWin.show(); } },
        { label: 'Open Chat',  click: () => createChatWindow() },
        { label: 'Hide Joi',   click: () => { if (avatarWin) avatarWin.hide(); } },
        { type: 'separator' },
        { label: 'Quit',       click: () => app.quit() }
    ]));
    tray.setToolTip('Joi — Your AI Companion');
    tray.on('click', () => {
        if (avatarWin) avatarWin.show();
        else           createAvatarWindow();
    });
}

// ── APP LIFECYCLE ────────────────────────────────────────────────────────────
app.whenReady().then(() => {
    createTray();
    createAvatarWindow();
});

app.on('window-all-closed', () => {});
app.on('activate', () => { if (!avatarWin) createAvatarWindow(); });
