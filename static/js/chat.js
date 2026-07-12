const form = document.getElementById("chat-form");
const promptEl = document.getElementById("prompt");
const logEl = document.getElementById("log");

function bubble(role, html, meta = "") {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.innerHTML = html + (meta ? `<div class="meta">${meta}</div>` : "");
  logEl.appendChild(div);
  logEl.scrollTop = logEl.scrollHeight;
  return div;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = promptEl.value.trim();
  if (!message) return;

  bubble("user", marked.parse(message));
  promptEl.value = "";
  const thinking = bubble("bot", "<em>Thinking…</em>");
  form.querySelector("button").disabled = true;

  try {
    const r = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await r.json();
    if (!r.ok) throw new Error(data.error || "Request failed");
    thinking.innerHTML = marked.parse(data.response) +
      `<div class="meta">${data.backend} · ${data.latency_ms} ms</div>`;
  } catch (err) {
    thinking.innerHTML = `<span style="color:#fca5a5">Error: ${err.message}</span>`;
  } finally {
    form.querySelector("button").disabled = false;
  }
});
