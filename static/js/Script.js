// ajax function to load a user to database
function submitForm() {
    var form = $("#userForm");
    var data = form.serialize();
    var jsonData = JSON.stringify(data);

    $.ajax({
        url: "/registro.html",
        type: "POST",
        data: jsonData,
        contentType: "application/json",
        success: function(response) {
            console.log("Data sent successfully");
            // Handle the response from the server
        },
        error: function(error) {
            console.error("Error sending data:", error);
            // Handle the error
        }
    });
}
