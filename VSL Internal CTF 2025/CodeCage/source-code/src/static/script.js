document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("codeForm");
  const codeInput = document.getElementById("codeInput");
  const output = document.getElementById("output");
  const captchaQuestion = document.getElementById("captchaQuestion");
  const captchaInput = document.getElementById("captchaInput");
  const refreshCaptchaBtn = document.getElementById("refreshCaptcha");
  const snippetsDropdown = document.getElementById("snippets");
  const copyCodeBtn = document.getElementById("copyCodeBtn");
  const downloadCodeBtn = document.getElementById("downloadCodeBtn");
  const historyList = document.getElementById("historyList");
  let historyData = JSON.parse(
    localStorage.getItem("executionHistory") || "[]"
  );
  function escapeHTML(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }
  function renderHistory() {
    historyList.innerHTML = "";

    if (historyData.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No previous executions.";
      historyList.appendChild(li);
      return;
    }

    historyData.forEach((item) => {
      const li = document.createElement("li");

      const timeDiv = document.createElement("div");
      timeDiv.classList.add("history-time");
      timeDiv.textContent = item.timestamp || "";

      const idDiv = document.createElement("div");
      idDiv.classList.add("history-id");
      idDiv.textContent = `ID: ${item.id || "N/A"}`;

      const codePre = document.createElement("pre");
      codePre.innerHTML = escapeHTML(item.code);

      const outputPre = document.createElement("pre");
      outputPre.innerHTML = escapeHTML(item.output);

      li.appendChild(timeDiv);
      li.appendChild(idDiv);
      li.appendChild(document.createTextNode("Code:"));
      li.appendChild(codePre);
      li.appendChild(document.createTextNode("Output:"));
      li.appendChild(outputPre);
      historyList.appendChild(li);
    });
  }
  function addToHistory(code, output, id) {
    const newItem = {
      code,
      output,
      id,
      timestamp: new Date().toLocaleString(),
    };
    historyData.unshift(newItem);
    if (historyData.length > 10) {
      historyData.pop();
    }
    localStorage.setItem("executionHistory", JSON.stringify(historyData));

    renderHistory();
  }
  renderHistory();
  async function loadSnippets() {
    try {
      const response = await fetch("/snippets");
      if (!response.ok) {
        throw new Error(`Error fetching snippets: ${response.statusText}`);
      }
      const snippets = await response.json();
      snippets.forEach((snippet) => {
        const option = document.createElement("option");
        option.value = snippet.code;
        option.textContent = snippet.name;
        snippetsDropdown.appendChild(option);
      });
    } catch (error) {
      console.error("Error loading snippets:", error);
    }
  }
  snippetsDropdown.addEventListener("change", function () {
    const snippet = this.value;
    if (snippet) {
      codeInput.value = snippet.replace(/\\n/g, "\n");
    }
  });
  const fetchCaptcha = async () => {
    try {
      const response = await fetch("/get_captcha");
      if (!response.ok) {
        throw new Error(`Error fetching CAPTCHA: ${response.statusText}`);
      }
      const data = await response.json();
      captchaQuestion.textContent = data.question;
      captchaInput.value = "";
    } catch (error) {
      captchaQuestion.textContent = "Error loading CAPTCHA.";
      console.error("Error:", error);
    }
  };
  refreshCaptchaBtn.addEventListener("click", (e) => {
    e.preventDefault();
    fetchCaptcha();
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const code = codeInput.value.trim();
    const captcha = captchaInput.value.trim();

    if (!code) {
      output.textContent = "Please enter some Python code to execute.";
      return;
    }

    if (!captcha) {
      output.textContent = "Please solve the CAPTCHA.";
      return;
    }

    output.textContent = "Executing...";

    try {
      const response = await fetch("/execute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: code, captcha: captcha }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.error || `Server error: ${response.statusText}`
        );
      }

      const data = await response.json();

      if (data.success) {
        output.innerHTML = `<strong>ID:</strong> ${data.id}\n\n<strong>Output:</strong>\n${data.output}`;
        addToHistory(code, data.output, data.id);
        fetchCaptcha();
      } else {
        output.textContent = data.error;
        fetchCaptcha();
      }
    } catch (error) {
      output.textContent =
        error.message || "An error occurred while executing the code.";
      console.error("Error:", error);
      fetchCaptcha();
    }
  });

  // Nút copy code
  copyCodeBtn.addEventListener("click", () => {
    const code = codeInput.value;
    if (!code) return;

    navigator.clipboard.writeText(code).then(
      () => {
        alert("Code copied to clipboard!");
      },
      (err) => {
        console.error("Failed to copy code:", err);
      }
    );
  });
  downloadCodeBtn.addEventListener("click", () => {
    const code = codeInput.value;
    if (!code) return;

    const filename = "code.py";
    const blob = new Blob([code], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  });
  loadSnippets();
  fetchCaptcha();
  const footer = document.createElement("footer");
  footer.textContent = "© 2025 By VSL. All Rights Reserved.";
  document.body.appendChild(footer);
});
