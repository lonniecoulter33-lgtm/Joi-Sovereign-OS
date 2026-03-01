const { ipcRenderer } = require('electron');

window.joiElectron = {
    openChat:       () => ipcRenderer.send('open-chat'),
    closeChat:      () => ipcRenderer.send('close-chat'),
    avatarClicked:  () => ipcRenderer.send('avatar-clicked'),
};
