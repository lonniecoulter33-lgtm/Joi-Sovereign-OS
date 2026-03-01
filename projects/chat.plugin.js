\
/**
 * Minimal chat plugin:
 * - Receives messages from renderer via IPC: "plugin:chat"
 * - Sends replies back via IPC: "plugin:reply"
 * - Notifies the avatar window to react via: "avatar:react"
 *
 * You can later swap the reply logic with Python or OpenAI calls.
 */
module.exports.init = function init(ctx) {
  const { ipcMain } = ctx;

  if (!ipcMain) {
    console.error("[chat.plugin] ipcMain missing in context");
    return;
  }

  // Avoid double-registering if plugins reload
  const CHANNEL_IN = "plugin:chat";
  const CHANNEL_OUT = "plugin:reply";
  const AVATAR_REACT = "avatar:react";

  // Remove prior listeners for this plugin's handler signature if any
  try {
    ipcMain.removeAllListeners(CHANNEL_IN);
  } catch (_) {}

  ipcMain.on(CHANNEL_IN, async (event, msg) => {
    try {
      const text = (msg ?? "").toString();

      // Simple placeholder reply
      const reply = text.trim()
        ? `Joi heard: ${text}`
        : "Say something and I’ll respond 🙂";

      // Reply to the sender (chat window)
      event.sender.send(CHANNEL_OUT, reply);

      // Optional: tell the avatar window to animate/react
      const aw = typeof ctx.getAvatarWin === "function" ? ctx.getAvatarWin() : ctx.avatarWin;
      if (aw && !aw.isDestroyed()) {
        aw.webContents.send(AVATAR_REACT, { mood: "talking", text });
      }
    } catch (err) {
      console.error("[chat.plugin] handler error:", err);
      try {
        event.sender.send(CHANNEL_OUT, "Sorry — something went wrong on my side.");
      } catch (_) {}
    }
  });

  console.log("[chat.plugin] Ready");
};
