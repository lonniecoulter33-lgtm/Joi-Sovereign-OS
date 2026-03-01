const fs = require("fs");
const path = require("path");

function loadPlugins(context) {
  const dir = __dirname;

  if (!fs.existsSync(dir)) return;

  const files = fs.readdirSync(dir).filter((f) => f.endsWith(".plugin.js"));

  for (const file of files) {
    try {
      const plugin = require(path.join(dir, file));
      if (plugin && typeof plugin.init === "function") {
        plugin.init(context);
        console.log("[Plugin] Loaded:", file);
      }
    } catch (err) {
      console.error("[Plugin] Failed:", file, err);
    }
  }
}

module.exports = { loadPlugins };
