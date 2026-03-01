// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
const { ipcRenderer } = require("electron");

ipcRenderer.on("to-notif-renderer", (_, data) => {
  console.log(data);
  // Was previously notif window but this wasn't necessary anymore so just made this a debug window as this was widely used by both dev and qa 
});