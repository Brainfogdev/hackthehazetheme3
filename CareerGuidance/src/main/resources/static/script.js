const baseUrl = "http://localhost:8080/api/career";

document.getElementById("profileForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const profile = {
    name: document.getElementById("name").value,
    age: parseInt(document.getElementById("age").value),
    currentClass: document.getElementById("currentClass").value,
    currentStream: document.getElementById("currentStream").value,
    subjects: document.getElementById("subjects").value.split(","),
    interests: document.getElementById("interests").value.split(","),
    skills: document.getElementById("skills").value.split(","),
    careerAspirations: document.getElementById("careerAspirations").value.split(","),
    academicPerformance: document.getElementById("academicPerformance").value,
    location: document.getElementById("location").value,
    familyBackground: document.getElementById("familyBackground").value,
    economicStatus: document.getElementById("economicStatus").value,
    examScores: {}
  };

  const response = await fetch(`${baseUrl}/profile`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });

  if (response.ok) {
    alert("Profile created successfully!");
  } else {
    alert("Error creating profile.");
  }
});

async function loadProfiles() {
  const response = await fetch(`${baseUrl}/profiles`);
  const profiles = await response.json();
  const list = document.getElementById("profilesList");
  list.innerHTML = "";
  profiles.forEach((p) => {
    const li = document.createElement("li");
    li.textContent = `${p.id}: ${p.name} (${p.currentStream}, ${p.currentClass})`;
    list.appendChild(li);
  });
}

async function getRecommendations() {
  const id = document.getElementById("recommendationId").value;
  const response = await fetch(`${baseUrl}/recommendations/${id}`, {
    method: "POST"
  });

  const list = document.getElementById("recommendationsList");
  list.innerHTML = "";

  if (response.ok) {
    const recs = await response.json();
    recs.forEach((r) => {
      const li = document.createElement("li");
      li.textContent = `${r.title}: ${r.description}`;
      list.appendChild(li);
    });
  } else {
    alert("No recommendations found or error occurred.");
  }
}
