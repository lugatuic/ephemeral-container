
function launch() {
  console.log("attempt to login");
  const netid = document.getElementById("NetID").value;
  const button = document.getElementById("login-button");
  if (!netid.trim()) {
    alert("Please enter a valid NetID");
    return;
  }

  button.disabled = true;
  button.textContent = "Launching..."

  fetch("http://doom.acmuic.org/api/launch", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ netid })
  })
  .then(res => {
    if(!res.ok){
        throw new Error(`HTTP error: ${res.status}`);
    } else{
         return res.json();
    }
  })
  .then(data => {
    if (data.success) {
      document.getElementById("status").innerHTML = `<span id="success-label">[SUCCESS]</span> Environment launched. <a id="link" "href="${data.url}" target="_blank">Click here to access.</a>`;
    } else {
      document.getElementById("status").textContent = "Error: " + data.message;
    }
  })
  .catch(err => {
    document.getElementById("status").textContent = "Something went wrong.";
    button.textContent = "Launch"
    console.error(err);
  })
  .finally(() => {
    button.disabled = false;
    button.textContent = "Activate";
  });
}