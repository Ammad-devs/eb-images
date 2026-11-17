const express = require("express");
const path = require("path");
const fs = require("fs");

const app = express();
const IMAGE_DIR = "C:\\Users\\ASUS\\Desktop\\eb_images";
const PORT = 8000;

// Serve static files (images, folders)
app.use(express.static(IMAGE_DIR));

// Add a default home page route so Chrome shows something nice
app.get("/", (req, res) => {
  fs.readdir(IMAGE_DIR, { withFileTypes: true }, (err, files) => {
    if (err) {
      return res.status(500).send("Unable to scan image directory.");
    }

    // Generate a simple HTML list of folders and files on your Desktop/eb_images
    let fileListHtml = files
      .map((file) => {
        const name = file.name;
        const isDir = file.isDirectory();
        return `<li><a href="/${name}" target="_blank">${name} ${isDir ? "📁 (Folder)" : "🖼️ (File)"}</a></li>`;
      })
      .join("");

    res.send(`
      <!DOCTYPE html>
      <html>
        <head>
          <title>EB Images Local Server</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; color: #333; }
            h1 { color: #0066cc; }
            ul { list-style: none; padding: 0; }
            li { background: #fff; margin: 8px 0; padding: 12px 16px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
            a { text-decoration: none; color: #0066cc; font-weight: bold; }
            a:hover { text-decoration: underline; }
          </style>
        </head>
        <body>
          <h1>Local Image Server Active 🚀</h1>
          <p>Browsing directory: <code>C:\\Users\\ASUS\\Desktop\\eb_images</code></p>
          <h3>Available Folders & Files:</h3>
          <ul>${fileListHtml}</ul>
        </body>
      </html>
    `);
  });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Image server running at: http://localhost:${PORT}`);
});