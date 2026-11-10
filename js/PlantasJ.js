    //Salvavidas para hacer la implementacion en numeros del arbol. Esto es lo que se va a mandar con POST cuando el usuario eliga
    //una de estas opciones
    
    const mapeosValores = {
    estado: {
        "Aguascalientes": 1, "Baja California": 2, "Baja California Sur": 3, "Campeche": 4, "Chiapas": 5,
    "Chihuahua": 6, "CDMX": 7, "Coahuila": 8, "Colima": 9, "Durango": 10, "Guanajuato": 11,
    "Guerrero": 12, "Hidalgo": 13, "Jalisco": 14, "México": 15, "Michoacán": 16, "Morelos": 17,
    "Nayarit": 18, "Nuevo León": 19, "Oaxaca": 20, "Puebla": 21, "Querétaro": 22, "Quintana Roo": 23,
    "San Luis Potosí": 24, "Sinaloa": 25, "Sonora": 26, "Tabasco": 27, "Tamaulipas": 28, "Tlaxcala": 29,
    "Veracruz": 30, "Yucatán": 31, "Zacatecas": 32
    },

    forma: {
        "Arbustivo (Plantas leñosas que pueden tener varios metros de altura)": 1,
        "Herbácea (Plantas que no forman leño o madera)": 2,
        "Arboreo (Árboles)": 3
    },
    herbacea: {
        "Trepadora (Plantas que se encaraman a un elemento como un muro, espaldera, etc)": 1,
        "Enredadera (Plantas con tallos delgados que necesita un soporte para trepar.)": 2,
        "Postrada (Plantas con tallos que se apoyan sobre el suelo.)": 3
    },
    fruta: {
        "Sí": 1,
        "No": 2
    },
    hoja: {
        "Sí": 1,
        "No": 2
    },
    uso: {
        "Medicinal": 1,
        "Ornamento": 2,
        "Forraje": 3
    },
    cflor: {
        "Amarillo": 1, "Azul": 2, "Blanco": 3, "Lila": 4, "Morado": 5,
        "Naranja": 6, "Rojo": 7, "Rosa": 8, "Verde": 9, "Cualquier Color": 0
    },
    heladas: {
        "Si": 1,
        "No": 2,
        "Ligeras": 3
    },
    riego: {
        "Abundante (Se riegan diariamente)": 1,
        "Moderado (Se riegan cada 3 o 4 días)": 2,
        "Bajo (Se riegan una vez a la semana)": 3
    },
    sol: {
        "Sol": 1,
        "Sombra": 2
    },
    velocidad: {
        "Lento (En más de 1 se llega a la etapa adulta)": 1,
        "Moderado (En menos de 1 año se llega a la etapa adulta)": 2,
        "Rapido (En menos de 6 meses se llega a la etapa adulta)": 3
    },
    phCond: {
        "Sí": 1,
        "No": 2
    },
    suelo: {
        "Arcilloso": 1,
        "Arenoso": 2,
        "Franco": 3,
        "Francoarenoso": 4,
        "Limoso": 5,
        "Pantanoso": 6,
        "Pedregoso": 7
    },
    CMO: {
        "Rico": 1,
        "Moderado": 2,
        "Pobre": 3
    }
};

    
    //Aqui se declaran las preguntas y su contenido
    const questions = [    
        //Pregunta 1 Estado
        {
        id: "estado",
        texto: "Selecciona el estado en el que vives",
        tipo: "desplegable", // tipo de pregunta: select, desplegable, texto u opciones (Talvez una combinacion de ellas, talvez), opciones es para las de si o no. 
        opciones: [
            "Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
            "Coahuila", "Colima", "Chiapas", "Chihuahua", "CDMX", "Durango", 
            "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "México", "Michoacán",
            "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", 
            "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", 
            "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
            ]

       },
        //Pregunta 2 Forma
       {
        id: "forma",
        texto: "¿Que tipo de plata prefieres?",
        tipo: "select",
        opciones: ["Arbustivo (Plantas leñosas que pueden tener varios metros de altura)","Herbácea (Plantas que no forman leño o madera)", "Arboreo (Árboles)" ]
       },

       //Pregunta 2.1 Tipo de Herbacea, solo si selecciona herbacea en la pasada
       {
        id: "herbacea",
        texto: "¿Qué tipo de herbácea prefieres?",
        tipo: "select",
        opciones: ["Trepadora (Plantas que se encaraman a un elemento como un muro, espaldera, etc)" ,"Enredadera (Plantas con tallos delgados que necesita un soporte para trepar.)", "Postrada (Plantas con tallos que se apoyan sobre el suelo.)"],
        //Entra condicional para que la pregunta  solo aparezca si se selecciono herbacea en 2.1
          condicional: {
            dependeDe: "forma",
            valor: "Herbácea (Plantas que no forman leño o madera)"
        }
        },

        //Pregunta 3 Area Minima
        {
            id: "amin",
            texto: "¿Cuál es el área que deseas destinar (en metros cuadrados)?",
            tipo: "texto"
        },
        
        //Pregunta 4 Frutas
        {
            id: "fruta",
            texto: "¿Quieres que la planta dé frutos comestibles?",
            tipo: "opciones",
            opciones: ["Sí", "No"]
        },

        //Pregunta 5 Hojas
        {
            id: "hoja",
            texto: "¿Prefiere hojas todo el año?",
            tipo: "opciones",
            opciones: ["Sí", "No"]
        },

        //Pregunta 6 Uso
        {
            id:"uso",
            texto: "¿Qué uso desea que tenga la planta?",
            tipo: "select",
            opciones:["Medicinal", "Ornamento", "Forraje"]
        },

        //Pregunta 7 Color de flor
        {
            id: "cflor",
            texto: "¿Qué color de flor desea?", 
            tipo: "select",
            opciones:["Amarillo", "Azul", "Blanco", "Lila", "Morado", "Naranja", "Rojo", "Rosa", "Verde", "Cualquier Color"]
        },


        //Pregunta 8 Altura
        {
            id: "altura",
            texto: "Ingrese la altura que le gustaria que tuviera (en metros)",
            tipo: "texto",
        },

        //Pregunta 9 Temperatura
        {
            id: "temp",
            texto: "Elija la temperatura promedio de su zona (en °C):",
            tipo: "texto"
        },
        
        //Pregunta 10 HHeladas

        {
            id: "heladas",
            texto: "¿Suele haber heladas?",
            tipo: "select",
            opciones: ["Si", "No", "Ligeras"] 
        },


        //Pregunta 11 RIEGO
        {
            id: "riego",
            texto: "Frecuencia de Riego Deseada",
            tipo: "select",
            opciones: ["Abundante (Se riegan diariamente)","Moderado (Se riegan cada 3 o 4 días)","Bajo (Se riegan una vez a la semana)"]
        },

        //Pregunta 12 Insolacion
        {
            id: "sol",
            texto: "¿Sol o Sombra?",
            tipo: "select",
            opciones:["Sol","Sombra"]
        },

        //Pregunta 13 Velocidad de Crecimiento
        {
            id:"velocidad",
            texto: "¿Que tan rapido quieres que crezca",
            tipo: "select",
            opciones: ["Lento (En más de 1 se llega a la etapa adulta)","Moderado (En menos de 1 año se llega a la etapa adulta)","Rapido (En menos de 6 meses se llega a la etapa adulta)"]
        },

        //Pregunta 14 Ph

    {
        id:"phCond",
        texto: "¿Conoce el PH?",
        tipo: "opciones",
        opciones: ["Sí", "No"]
    },

    //14.1 PH si si lo conoce
    {
        id: "ph",
        texto: "¿Cuál es el pH?",
        tipo: "texto",
         condicional: {
            dependeDe: "phCond",
            valor: "Sí"
        }
    },

    //15 Suelo
        {
            id:"suelo",
            texto:"Seleccione el Tipo de Suelo",
            tipo: "select",
            opciones:["Arcilloso", "Arenoso", "Franco", "Francoarenoso", "Limoso", "Pantanoso", "Pedregoso"]
        },

    //16 CMO
        {
            id: "CMO",
            texto:"Cantidad de materia orgánica",
            tipo: "select",
            opciones: ["Rico", "Moderado", "Pobre"]
        }
    ]
    

