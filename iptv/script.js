function addChannel() {
  const div = document.createElement("div");
  div.className = "channel";
  div.innerHTML = `
    <input type="text" placeholder="ชื่อช่อง" class="channel-name"/>
    <input type="text" placeholder="ลิงก์ .m3u8" class="channel-url"/>
    <input type="text" placeholder="group-title" class="channel-group"/>
    <input type="text" placeholder="tvg-id (EPG)" class="channel-id"/>
    <input type="text" placeholder="โลโก้ (URL)" class="channel-logo"/>
    <input type="text" placeholder="Referrer" class="channel-referrer"/>
    <input type="text" placeholder="User-Agent" class="channel-ua"/>
    <button onclick="this.parentElement.remove()">❌</button>
  `;
  document.getElementById("channels-container").appendChild(div);
}

function buildM3U() {
  const names = document.querySelectorAll(".channel-name");
  const urls = document.querySelectorAll(".channel-url");
  const groups = document.querySelectorAll(".channel-group");
  const ids = document.querySelectorAll(".channel-id");
  const logos = document.querySelectorAll(".channel-logo");
  const referrers = document.querySelectorAll(".channel-referrer");
  const uas = document.querySelectorAll(".channel-ua");

  let m3u = "#EXTM3U\n";
  for (let i = 0; i < names.length; i++) {
    const name = names[i].value.trim();
    const url = urls[i].value.trim();
    const group = groups[i].value.trim();
    const id = ids[i].value.trim();
    const logo = logos[i].value.trim();
    const ref = referrers[i].value.trim();
    const ua = uas[i].value.trim();
    if (name && url) {
      m3u += `#EXTINF:-1`;
      if (id) m3u += ` tvg-id="${id}"`;
      if (name) m3u += ` tvg-name="${name}"`;
      if (logo) m3u += ` tvg-logo="${logo}"`;
      if (group) m3u += ` group-title="${group}"`;
      m3u += `,${name}\n`;
      if (ref) m3u += `#EXTVLCOPT:http-referrer=${ref}\n`;
      if (ua) m3u += `#EXTVLCOPT:http-user-agent=${ua}\n`;
      m3u += `${url}\n`;
    }
  }
  return m3u;
}

function generatePlaylist() {
  const m3u = buildM3U();
  const blob = new Blob([m3u], { type: "text/plain;charset=utf-8" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "playlist.m3u";
  link.click();
}

function copyPlaylist() {
  navigator.clipboard.writeText(buildM3U());
  alert("✅ คัดลอก Playlist ไปยัง Clipboard แล้ว!");
}

// สร้างช่องแรกอัตโนมัติ
addChannel();
