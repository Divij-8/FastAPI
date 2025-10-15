export const mockQueryResponse = {
  answer: "Based on available manuals, inspect ignition and vacuum leaks. Steps: 1) Check plugs and coils 2) Smoke test intake 3) Verify fuel pressure 4) Scan for related codes.",
  sources: [
    { text: "Ignition diagnosis steps...", source: "toyota_camry_2018_manual.pdf", page: 123, score: 0.12 },
    { text: "Vacuum leak test...", source: "generic_powertrain.pdf", page: 45, score: 0.25 }
  ],
  suggested_actions: ["Check spark plugs", "Run smoke test", "Measure fuel pressure"]
}

export const mockDiagnostic = {
  code: "P0300",
  name: "Random/Multiple Cylinder Misfire Detected",
  description: "PCM detected random/multiple misfires",
  symptoms: ["Rough idle", "Hesitation"],
  possible_causes: ["Spark plugs", "Vacuum leak"],
  troubleshooting_steps: ["Inspect plugs", "Smoke test intake"]
}

export const mockVehicle = {
  make: "Toyota",
  model: "Camry",
  year: 2018,
  engine: "2.5L I4",
  transmission: "8-speed automatic",
  specs: { oil_capacity: "4.8 qt", spark_plug_gap: "0.044 in" }
}