const startBtn = document.getElementById('startBtn');
const questionsSection = document.getElementById('questionsSection');
const resultsSection = document.getElementById('resultsSection');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const restartBtn = document.getElementById('restartBtn');
const shareBtn = document.getElementById('shareBtn');
const questionsContainer = document.getElementById('questionsContainer');

let currentQuestionIndex = 0;
let userAnswers = {};
let questionHistory = [];  // Guarda el historial de preguntas mostradas (Resuelve prevbtn)


// Oculta seccion de preguntas y resultado
document.addEventListener('DOMContentLoaded', function() {
    questionsSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
});

startBtn.addEventListener('click', function() {
    questionsSection.classList.remove('hidden');
    renderQuestion();
    questionsSection.scrollIntoView({ behavior: 'smooth' });
});

prevBtn.addEventListener('click', function() {
    if (questionHistory.length > 0) {
        currentQuestionIndex = questionHistory.pop();  // Volver al último índice mostrado
        renderQuestion();
    }
});


nextBtn.addEventListener('click', function() {
    if (currentQuestionIndex < questions.length - 1) {
        questionHistory.push(currentQuestionIndex);  // Guarda historial antes de avanzar
        currentQuestionIndex++;
        renderQuestion();
    } else {
        showResults();
    }
});


restartBtn.addEventListener('click', function() {
    currentQuestionIndex = 0;
    //Borra las respuestas que se hayan guardado
    userAnswers = {};
    //Esconde la pantalla de exito
    resultsSection.classList.add('hidden');
    questionsSection.classList.remove('hidden');
    renderQuestion();
    questionsSection.scrollIntoView({ behavior: 'smooth' });
});


