// ajax function to load a user to database
let tope = 6;
let searchId;
function showAdditionalFields() {
    var planSelect = document.getElementById("plan");
    var additionalFields = document.getElementById("additionalFields");
    tope = 6;
    if (planSelect.value === "8") {
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
        submitUserForm();
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

function submitUserForm() {
    var formData = {
        nombre: $('#nombre').val(),
        apellido: $('#apellido').val(),
        edad: $('#edad').val(),
        cedula: $('#cedula').val(),
        correo: $('#correo').val(),
        telefono: $('#telefono').val(),
        direccion: $('#direccion').val(),
        plan: $('#plan').val(),
        duracion: $('#duracion').val(), // Agrega campos adicionales según sea necesario
        valor: $('#valor').val()
    };

    $.ajax({
        url: '/registro.html',  // Ajusta la URL según la ruta de tu servidor Flask
        type: 'POST',
        data: formData,
        success: function(data) {
            console.log(data);
            console.log(typeof( data ));
            // Puedes manejar la respuesta del servidor aquí
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    });

}

function checklogin(event){
    var f = document.forms["loginform"].elements;
    var emptyFields = false;
    console.log(f.length);
    for (var i = 0; i < 2; i++) {
        console.log(f[i].value);
        if (f[i].value.trim() === "") {
            emptyFields = true;
            console.log("empty");
            break;
        }
    }

    if (emptyFields) {
        event.preventDefault();
        appendAlert('Hacen falta datos por rellenar', 'danger');
        hideAlertAfterDelay(10000);

    } else {
        console.log(f[0].value);
        console.log(f[1].value);
       if (f[0].value === "admin" && f[1].value === "admin") {
        console.log("entro");
        appendAlert('Bienvenido', 'success');
        hideAlertAfterDelay(10000); 
        setTimeout(() => {
        window.location.href = "index.html";
        }, 500);
       }
       else{
        appendAlert('Usuario o contraseña incorrectos', 'danger');
        hideAlertAfterDelay(5000); 
       }
    }
}

function searchUser() {
    var userId = {
        id: $('#userId').val(),
        form_id: 'form1'
    };
    
    $.ajax({
        url: '/usuarios.html',  // Adjust the URL according to your Flask server route
        type: 'POST',
        data: userId,
        success: function(data) {
            console.log(data);
            let plan = "";
            let dias = false;
            var userData = document.getElementById("userData");
            switch (data[0][11]) {
                case 1:
                    plan = "1 mes";
                    break;
                case 2:
                    plan = "2 meses";
                    break;
                case 3:
                    plan = "3 meses";
                    break;
                case 4: 
                    plan = "6 meses";
                    break;
                case 5:
                    plan = "10 dias";
                    dias = true;
                    break;
                case 6:
                    plan = "12 dias";
                    dias = true;
                    break;
                case 7:
                    plan = "15 dias";
                    dias = true;
                    break;
                case 8:
                    plan = "Otro";
                    break;
            }



            userData.innerHTML = "";
            userData.innerHTML = `
                <tr>
                    <td>${data[0][4]}</td>
                    <td>${data[0][1]} ${data[0][2]}</td>
                    <td>${data[0][5]}</td>
                    <td>${data[0][6]}</td>
                    <td>${data[0][7]}</td>
                    <td>${plan}</td>
                    <td>${data[0][13]}</td>
                </tr>
            `; 

            if (dias) {
                console.log("entro dias");
                userTable.innerHTML += `<th>Dias restantes</th>`;
                userData.innerHTML += `<td>${data[0][14]}</td>`;
                if(data[0][14]==0){
                    console.log("entro vencido por frecuencia");
                    userTable.innerHTML += `<th>Estado</th>`;    
                    userData.innerHTML += `<td>vencido</td>`;

                }else{
                    console.log("entro activo por frecuencia pero chequeo fecha")
                    checkdate();                  
                }
            }else{
                console.log("entro planes de meses y chequeo fechas");
                checkdate();
            }            
            var userTable = document.getElementById("userTable");
            userTable.style.display = "block";
            searchId = data[0][10];
        },
        error: function(status, error) { 
            console.error('Error:', error);
        }
    });
}

function checkdate(){
    var currentDate = new Date();
    var dataDate = new Date(data[0][13]);
    console.log(currentDate);
    console.log(dataDate);
    if (currentDate >= dataDate) {
        userTable.innerHTML += `<th>Estado</th>`;    
        userData.innerHTML += `<td>vencido</td>`;
        displaycontent();
    }else{
        userTable.innerHTML += `<th>Estado</th>`;    
        userData.innerHTML += `<td>activo</td>`;
    }    
}


function newEntry(){
    var userIdEntry = {
        id: $('#entryUser').val(),
    };
    console.log(userIdEntry);   
    $.ajax({
        url: '/index.html',  
        type: 'POST',
        data: userIdEntry,
        success: function(data) {
            console.log(data);
            console.log(typeof( data ));
        
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    })
}

function renewPlan(){
    var newPlan = {
        id: searchId,
        plan: $('#plan').val(),
        duracion: $('#duracion').val(),
        form_id: 'form2'
    };
    console.log(newPlan);   
    $.ajax({
        url: '/usuarios.html',  
        type: 'POST',
        data: newPlan,
        success: function(data) {
            console.log(data);
            console.log(typeof( data ));
        
        },
        error: function(xhr, status, error) {
            console.error('Error:', error);
        }
    })
}



function displaycontent(){
    var content = document.getElementById("renovar");
    content.style.display = "block";
}