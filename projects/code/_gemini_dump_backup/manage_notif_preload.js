// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts
const { contextBridge, ipcRenderer } = require("electron");
const { webFrame } = require("electron");

webFrame.insertCSS(`
::-webkit-scrollbar {
  display: none;
}
`);

var listener;
contextBridge.exposeInMainWorld("electron", {
  send: (data) => ipcRenderer.send("from-manage-notif-renderer", data),
  onMessage: (callback) => {
    console.log("Attaching callback");
    listener = callback;
  },
});

ipcRenderer.on("to-manage-notif-renderer", (event, arg) => {
  if (listener) {
    listener(arg);
  } else {
    console.log(arg);
    console.warn("No listener attached!");
  }
});
