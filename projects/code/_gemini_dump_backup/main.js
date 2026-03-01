const { app, BrowserWindow } = require('electron');

function createWindow() {
    const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    win.loadFile('joi_ui.html');
    win.setIcon('path/to/joi_avatar.png'); // Update this path to your avatar PNG
}

app.whenReady().then(createWindow);