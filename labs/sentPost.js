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
  sendPostRequest();