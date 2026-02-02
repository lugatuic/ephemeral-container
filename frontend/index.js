
function launch() {
  console.log("attempt to login");
  const netid = document.getElementById("NetID").value;
  const button = document.getElementById("login-button");
  netid.trim();

  if(template_id == -1 || !netid){
    document.getElementById("status").innerHTML = `<span id="fail-label">[FAILED]</span> Please enter your NetID and select a container.`;
    return;
  }
  
  button.disabled = true;
  button.textContent = "Launching..."
  document.getElementById("status").textContent = "";

  fetch("/api/launch", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ netid, template_id})
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
      document.getElementById("status").innerHTML = `<span id="success-label">[SUCCESS]</span> Environment launched. <a id="link" href="${data.url}" target="_blank">Click here to access.</a>`;
    } else {
      document.getElementById("status").textContent = "Error: " + data.message;
    }
  })
  .catch(err => {
    document.getElementById("status").innerHTML = `<span id="fail-label">[FAILED]</span> Something went wrong. Please try again.`;
    button.disabled = false;
    button.textContent = "Launch"
    console.error(err);
  })
  .finally(() => {
    button.disabled = false;
    button.textContent = "Launch";
  });
}


//TO DO: API call that returns all available types of containers for users

//[Key: Name of Container, Value: value for launch]
const containers = new Map();
containers.set("Default Debian Linux", 142);
let template_id = -1; //Nothing selected. 

const dropdownButton = document.getElementById("dropdown-button");
const dropdownText = document.getElementById("button-text");
const dropdownIcon = document.getElementById("dropdown-icon");
const dropdownList = document.getElementById("dropdown-list");
const selectedValue = document.getElementById('selectedValue');

//Populate containers within the dropdown.
containers.forEach((id, name) => {
    const div = document.createElement('div');
    div.className = 'dropdown-item';
    div.textContent = name;
    div.onclick = () => selectItem(name);
    dropdownList.appendChild(div);
});

//Toggle dropdown
dropdownButton.onclick = (e) => {
  e.stopImmediatePropagation(); //Prevent immediate triggering of the closing.
  dropdownList.classList.toggle('open'); 
  dropdownIcon.classList.toggle('active');
}

//Selecting a item from the dropbox
function selectItem(name){
  dropdownText.textContent = name;
  template_id = containers.get(name);
  dropdownList.classList.remove('open');
  dropdownIcon.classList.remove('active');
}

document.addEventListener('click', (e) => {
    if(!dropdownList.contains(e.target)){
      dropdownList.classList.remove('open');
      dropdownIcon.classList.remove('active');
    }
});


