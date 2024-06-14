let temp = 0;

document.addEventListener("DOMContentLoaded", function () {
  autosize(document.querySelector('textarea[name="user_input"]'));
});

document
  .querySelector('input[type="file"]')
  .addEventListener("change", function () {
    const h4Tag = document.getElementById("file-name"); // Get the h4 tag
    const fileInput = document.querySelector('input[type="file"]');

    if (fileInput.files.length > 0) {
      // File is selected
      const fileName = fileInput.files[0].name; // Get the filename
      h4Tag.innerText = "Uploaded file: " + fileName; // Change the h4 tag text to the filename
    } else {
      // No file selected
      h4Tag.innerText = "Upload your CSV to get started.."; // Change the h4 tag text back to default
    }
  });

document.querySelector("form").addEventListener("submit", async function (e) {
  e.preventDefault(); // Prevent the default form submission behavior
  const submittedButton = e.submitter;
  const textarea = document.querySelector('textarea[name="user_input"]');

  // Check which button was clicked
  if (submittedButton.id === "start") {
    temp += 1;
    // Handle the "Start" button click
    document.getElementById("stop").style.display = "block";
    document.getElementById("start").style.display = "none";

    // Get form data
    const formData = new FormData(e.target);

    // Send form data to the server asynchronously
    const response = await fetch("/get_response", {
      method: "POST",
      body: formData,
    });
    textarea.value = "";
    autosize.update(textarea);

    // Get the response text
    const outputText = await response.text();
    console.log(outputText);
    const inputText = formData.get("user_input"); // Get the user input

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "user");
    this.parentNode.insertBefore(messageDiv, this); // Insert messageDiv above the form

    // Function to display text with popping effect
    async function displayTextWithPopping(text, element) {
      for (let i = 0; i < text.length; i++) {
        if (temp == 2) break;
        if(text[i] =="\n"){
          element.innerHTML += "<br/>";
          element.innerHTML += "<br/>";
        }
        element.innerHTML += text[i]; // Add letter to the message
        await new Promise((resolve) => setTimeout(resolve, 50)); // Wait for a short delay
      }
    }

    // Create a span for the user input
    const inputSpan = document.createElement("span");
    inputSpan.classList.add("input-span", "curved-box");
    messageDiv.appendChild(inputSpan);

    // Display the user input
    inputSpan.textContent = inputText; // Update input span with input text

    // Insert a line break with a space
    const spaceDiv = document.createElement("div");
    spaceDiv.classList.add("space");
    messageDiv.appendChild(spaceDiv);

    // Create a span for the output text
    const outputSpan = document.createElement("span");
    outputSpan.classList.add("output-span");
    messageDiv.appendChild(outputSpan);

    const myObj = JSON.parse(outputText);
    console.log(myObj);
    let ttext = "";
    for (let x in myObj) {
      ttext += x+": "+myObj[x]+"\n";
       // Display the output text with popping effect
      await displayTextWithPopping(ttext, outputSpan);
      ttext='';
    }
   

    // Reset buttons and temp
    document.getElementById("start").style.display = "block";
    document.getElementById("stop").style.display = "none";
    temp = 0;
  } else if (submittedButton.id === "stop") {
    temp += 1;
    // Handle the "Stop" button click
    document.getElementById("start").style.display = "block";
    document.getElementById("stop").style.display = "none";
    e.target.reset();

    // Optionally, you can trigger the autosize to resize the textarea
    autosize.update(textarea);
  }
});
