
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
  document.getElementById("status").textContent = "";

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

//Everything is hardcoded until otherwise.
let container_types = ["Default Debian Linux", "Linux Week 2026"];
let container_id = [];

//[Key: Name of Container, Value: value for launch]
const containers = new Map();
containers.set("Default Debian Linux", 100);
containers.set("Linux Week 2026", 200);

let selected_id = -1; //Nothing selected. 

const dropdownButton = document.getElementById("dropdown-button");
const dropdownList = document.getElementById("dropdown-list");
const selectedValue = document.getElementById('selectedValue');

let isActive = false;

//Populate containers within the dropdown.
containers.forEach((id, name) => {
    const div = document.createElement('div');
    div.className = 'dropdown-item';
    div.textContent = name;
    div.onclick = () => selectItem(item);
    dropdownList.appendChild(div);
    console.log("Container Made");
});

//Toggle dropdown
dropdownButton.onclick = (e) => {
  e.stopImmediatePropagation(); //Prevent immediate triggering of the closing.
  dropdownList.classList.toggle('open'); 
  dropdownButton.classList.toggle('close');
}

//Selecting a item from the dropbox
function selectItem(item){
  dropdownButton.textContent = item;
  selectedValue.textContent = item;
  selected_id = containers.get(`${selectedValue.textContent}`);
  dropdownList.classList.remove('open');
}

document.addEventListener('click', (e) => {
    if(!dropdownList.contains(e.target)){
      dropdownList.classList.remove('open');
      dropdownButton.classList.remove('close');
    }
});


