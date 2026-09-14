// Endereço utilizado pelo dashboard para acessar a API.
const studiesUrl = "/api/studies";

// Elementos da página que serão controlados pelo JavaScript.
const form = document.querySelector("#study-form");
const titleInput = document.querySelector("#title");
const descriptionInput = document.querySelector("#description");
const formMessage = document.querySelector("#form-message");
const loadingMessage = document.querySelector("#loading-message");
const emptyMessage = document.querySelector("#empty-message");
const studyList = document.querySelector("#study-list");
const refreshButton = document.querySelector("#refresh-button");
const submitButton = form.querySelector('button[type="submit"]');


// Apresenta uma mensagem abaixo do formulário.
function showFormMessage(message, type) {
    formMessage.textContent = message;
    formMessage.className = type;
}


// Converte a data recebida da API para o formato brasileiro.
function formatDate(dateText) {
    const date = new Date(dateText);

    return date.toLocaleString("pt-BR");
}


// Cria os elementos HTML que representam um estudo.
function createStudyElement(study) {
    const article = document.createElement("article");
    article.className = "study-item";

    const title = document.createElement("h3");
    title.textContent = study.title;

    const description = document.createElement("p");
    description.textContent = study.description;

    const createdAt = document.createElement("time");
    createdAt.dateTime = study.created_at;
    createdAt.textContent = `Criado em ${formatDate(study.created_at)}`;

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "delete-button";
    deleteButton.textContent = "Excluir";

    // Guarda no botão o ID do registro que deverá ser excluído.
    deleteButton.addEventListener("click", () => {
        deleteStudy(study.id);
    });

    article.append(title, description, createdAt, deleteButton);

    return article;
}


// Consulta todos os estudos armazenados.
async function loadStudies() {
    loadingMessage.hidden = false;
    emptyMessage.hidden = true;
    studyList.replaceChildren();

    try {
        const response = await fetch(studiesUrl);

        if (!response.ok) {
            throw new Error("Não foi possível carregar os estudos.");
        }

        const studies = await response.json();

        // Exibe uma mensagem quando o banco ainda não possui registros.
        if (studies.length === 0) {
            emptyMessage.hidden = false;
            return;
        }

        // Cria um card para cada registro recebido.
        studies.forEach((study) => {
            studyList.append(createStudyElement(study));
        });
    } catch (error) {
        emptyMessage.hidden = false;
        emptyMessage.textContent = error.message;
    } finally {
        loadingMessage.hidden = true;
    }
}


// Exclui um estudo utilizando seu identificador.
async function deleteStudy(studyId) {
    const confirmed = window.confirm(
        "Deseja realmente excluir este registro?",
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`${studiesUrl}/${studyId}`, {
            method: "DELETE",
        });

        if (!response.ok) {
            throw new Error("Não foi possível excluir o estudo.");
        }

        showFormMessage("Estudo excluído com sucesso.", "success-message");

        await loadStudies();
    } catch (error) {
        showFormMessage(error.message, "error-message");
    }
}


// Envia um novo estudo para a API.
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = titleInput.value.trim();
    const description = descriptionInput.value.trim();

    if (!title || !description) {
        showFormMessage(
            "Preencha o título e a descrição.",
            "error-message",
        );
        return;
    }

    submitButton.disabled = true;
    showFormMessage("Salvando estudo...", "");

    try {
        const response = await fetch(studiesUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                title,
                description,
            }),
        });

        if (!response.ok) {
            throw new Error("Não foi possível salvar o estudo.");
        }

        form.reset();

        showFormMessage(
            "Estudo salvo com sucesso.",
            "success-message",
        );

        await loadStudies();
    } catch (error) {
        showFormMessage(error.message, "error-message");
    } finally {
        submitButton.disabled = false;
    }
});


// Atualiza manualmente a listagem.
refreshButton.addEventListener("click", loadStudies);


// Carrega os registros assim que a página é aberta.
loadStudies();