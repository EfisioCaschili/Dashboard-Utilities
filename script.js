document.getElementById("scriptSelector").addEventListener("change", updateFields);

function updateFields() {
  const container = document.getElementById("fieldsContainer");
  container.innerHTML = ""; // reset

  const script = document.getElementById("scriptSelector").value;

  if (script === "Create_PDF_Report/main.py") {
    container.innerHTML = `
    
        <div class="input-group">
            <input type="date" id="today">
            <label for="today">Today:</label>
        </div>

        <div class="input-group">
            <input type="date" id="tomorrow">
            <label for="tomorrow">Tomorrow:</label>
        </div>
     
    `;
  } else if (script === "WEEKLY REPORT/main.py") {
    container.innerHTML = `
      
      <div class="input-group">
         <input type="number" id="year" min="2000" max="2100" placeholder="Year" value="2025"> 
         <label for="year">Year:</label>
      </div>

      <div class="input-group">
        <input type="number" id="week" min="1" max="52" placeholder="Week" value="1"> 
        <label for="week">Week:</label>
      </div>
    `;
  }
}

async function runScript() {
  const scriptName = document.getElementById("scriptSelector").value;
  const outputBox = document.getElementById("outputBox");

  let payload = { script: scriptName };

  const todayInput = document.getElementById("today");
  const tomorrowInput = document.getElementById("tomorrow");
  const yearInput = document.getElementById("year");
  const weekInput = document.getElementById("week");

  if (todayInput) payload.today = todayInput.value;
  if (tomorrowInput) payload.tomorrow = tomorrowInput.value;
  if (yearInput) payload.year = yearInput.value;
  if (weekInput) payload.week = weekInput.value;

  outputBox.textContent = "Execution on going...";

  try {
    const response = await fetch(`/run_script`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    outputBox.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    outputBox.textContent = "Error: " + err;
  }
}
