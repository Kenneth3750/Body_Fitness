// ajax function to load a user to database
let tope = 6;
function showAdditionalFields() {
    var planSelect = document.getElementById("plan");
    var additionalFields = document.getElementById("additionalFields");
    if (planSelect.value === "plan8") {
        tope = 10;
        additionalFields.style.display = "block";
    } else {
        additionalFields.style.display = "none";
    }
}




function checkform(event){
    var f = document.forms["userForm"].elements;
    var emptyFields = false;
    console.log(tope);
    console.log(f.length);
    for (var i = 0; i < tope; i++) {
        console.log(f[i].value)
        console.log(typeof f[i].value);
        if (f[i].value.trim() === "") {
            emptyFields = true;
            break;
        }
    }

    if (emptyFields) {
        event.preventDefault();
        appendAlert('Hacen falta datos por rellenar', 'danger');
        hideAlertAfterDelay(10000);

    } else {
        submitWithDelay(event);
    }
}


function submitWithDelay(event) {
    event.preventDefault();
        submitForm();
        appendAlert('Nuevo usuario registrado exitosamente', 'success');
        hideAlertAfterDelay(10000); 
        setTimeout(() => {
        window.location.reload();
        }, 5000);
}

function appendAlert(message, type) {
    const alertPlaceholder = document.getElementById('liveAlertPlaceholder');
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
        <div class="alert alert-${type} alert-dismissible" role="alert">
            <div>${message}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" onclick="window.location.reload();" aria-label="Close"></button>
        </div>
    `;
    alertPlaceholder.append(wrapper);
}


function hideAlertAfterDelay(delay) {
    const alert = document.querySelector('.alert');
    setTimeout(() => {
        alert.style.display = 'none';
    }, delay);
}




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