shareBtn.addEventListener('click', function() {
        // Compartir (Lo hace el navegador)
        if (navigator.share) {
            navigator.share({
                title: 'Especies compatibles para mi jardín',
                text: 'Consulta especies compatibles con las condiciones de tu jardín',
                url: window.location.href
        // El window.location.href es porque aun no tenemos url en internet bien
            });
        } else {
            // Catch para navegador incompatible al API del comparti
            // Basicamente copia el link del resultado 
            if (navigator.clipboard) {
                navigator.clipboard.writeText(window.location.href);
                alert('¡Enlace copiado al portapapeles!');
            } else {
                alert('Comparte este enlace: ' + window.location.href);
            }
        }
    });

//Funcion que muestra preguntas y opciones
function renderQuestion() {
    const question = questions[currentQuestionIndex];

    // Verifica condiciones si la pregunta es condicional (Tippo herbacia o ph)
    if (question.condicional) {
        const { dependeDe, valor } = question.condicional;
        const respuestaPadre = userAnswers[dependeDe];
        const valorEsperado = mapeosValores[dependeDe]?.[valor] || valor;

        if (respuestaPadre !== valorEsperado) {
            currentQuestionIndex++;
            if (currentQuestionIndex < questions.length) {
                renderQuestion();
            } else {
                showResults();
            }
            return;
        }
    }

    // Limpiar contenedor de pregunta
    questionsContainer.innerHTML = '';

    // Acomoda visualmente el titulo de pregunta
    const questionBox = document.createElement('div');
    questionBox.className = 'question-box';

    const questionTitle = document.createElement('h4');
    questionTitle.className = 'question-title';
    questionTitle.textContent = question.texto;
    questionBox.appendChild(questionTitle);

    // Entrada tipo text
    if (question.tipo === 'texto') {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'text-input';
        input.value = userAnswers[question.id] || '';
        input.oninput = (e) => {
            const val = e.target.value;
            const num = val.includes('.') ? parseFloat(val) : parseInt(val);
            userAnswers[question.id] = isNaN(num) ? val : num;
        };

        const inputWrapper = document.createElement('div');
        inputWrapper.className = 'input-wrapper';
        inputWrapper.appendChild(input);
        questionBox.appendChild(inputWrapper);
    }

    // Entrada tipo desplegable (Estados de la preg 1)
    else if (question.tipo === "desplegable") {
        const select = document.createElement("select");
        select.classList.add("dropdown-select");

        const defaultOption = document.createElement("option");
        defaultOption.disabled = true;
        defaultOption.selected = true;
        defaultOption.textContent = "Selecciona una opción";
        select.appendChild(defaultOption);

        question.opciones.forEach((opcion) => {
            const opt = document.createElement("option");
            opt.value = opcion;
            opt.textContent = opcion;
            select.appendChild(opt);
        });

        if (userAnswers[question.id]) {
            select.value = userAnswers[question.id];
        }

        select.addEventListener("change", () => {
            if (mapeosValores[question.id]) {
                userAnswers[question.id] = mapeosValores[question.id][select.value];
            } else {
                userAnswers[question.id] = select.value;
            }
        });

        questionBox.appendChild(select);
    }

    // Opciones tipo botón
    else if (question.tipo === 'select' || question.tipo === 'opciones') {
        const opcionesWrapper = document.createElement('div');
        opcionesWrapper.className = 'opciones-wrapper';

        question.opciones.forEach(opcion => {
            const btn = document.createElement('button');
            btn.textContent = opcion;
            btn.className = 'btn-option';
            btn.onclick = () => {
                if (mapeosValores[question.id]) {
                    userAnswers[question.id] = mapeosValores[question.id][opcion];
                } else {
                    userAnswers[question.id] = opcion;
                }
                nextBtn.click();
            };
            opcionesWrapper.appendChild(btn);
        });

        questionBox.appendChild(opcionesWrapper);
    }

    questionsContainer.appendChild(questionBox);

    // Actualizar progreso
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
    document.getElementById('progressBar').style.width = progress + '%';
    document.getElementById('questionCounter').textContent = 'Pregunta ' + (currentQuestionIndex + 1) + ' de ' + questions.length;
    prevBtn.disabled = currentQuestionIndex === 0;
    nextBtn.textContent = currentQuestionIndex === questions.length - 1 ? 'Ver Resultado' : 'Siguiente →';
}


