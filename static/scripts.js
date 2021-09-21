function mostrarHTML(ruta) {
    // Creamos el objeto para la solicitud al servidor
    let request = new XMLHttpRequest();

    // Abrimos la conexion con la ruta que buscamos (cada boton representa una ruta)
    request.open('GET', ruta);

    // Enviamos la solicitud al servidor
    request.send();

    // Verificamos el estado de nuestra solicitud
    // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/readyState

    // Esto se activa con cada cambio de estado
    request.onreadystatechange = function () {
        // this hace referencia a request
        // El 4 es el estado que refleja que la operacion se completo
        if (this.readyState == 4) {
            // El codigo de respuesta ya sea 200 ok, 400, 404, 500 etc.
            let codigo = this.status;

            // Respuesta del servidor, nosotros esperamos codigo HTML
            let respuesta = this.responseText;

            if (codigo == 200) {
                // Obtenemos el div del contenido
                let contenido = document.getElementById("contenido-cambiable");
                contenido.innerHTML = respuesta;
                return false;
            } else if (codigo == 500) {
                // Aca mostramos errores 
                alert('Hay un problema con el servidor');
                return false;
            }

        }
    }
}

function agregar(formulario) {
    // Creamos un formulario para enviar los datos en base al que habia en el HTML
    let datos = new FormData(formulario);

    // Hacemos la solicitud al servidor igual que en mostrarHTML
    let request = new XMLHttpRequest();
    request.open('POST', '/agregar');

    // Aca el cambio es que se envia el formulario que creamos previamente
    request.send(datos);

    // aca esperamos la respuesta del servidor
    request.onreadystatechange = function () {
        if (this.readyState == 4) {
            // El codigo de respuesta
            let codigo = this.status;

            // Respuesta del servidor, nosotros esperamos codigo HTML
            let respuesta = this.responseText;

            if (codigo == 200) {
                alert('Agregado');

                // Obtenemos el div del contenido
                let contenido = document.getElementById("contenido-cambiable");
                contenido.innerHTML = respuesta;
                return false;
            } else if (codigo == 500) {
                // Aca mostramos errores 
                alert('Hay un problema con el servidor');
                return false;
            }

        }
    };
}

// Uso de json
function buscar(valor) {
    // Buscamos el contenedor 
    let container = document.getElementById('resultados');
    // limpicamos
    container.textContent = "";

    // Ya que no tenemos un formulario base creamos nosotros el campo 
    let datos = new FormData();
    datos.append("q", valor);

    let request = new XMLHttpRequest();
    request.responseType = 'json';
    request.open('POST', '/buscar');
    request.send(datos);



    // Esta vez esperamos un json

    request.onreadystatechange = function () {

        if (this.readyState == 4) {
        

            // El codigo de respuesta
            let codigo = this.status;

            // Respuesta del servidor, nosotros esperamos codigo HTML
            let respuesta = this.response;

            console.log(respuesta);

            // respuesta = JSON.parse(respuesta);

            if (codigo != 200) {
                return false;
            }

            // Cuando no hay resultados
            if (respuesta.items_counter == 0) {
                container.textContent = "No hay resultados";
                return false;
            } else {
                container.innerHTML = "";
                for (var i = 0; i < respuesta.items_counter; i++) {

                    // Item guarda cada diccionario temporal que se hizo en el app.py
                    let item = respuesta.items[i];

                    // div class row (ver resultados.html)
                    let row = document.createElement('div');
                    row.setAttribute('class', 'row');
                    row.setAttribute('style', 'margin-top: 50px;');

                    //div class card
                    let card = document.createElement('div');
                    card.setAttribute('class', 'card');
                    card.setAttribute('style', 'width: 18rem;');

                    // imagen
                    let img = document.createElement('img');
                    img.setAttribute('src', item.image);
                    img.setAttribute('class', 'card-img-top');

                    // div class card body
                    let card_body = document.createElement('div');
                    card_body.setAttribute('class', 'card_body');

                    // h5
                    let h5 = document.createElement('h5');
                    h5.setAttribute('class', 'card-title');
                    h5.innerHTML = item.name + ' <b>' + item.year + '</b>' + '<hr>';

                    // parrafo
                    let pa = document.createElement('p');
                    pa.setAttribute('class', 'card-text');
                    pa.textContent = item.description;

                    //ahora vamos a meter elemento dentro de elemento

                    // Lo que va dentro del body card
                    card_body.appendChild(h5);
                    card_body.appendChild(pa);

                    // Lo que va dentro del card
                    card.appendChild(img);
                    card.appendChild(card_body);

                    // Card dentro de row
                    row.appendChild(card);

                    // Agregar el item al container
                    container.appendChild(row);


                }
            }





            return false;
        }





    }
}

function actualizar(form) {
    let datos = new FormData(form);

    let request = new XMLHttpRequest();
    request.open('POST', '/actualizar');
    request.send(datos);

    request.onreadystatechange = function () {
        if (this.readyState == 4) {
            let respuesta = this.responseText;

            // Obtenemos el div del contenido
            let contenido = document.getElementById("contenido-cambiable");
            contenido.innerHTML = respuesta;


        }
    }

}

function guardar_actual(form) {
    let datos = new FormData(form);

    let request = new XMLHttpRequest();
    request.open('POST', '/actualizador');
    request.send(datos);

    request.onreadystatechange = function () {
        if (this.readyState == 4) {
            if (this.status == 200) {
                alert('Editado');
                let respuesta = this.responseText;
                // Obtenemos el div del contenido
                let contenido = document.getElementById("contenido-cambiable");
                contenido.innerHTML = respuesta;

            }
            return false;
        }
    }
}


function eliminar(form) {
    let datos = new FormData(form);
    let request = new XMLHttpRequest();
    request.open('POST', '/eliminar');
    request.send(datos);

    request.onreadystatechange = function () {
        if(this.readyState == 4){
            if(this.status == 200){
                alert('eliminado');
                let respuesta = this.responseText;
                // Obtenemos el div del contenido
                let contenido = document.getElementById("contenido-cambiable");
                contenido.innerHTML = respuesta;
            }
        }
    }
}