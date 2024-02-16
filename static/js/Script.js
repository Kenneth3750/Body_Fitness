// ajax function to load a user to database
let tope = 6;
let searchId;
let cedula_ver_mas;
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
            appendAlert('Nuevo usuario registrado exitosamente', 'success');
            hideAlertAfterDelay(10000); 
            setTimeout(() => {
            window.location.reload();
            }, 5000);
            // Puedes manejar la respuesta del servidor aquí
        },
        error: function(xhr, status, error) {
            console.error('Error:', xhr.status);
            console.error("Error en la base de datos: ", error);
            if (xhr.status === 493) {
                appendAlert('La cédula ya se encuentra registrada', 'danger');
                hideAlertAfterDelay(10000);
            }else{
                appendAlert('Error en la base de datos', 'danger');
                hideAlertAfterDelay(10000);
            }
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

function table_data_Users(data) {

    console.log(data);
    var userData = document.getElementById("userData");
    userData.innerHTML = "";
    userHead.innerHTML = `
        <tr>
            <th>Cedula</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Telefono</th>
            <th>Direccion</th>
            <th>Plan</th>
            <th>Válido desde</th>
            <th>Válido hasta</th>
            <th>Estado</th>
            <th>Dias restantes</th>
            <th>Último ingreso</th>
            <th>Pago</th>
        </tr>       
        `;

    console.log(`este es el datalengh ${data.length}`);
    for (let i = 0; i < data.length; i++) {
        let plan = "";
        let dias = false;     
        switch (data[i][11]) {
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

        
        var datafecha = new Date(data[i][13]);
        var datafechap = new Date(data[i][12]);
        var ultimoIngreso = new Date(data[i][17]);
        console.log(`el data solo sin pasarlo por Date es ${data[i][12]}`)
        console.log(`este es el year datafecha ${datafecha.getFullYear()}`);
        console.log(`este es el year datafechap del plan ${i+1} ${datafechap.getFullYear()}`);

        
        if (dias) {
            console.log("entro dias");
            dias_rest = data[i][14];
            if(data[i][14]==0){
                console.log("entro vencido por frecuencia");
                plan_state = "vencido";
                if(i==0){
                    displaycontent();
                }
                

            }else{
                console.log("entro activo por frecuencia pero chequeo fecha")
                checkdate(data[i][13],i);                  
            }
        }else{
            console.log("entro planes de meses y chequeo fechas");
            checkdate(data[i][13],i);
            dias_rest = "N/A";
        } 
        function dias2(dias){
            num_dia=parseInt(dias);   
            if(num_dia<10){
                num_dia="0"+num_dia;
            } 
            return num_dia;
        }
        
        userData.innerHTML += `
            <tr>
                <td>${data[i][4]}</td>
                <td>${data[i][1]} ${data[i][2]}</td>
                <td>${data[i][5]}</td>
                <td>${data[i][6]}</td>
                <td>${data[i][7]}</td>
                <td>${plan}</td>
                <td>${datafechap.getFullYear()}-${mes(datafechap.getMonth())}-${dias2(datafechap.getDate())}</td>
                <td>${datafecha.getFullYear()}-${mes(datafecha.getMonth())}-${dias2(datafecha.getDate())}</td>
                <td>${plan_state}</td>
                <td>${dias_rest}</td>
                <td>${ultimoIngreso.getFullYear()}-${mes(ultimoIngreso.getMonth())}-${dias2(ultimoIngreso.getDate())}</td>
                <td>${data[i][16]} <button class="btn" onclick="confirmPayment()"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check-circle-fill" viewBox="0 0 16 16">
                <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"style="fill: #66a324;"/>
              </svg></button> </td>
            </tr>

        `; 
        

                
        var userTable = document.getElementById("userTable");
        userTable.style.display = "block";
        searchId = data[i][10];
    }
    
        var numLines = document.getElementById('userData').getElementsByTagName('tr').length;
        document.getElementById('num_elementos').innerHTML = `Número de elementos: ${numLines}`;
        var numPages = Math.ceil(numLines / 10);
        console.log('Num pages es ' + numPages);
        console.log('numlines es ' + numLines);

        var userTabs = document.getElementById('userTabs');
        if (numPages == 1) {
            // Remove additional pages
            var userTabContent = document.getElementById('userTabContent');
            var pageDivs = userTabContent.getElementsByClassName('tab-pane');
            while (pageDivs.length > 1) {
                userTabContent.removeChild(pageDivs[1]);
            }
            // Remove page links
            var userTabs = document.getElementById('userTabs');
            var pageLinks = userTabs.getElementsByClassName('nav-link');
            while (pageLinks.length > 1) {
                userTabs.removeChild(pageLinks[1]);
            }
        } else {
            for (var i = 2; i <= numPages; i++) {
                var pageLink = document.createElement('a');
                pageLink.classList.add('nav-link');
                pageLink.setAttribute('data-bs-toggle', 'tab');
                pageLink.href = '#page' + i;
                pageLink.textContent = 'Página ' + i;
                userTabs.appendChild(pageLink);
            }

            // Create additional pages
            var userTabContent = document.getElementById('userTabContent');
            for (var i = 2; i <= numPages; i++) {
                var pageDiv = document.createElement('div');
                pageDiv.classList.add('tab-pane', 'fade');
                pageDiv.id = 'page' + i;
                var table = document.createElement('table');
                table.classList.add('table', 'table-light', 'table-striped');
                var tbody = document.createElement('tbody');
                tbody.classList.add('table-group-divider');
                table.appendChild(tbody);
                pageDiv.appendChild(table);
                userTabContent.appendChild(pageDiv);
            }

            // Move data to additional pages
            var userData = document.getElementById('userData');
            var rows = Array.from(userData.getElementsByTagName('tr')); // Convert to array
            for (var i = 0; i < rows.length; i++) {
                var pageIndex = Math.ceil((i + 1) / 10);
                var pageTable = document.getElementById('page' + pageIndex).getElementsByTagName('tbody')[0];
                pageTable.appendChild(rows[i]);
            }

            // Clone the table header for each page
            var tableHeader = document.getElementById('userHead');
            var userTabContent = document.getElementById('userTabContent');
            var pageDivs = userTabContent.getElementsByClassName('tab-pane');
            for (var i = 1; i < pageDivs.length; i++) {
                var pageTable = pageDivs[i].getElementsByTagName('table')[0];
                var clonedHeader = tableHeader.cloneNode(true);
                pageTable.insertBefore(clonedHeader, pageTable.firstChild);
            }
        }

}



function searchUser(event) {
    event.preventDefault();
    var userId = {
        id: $('#userId').val(),
        form_id: 'form1'
    };
    
    $.ajax({
        url: '/usuarios.html',  // Adjust the URL according to your Flask server route
        type: 'POST',
        data: userId,
        success: function(data){
            console.log(data);
            console.log(data.length);
            if(data.length==0){
                appendAlert('Usuario no registrado', 'danger');
                hideAlertAfterDelay(5000);
            }else{
                table_data_Users(data);
                document.getElementById("tabla_titulo").innerHTML = "Datos del usuario";
            }
        },
        
        error: function(status, error) { 
            appendAlert('Usuario no registrado', 'danger');
            hideAlertAfterDelay(5000); 
            console.log('Error:', error);
        }
    });
}
function mes(mes){
    num_mes=parseInt(mes)+1;   
    if(num_mes<10){
        num_mes="0"+num_mes;
    } 
    return num_mes;
}

function dias(dias){
    num_dia=parseInt(dias);   
    if(num_dia<10){
        num_dia="0"+num_dia;
    } 
    return num_dia;
}
function checkdate(data,i){
    var currentDate = new Date();
    var dataDate = new Date(data);
    console.log(currentDate);
    console.log(dataDate);
    if (currentDate >= dataDate) {
        plan_state = "vencido";
        if(i==0){
            displaycontent();
        }  
    }else{
        plan_state = "activo";
    }    
}


function newEntry(event){
    event.preventDefault();
    var userIdEntry = {
        id: $('#entryUser').val(),
        form_id: 'form4'
    };
    console.log(userIdEntry);   
    $.ajax({
        url: '/index.html',  
        type: 'POST',
        data: userIdEntry,
        success: function(data) {
            console.log(data);
            console.log(typeof( data ));
            var contenido= "";
            if(data.length==0){
                contenido = "Usuario no registrado";
                appendAlert2(contenido, 'danger');
                hideAlertAfterDelay(10000);
            }else{
                if(data[0][2]==null){
                    var currentDate = new Date();
                    var dataDate = new Date(data[0][3]);
                    if (currentDate >= dataDate) {
                        appendAlert2("Su plan se encuentra vencido", 'danger');
                        hideAlertAfterDelay(10000);
                    }
                    else{
                        var diff = Math.abs(currentDate - dataDate);
                        contenido = `Bienvenido(a) ${data[0][0]} ${data[0][1]}, Tiempo restante: ${Math.ceil(diff / (1000 * 60 * 60 * 24))} dias`;           
                    }           
                }else{
                    if(data[0][2]==0){
                        appendAlert2("Su plan se encuentra vencido", 'danger');
                        hideAlertAfterDelay(10000);
                    }else{
                        var dataDate = new Date(data[0][3]);
                        contenido = `Bienvenido(a) ${data[0][0]} ${data[0][1]}, Tiempo restante: ${data[0][2]} dias hasta el ${dataDate.getFullYear()}-${mes(dataDate.getMonth())}-${dias(dataDate.getDate())} `;
                    }
                }
                if(contenido!=""){
                    appendAlert2(contenido, 'success');
                    hideAlertAfterDelay(10000);
                }
                
            }
            document.getElementById("entryUser").value = "";
        
        },
        error: function(xhr, status, error) { 
            appendAlert2('Usuario no registrado', 'danger');
            hideAlertAfterDelay(10000);
            console.error('Error:', error);
            document.getElementById("entryUser").value = "";
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
            appendAlert('Usuario registrado correctamente', 'success');
            hideAlertAfterDelay(3000);
            var content = document.getElementById("renovar");
            content.style.display = "none";   
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


function proxusers(){
    document.getElementById("entryUser").focus();
    


    data_form = {
        form_id: 'form3'
    };
    
    $.ajax({
        url: '/index.html',
        type: 'POST',
        data: data_form,
        success: function(data){
            console.log(data);
            console.log(data.length);
            if(data.length==0){
                var proxuserTitle = document.getElementById("proxtitle");
                proxuserTitle.innerHTML = "No hay usuarios proximos a vencer";
            }else{
                document.getElementById("proxtable").style.display = "block";
                var proxuserData = document.getElementById("proxusers");
            
                proxuserData.innerHTML = "";
                for(let i=0; i<data.length; i++){
                    var dataDate = new Date(data[i][3]);
                    let fechaexact = `${dataDate.getFullYear()}-${mes(dataDate.getMonth())}-${dias(dataDate.getDate())}`
                    if(data[i][4]==null){
                        dias_rest = "N/A"
                    }else{
                        dias_rest = data[i][4]
                    }

                    proxuserData.innerHTML += `
                    <tr>
                        <td>${data[i][0]} ${data[i][1]}</td>
                        <td>${data[i][2]}</td>
                        <td>${fechaexact}</td>
                        <td>${dias_rest}</td>
                        <th> <button class="btn" onclick="vermasfn(${data[i][2]})"> <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3z " style="fill: #18317d;"/>
                    </svg></button></th>
                    </tr>
                    `
                }
        }
        }, 
        error: function(xhr, status, error){
            console.error('Error:', error);
        }
    })
    

}
function vermasfn(cedula){
    console.log("entro ver mas fn");
    localStorage.setItem('ver_mas', true);
    localStorage.setItem('cedula_ver_mas', cedula);
    window.location.href="usuarios.html";
}

function check_ver_mas(){
    
    let vermas = localStorage.getItem('ver_mas');
    let cedula_ver_mas = localStorage.getItem('cedula_ver_mas');
    console.log("entro check ver mas");
    console.log('vermas '+ vermas);
    console.log(cedula_ver_mas);
    if (vermas == "true"){
        console.log("entro ver mas");
        document.getElementById("userId").value = cedula_ver_mas;
        localStorage.setItem('ver_mas', false);
        searchUser(event);

    }else{
        console.log("no entro ver mas por tanto muestro usuarios activos");
        usuarios_activos();
    }
}

function usuarios_activos(){
    data = {
        form_id: 'defaultForm'
    };
   
    $.ajax({
        url: '/usuarios.html',
        type: 'POST',
        data: data,
        success: function(response){
            console.log(response);
            console.log(response.length);
            if(response.length==0){
                appendAlert('no hay usuarios en la base de datos', 'danger');
                hideAlertAfterDelay(5000);
            }else{
                table_data_Users(response);
                document.getElementById("tabla_titulo").innerHTML = "Usuarios activos";
                document.getElementById("renovar").style.display = "none";
            }
        },
        error: function(xhr, status, error){
            console.error('Error:', error);
        }
    });
}
function appendAlert2(message, type) {
    const alertPlaceholder = document.getElementById('liveAlertPlaceholder');
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
        <div class="alert alert-${type} alert-dismissible" role="alert">
            <div>
            <h1>${message}</h1>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" onclick="window.location.reload();" aria-label="Close"></button>
        </div>
    `;
    alertPlaceholder.append(wrapper);
}


function confirmPayment(user_id, start_plan){
    data = {
        form_id: 'formPay',
        user: user_id,
        start_plan_date: start_plan
    }

    $.ajax({
        url: '/usuarios.html',
        type: 'POST',
        data: data,
        success: function(response){
            console.log(response);
            appendAlert('Pago confirmado', 'success');
            hideAlertAfterDelay(5000);
        },
        error: function(xhr, status, error){
            console.error('Error:', error);
        }   
    })
}