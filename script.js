// ============================================
// IMAGE PREVIEW
// ============================================

const plantImage =
    document.getElementById("plantImage");

const imagePreview =
    document.getElementById("imagePreview");

const previewContainer =
    document.getElementById("previewContainer");


plantImage.addEventListener(
    "change",
    function () {

        const file = this.files[0];

        if (!file) {
            previewContainer.style.display = "none";
            return;
        }

        const reader =
            new FileReader();

        reader.onload = function (event) {

            imagePreview.src =
                event.target.result;

            previewContainer.style.display =
                "block";
        };

        reader.readAsDataURL(file);
    }
);


// ============================================
// PLANT ANALYSIS
// ============================================

const analysisForm =
    document.getElementById("analysisForm");


analysisForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        const button =
            document.querySelector(".analyze-button");

        button.disabled = true;

        button.innerText =
            "🔬 Analyzing...";


        const formData =
            new FormData(this);


        try {

            const response =
                await fetch(
                    "/analyze",
                    {
                        method: "POST",
                        body: formData
                    }
                );


            const data =
                await response.json();


            if (!data.success) {

                alert(
                    data.message ||
                    "Something went wrong."
                );

                return;
            }


            showAnalysisResult(data);


        } catch (error) {

            console.error(error);

            alert(
                "Unable to connect to Python server."
            );

        } finally {

            button.disabled = false;

            button.innerText =
                "🔬 Analyze Plant";
        }

    }
);


// ============================================
// DISPLAY RESULT
// ============================================

function showAnalysisResult(data) {

    document.getElementById(
        "emptyResult"
    ).style.display = "none";


    document.getElementById(
        "resultContent"
    ).style.display = "block";


    document.getElementById(
        "resultImage"
    ).src = data.image_url;


    document.getElementById(
        "healthScore"
    ).innerText =
        data.health_score + "%";


    document.getElementById(
        "scoreBar"
    ).style.width =
        data.health_score + "%";


    const plant =
        data.plant;


    document.getElementById(
        "resultPlant"
    ).innerText =
        plant.icon + " " + plant.name;


    document.getElementById(
        "resultDescription"
    ).innerText =
        plant.description;


    document.getElementById(
        "scientificName"
    ).innerText =
        plant.scientific;


    document.getElementById(
        "resultSoil"
    ).innerText =
        plant.soil;


    document.getElementById(
        "resultWater"
    ).innerText =
        plant.water;


    document.getElementById(
        "resultSun"
    ).innerText =
        plant.sun;


    const disease =
        data.disease;


    document.getElementById(
        "resultDisease"
    ).innerText =
        disease.name;


    document.getElementById(
        "diseaseSymptoms"
    ).innerHTML =
        "<b>Symptoms:</b> " +
        disease.symptoms;


    document.getElementById(
        "diseaseCause"
    ).innerHTML =
        "<b>Possible cause:</b> " +
        disease.causes;


    document.getElementById(
        "diseaseCare"
    ).innerHTML =
        "<b>Care:</b> " +
        disease.care;


    document.getElementById(
        "diseasePrevention"
    ).innerHTML =
        "<b>Prevention:</b> " +
        disease.prevention;


    const suggestions =
        document.getElementById(
            "suggestions"
        );

    suggestions.innerHTML = "";


    data.suggestions.forEach(
        function (item) {

            const li =
                document.createElement("li");

            li.innerText =
                item;

            suggestions.appendChild(li);
        }
    );


    document.getElementById(
        "plantLink"
    ).href =
        plant.link;


    document.getElementById(
        "resultContent"
    ).scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ============================================
// PLANT INFORMATION MODAL
// ============================================

async function showPlant(plantId) {

    try {

        const response =
            await fetch(
                "/api/plant/" + plantId
            );


        const data =
            await response.json();


        if (!data.success) {

            alert(
                "Plant information not found."
            );

            return;
        }


        const plant =
            data.plant;


        document.getElementById(
            "modalPlantIcon"
        ).innerText =
            plant.icon;


        document.getElementById(
            "modalPlantName"
        ).innerText =
            plant.name;


        document.getElementById(
            "modalScientific"
        ).innerText =
            plant.scientific;


        document.getElementById(
            "modalDescription"
        ).innerText =
            plant.description;


        document.getElementById(
            "modalSoil"
        ).innerText =
            plant.soil;


        document.getElementById(
            "modalWater"
        ).innerText =
            plant.water;


        document.getElementById(
            "modalSun"
        ).innerText =
            plant.sun;


        document.getElementById(
            "modalMedical"
        ).innerText =
            plant.medical;


        document.getElementById(
            "modalDiseases"
        ).innerText =
            plant.diseases.join(
                ", "
            );


        document.getElementById(
            "modalLink"
        ).href =
            plant.link;


        document.getElementById(
            "plantModal"
        ).style.display =
            "block";


    } catch (error) {

        console.error(error);

        alert(
            "Unable to load plant information."
        );
    }
}


function closeModal() {

    document.getElementById(
        "plantModal"
    ).style.display =
        "none";
}


window.onclick =
    function(event) {

        const modal =
            document.getElementById(
                "plantModal"
            );

        if (event.target === modal) {

            closeModal();
        }
    };


// ============================================
// PLANT AI ASSISTANT
// ============================================

async function askAI() {

    const input =
        document.getElementById(
            "questionInput"
        );

    const plant =
        document.getElementById(
            "chatPlant"
        ).value;


    const question =
        input.value.trim();


    if (!question) {

        alert(
            "Please type a question."
        );

        return;
    }


    addMessage(
        question,
        "user"
    );


    input.value = "";


    try {

        const response =
            await fetch(
                "/api/ask",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            question:
                                question,

                            plant:
                                plant
                        })
                }
            );


        const data =
            await response.json();


        addMessage(
            data.answer,
            "bot"
        );


    } catch (error) {

        console.error(error);

        addMessage(
            "I couldn't connect to the Python server.",
            "bot"
        );
    }
}


// ============================================
// CHAT MESSAGE
// ============================================

function addMessage(
    message,
    type
) {

    const container =
        document.getElementById(
            "chatMessages"
        );


    const div =
        document.createElement("div");


    div.className =
        type === "user"
            ? "user-message"
            : "bot-message";


    div.innerText =
        message;


    container.appendChild(div);


    container.scrollTop =
        container.scrollHeight;
}


// ENTER KEY FOR AI

document.getElementById(
    "questionInput"
).addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            askAI();
        }
    }
);