function showResults() {
    questionsSection.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth' });
    enviarRespuestasAlBackend();
}

function enviarRespuestasAlBackend() {
    // Lifesaver por dato int o double en vez de float en los cuadros de texto
    const camposNumericos = ["amin", "altura", "temp", "ph"];
    camposNumericos.forEach((campo) => {
        if (userAnswers.hasOwnProperty(campo)) {
            const val = userAnswers[campo];
            if (typeof val === "string") {
                userAnswers[campo] = parseFloat(val.replace(',', '.'));
            }
        }
    });
//Parte escencial, manda a app.py las respuestas recolectadas 
    fetch('/procesar_respuestas', {
        method: 'POST',    
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userAnswers)
    })
    .then(response => response.json())
    .then(data => {
        mostrarResultado(data); // Función para mostrar el resultado
    })
    .catch(error => {
        console.error('Error al enviar respuestas:', error);
    });
}

function mostrarResultado(data) {
    const container = document.getElementById('resultsContainer');
    container.replaceChildren();
    if (data.error) {
        const p = document.createElement('p');
        p.textContent = data.error;
        container.appendChild(p);
        return;
    }
    if (!Array.isArray(data.preferidas) || !Array.isArray(data.alternativas)) {
        container.textContent = 'No fue posible interpretar los resultados del servidor.';
        return;
    }
    const total = data.preferidas.length + data.alternativas.length;
    const resumen = document.createElement('p');
    resumen.textContent = `Se encontraron ${total} especies ambientalmente compatibles.`;
    container.appendChild(resumen);
    if (total === 0) {
        const aviso = document.createElement('p');
        aviso.textContent = 'No se encontraron especies compatibles con las condiciones ambientales. Intenta modificar tus respuestas.';
        container.appendChild(aviso);
        return;
    }
    function grupo(titulo, especies) {
        const seccion = document.createElement('section');
        const encabezado = document.createElement('h4');
        encabezado.textContent = `${titulo} (${especies.length})`;
        seccion.appendChild(encabezado);
        const listado = document.createElement('div');
        listado.className = 'resultados-lista';
        if (especies.length === 0) {
            const aviso = document.createElement('p');
            aviso.textContent = 'No hay especies en este grupo.';
            listado.appendChild(aviso);
        }
        especies.forEach(especie => {
            const tarjeta = document.createElement('article');
            tarjeta.className = 'resultado-especie';
            const nombre = document.createElement('h4');
            nombre.textContent = especie.especie || 'Especie sin nombre';
            tarjeta.appendChild(nombre);
            if (typeof especie.foto === 'string' && especie.foto.trim()) {
                const img = document.createElement('img');
                img.src = especie.foto.replace(/&amp;/g, '&');
                img.alt = `Infografía de ${especie.especie || 'la especie'}`;
                img.className = 'resultado-imagen';
                img.loading = 'lazy';
                tarjeta.appendChild(img);
            }
            listado.appendChild(tarjeta);
        });
        seccion.appendChild(listado);
        container.appendChild(seccion);
    }
    grupo('Compatibles que cumplen todas tus preferencias', data.preferidas);
    grupo('Otras especies ambientalmente compatibles', data.alternativas);
}
