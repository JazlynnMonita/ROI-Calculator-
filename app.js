// app.js

document.addEventListener("DOMContentLoaded", () => {
  const simulateBtn = document.getElementById("simulateBtn");
  const saveBtn = document.getElementById("saveBtn");
  const loadBtn = document.getElementById("loadBtn");
  const scenarioSelect = document.getElementById("scenarioSelect");

  const resultDiv = document.getElementById("results");

  // Run simulation
  simulateBtn.addEventListener("click", async () => {
    const formData = getFormData();
    if (!formData) return;

    const response = await fetch("/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    const data = await response.json();
    displayResults(data);
  });

  // Save scenario
  saveBtn.addEventListener("click", async () => {
    const formData = getFormData();
    if (!formData) return;

    const response = await fetch("/scenarios", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    const data = await response.json();
    alert(data.message || "Scenario saved!");
    loadScenarios();
  });

  // Load selected scenario
  loadBtn.addEventListener("click", async () => {
    const scenarioId = scenarioSelect.value;
    if (!scenarioId) return;

    const response = await fetch(`/scenarios/${scenarioId}`);
    const scenario = await response.json();
    populateForm(scenario);
  });

  // Load scenario options on page load
  loadScenarios();

  // Helper functions
  function getFormData() {
    const scenario_name = document.getElementById("scenario_name").value.trim();
    const monthly_invoice_volume = parseFloat(document.getElementById("monthly_invoice_volume").value);
    const num_ap_staff = parseFloat(document.getElementById("num_ap_staff").value);
    const avg_hours_per_invoice = parseFloat(document.getElementById("avg_hours_per_invoice").value);
    const hourly_wage = parseFloat(document.getElementById("hourly_wage").value);
    const error_rate_manual = parseFloat(document.getElementById("error_rate_manual").value);
    const error_cost = parseFloat(document.getElementById("error_cost").value);
    const time_horizon_months = parseFloat(document.getElementById("time_horizon_months").value);
    const one_time_implementation_cost = parseFloat(document.getElementById("one_time_implementation_cost").value) || 0;

    if (!scenario_name) {
      alert("Please enter a scenario name.");
      return null;
    }

    return {
      scenario_name,
      monthly_invoice_volume,
      num_ap_staff,
      avg_hours_per_invoice,
      hourly_wage,
      error_rate_manual,
      error_cost,
      time_horizon_months,
      one_time_implementation_cost,
    };
  }

  function displayResults(data) {
    resultDiv.innerHTML = `
      <h3>Results:</h3>
      <p><strong>Monthly Savings:</strong> $${data.monthly_savings.toFixed(2)}</p>
      <p><strong>Payback (months):</strong> ${data.payback_months.toFixed(2)}</p>
      <p><strong>ROI (%):</strong> ${data.roi_percentage.toFixed(2)}</p>
    `;
  }

  async function loadScenarios() {
    const response = await fetch("/scenarios");
    const scenarios = await response.json();

    scenarioSelect.innerHTML = '<option value="">--Select Scenario--</option>';
    scenarios.forEach((s) => {
      const option = document.createElement("option");
      option.value = s.id;
      option.textContent = s.scenario_name;
      scenarioSelect.appendChild(option);
    });
  }

  function populateForm(scenario) {
    document.getElementById("scenario_name").value = scenario.scenario_name;
    document.getElementById("monthly_invoice_volume").value = scenario.monthly_invoice_volume;
    document.getElementById("num_ap_staff").value = scenario.num_ap_staff;
    document.getElementById("avg_hours_per_invoice").value = scenario.avg_hours_per_invoice;
    document.getElementById("hourly_wage").value = scenario.hourly_wage;
    document.getElementById("error_rate_manual").value = scenario.error_rate_manual;
    document.getElementById("error_cost").value = scenario.error_cost;
    document.getElementById("time_horizon_months").value = scenario.time_horizon_months;
    document.getElementById("one_time_implementation_cost").value = scenario.one_time_implementation_cost || 0;
  }
});
