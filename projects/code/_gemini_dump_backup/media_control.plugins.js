const { exec } = require('child_process');

module.exports = (context) => {
    const { ipcMain, screen } = context;

    // Command to Enlarge the Joi UI Window
    ipcMain.on('enlarge-ui', () => {
        if (context.chatWin) {
            const { width, height } = screen.getPrimaryDisplay().workAreaSize;
            context.chatWin.setBounds({ x: 0, y: 0, width, height }, true);
        }
    });

    // Command to trigger Full Screen (Alt+Enter) in the active window (Media Player)
    ipcMain.on('make-fullscreen', () => {
        // Simple PowerShell script to send Alt+Enter to the system
        const psCommand = `powershell -Command "$wshell = New-Object -ComObject WScript.Shell; $wshell.SendKeys('%{ENTER}')"`;
        exec(psCommand);
    });

    // Command to shrink Joi UI back to normal
    ipcMain.on('shrink-ui', () => {
        if (context.chatWin) {
            context.chatWin.setSize(450, 700, true);
        }
    });
};