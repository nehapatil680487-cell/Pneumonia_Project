(function () {
  const form = document.querySelector("form");
  const fileInput = form.querySelector('input[type=file]');
  const nameInput = form.elements["patient_name"];
  const box = document.querySelector(".upload-box");

  // names of the boxes to fill (same as name="..." in the form)
  const FIELDS = ["patient_name", "age", "gender", "wbc", "rbc", "platelet",
                  "hb", "temperature", "spo2", "pulse_rate", "crp"];

  // message line inside the upload box
  const status = document.createElement("div");
  status.className = "upload-hint";
  status.style.fontWeight = "600";
  box.appendChild(status);

  function show(text, color) {
    status.style.color = color;
    status.textContent = text;
  }

  // ask Python to look up the patient in the Excel file, then fill the form
  async function lookup() {
    const file = fileInput.files[0];
    if (!file) return;

    show("Looking up patient in Excel file...", "#64748b");
    const params = new URLSearchParams({ name: nameInput.value.trim(), file: file.name });

    try {
      const res = await fetch("/excel-lookup?" + params.toString());
      const json = await res.json();

      if (!json.found) {
        show(json.message, "#b45309");
        return;
      }
      FIELDS.forEach(name => {
        const el = form.elements[name];
        if (el && json.data[name] !== undefined && json.data[name] !== "") {
          el.value = json.data[name];
        }
      });
      show("\u2714 " + json.message, "#15803d");
    } catch (e) {
      show("Lookup failed. Please enter the values manually.", "#b91c1c");
    }
  }

  // when an X-ray is chosen with the "Choose File" button
  fileInput.addEventListener("change", lookup);

  // when the name is typed after the X-ray was already chosen
  let timer = null;
  nameInput.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(lookup, 700);
  });

  // when an X-ray is dragged and dropped on the dashed box
  box.addEventListener("dragover", e => e.preventDefault());
  box.addEventListener("drop", e => {
    e.preventDefault();
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      fileInput.dispatchEvent(new Event("change"));
    }
  });
})();