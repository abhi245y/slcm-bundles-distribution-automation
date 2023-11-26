// Experimental stuff. Still woking on this.

 // Function to send POST request
 function sendPostRequest() {
  // Extract the value of bundleID from the div with id="bundleID"
  var bundleIDValue = $('#bundlesdiv .media-title:first').text();

  // Create the payload object with bundleID
  const payload = {
    bundleID: bundleIDValue
  };

  // Convert payload to JSON
  const jsonData = JSON.stringify(payload);

  // Define the URL to send the POST request to
  const url = 'http://127.0.0.1:5000/api/get_data';

  // Send the POST request
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: jsonData
  })
    .then(response => response.json())
    .then(data => {
      // Extract the district value from the response JSON
      const districtValue = data.district;

      // Show the district value in an alert
      // alert('District: ' + districtValue);
      if (data.status== "success"){
        swal({  
          title: "Camp Details",
          text:"Goes to "+districtValue+" Camp",
          type:"info",
          showConfirmButton: true
        })
      }else{
        swal({  
          title: "Error",
          text:"Distribution Not Found",
          type:"error",
          showConfirmButton: true
        })
      }
    })
    .catch(error => {
      console.error('Error:', error);
      // alert('Error occurred while processing the request.');
      swal({  
        title: "Error",
        text:"Something went wrong",
        type:"error",
        showConfirmButton: true
      })
    });
}

// Call the function to send the POST request
// sendPostRequest();

function handleMutation(mutationsList, observer) {
    // Loop through all the mutations
    for (const mutation of mutationsList) {
      // Check if nodes have been added
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        // Check if the added nodes contain the div with id="bundlesdiv"
        const bundlesDiv = document.getElementById('bundlesdiv');
        if (bundlesDiv && bundlesDiv.children.length > 0) {
          // Show the alert when the div is populated
            setTimeout(() => {
        var firstCardTitle = $('#bundlesdiv .media-title:first').text();
                // alert('The div with id="bundlesdiv" is populated!');
        sendPostRequest();
    }, 1000); 
         
          // You can perform additional actions here if needed
          // For example, you could access the populated data or modify the page content
        }
      }
    }
  }

  // Create a new MutationObserver
  const observer = new MutationObserver(handleMutation);

  // Target the div with id="bundlesdiv" and listen for childList changes
  const targetNode = document.getElementById('bundlesdiv');
  const config = { childList: true };

  // Start observing the target node
  observer.observe(targetNode, config);



  // Set 2
  // Function to send POST request
// function sendPostRequest() {
//   // Extract the value of bundleID from the div with id="bundleID"
//   var bundleIDValue = $('#bundlesdiv .media-title:first').text();

//   // Create the payload object with bundleID
//   const payload = {
//     bundleID: bundleIDValue
//   };

//   // Convert payload to JSON
//   const jsonData = JSON.stringify(payload);

//   // Define the URL to send the POST request to
//   const url = 'http://127.0.0.1:5000/api/get_data';

//   // Send the POST request
//   fetch(url, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: jsonData
//   })
//     .then(response => response.json())
//     .then(data => {
//       // Show the district value in an alert
//       // alert('District: ' + districtValue);
//       if (data.status== "success"){
//         swal({  
        //   title: "Camp Details",
        //   text:bundleIDValue+" Goes to "+districtValue+" Camp",
        //   type:"info",
        //   showConfirmButton: true
        // })
//       }
//     }).catch(error => {
//       console.error('Error:', error);
//       // alert('Error occurred while processing the request.');
//       swal({  
//         title: "Opps Something went wrong",
//         text:error,
//         type:"error",
//         showConfirmButton: true
//       })
//     });
// }

// (function() {
//   var _old_alert = window.swal;
//   window.swal = function() {
//     // https://media.geeksforgeeks.org/wp-content/uploads/20190531135120/beep.mp3
//       // run some code when the alert pops up
//     var audio = new Audio('https://media.geeksforgeeks.org/wp-content/uploads/20190531135120/beep.mp3');
//     audio.play();
//     _old_alert.apply(window,arguments);
//     // alert("Working")
//   };
// })();

function saveDetails(){
  var bundleIDValue = $('#bundlesdiv .media-title:first').text();
  
  const payload = {
    bundleID: bundleIDValue
  };

  // Convert payload to JSON
  const jsonData = JSON.stringify(payload);

  // Define the URL to send the POST request to
  const url = 'http://127.0.0.1:5000/api/save_data';

  // Send the POST request
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: jsonData
  })
    .then(response => response.json())
    .then(data => {
      // Extract the district value from the response JSON

      // Show the district value in an alert
      // alert('District: ' + districtValue);
      if (data.status== "Error"){
        swal({  
          title: "Camp Details",
          text: "Some Error",
          type:"info",
          showConfirmButton: true
        })
      }
    })
    .catch(error => {
      console.error('Error:', error);
      // alert('Error occurred while processing the request.');
      swal({  
        title: "Opps Something went wrong",
        text:error,
        type:"error",
        showConfirmButton: true
      })
    });
}

// Call the function to send the POST request
// sendPostRequest();

function scanningAlert(firstCardTitle){
  var qpCode = firstCardTitle.match(/(\w+ \d{4})/)[0];

  if (prvCode !== ''){
      if(prvCode !== qpCode){
        swal({  
              title: "Change in QP Series",
              text: "Previous QP code: ".concat(prvCode," Current QP code: ", qpCode),
              type:"info",
              showConfirmButton: true
            })
          }
      }
  prvCode = qpCode
}
function handleMutation(mutationsList, observer) {
    // Loop through all the mutations
    for (const mutation of mutationsList) {
      // Check if nodes have been added
      if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
        // Check if the added nodes contain the div with id="bundlesdiv"
        const bundlesDiv = document.getElementById('bundlesdiv');
        if (bundlesDiv && bundlesDiv.children.length > 0) {
          // Show the alert when the div is populated
            setTimeout(() => {
        var firstCardTitle = $('#bundlesdiv .media-title:first').text();
                // alert('The div with id="bundlesdiv" is populated!');
        // sendPostRequest();
        // saveDetails();
        scanningAlert(firstCardTitle);
    }, 400); 
         
          // You can perform additional actions here if needed
          // For example, you could access the populated data or modify the page content
        }
      }
    }
  }


  if(window.location.pathname === '/cd-unit/bundle-recive'){
    // Create a new MutationObserver
  const observer = new MutationObserver(handleMutation);

  // Target the div with id="bundlesdiv" and listen for childList changes
  const targetNode = document.getElementById('bundlesdiv');
  const config = { childList: true };

  // Start observing the target node
  observer.observe(targetNode, config);
  }
  
    //Enter Key Listner for camp allocation page

  document.addEventListener("keyup", function(event) {
    if (window.location.pathname === '/cd-unit/qpcode-wise-bundle-list'){
      if (event.which === 13) {
          document.getElementById('submit_button').click();
      }
    }
});


  
  