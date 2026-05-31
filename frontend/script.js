const API_BASE = "http://127.0.0.1:8000";
async function uploadPDF() {

    const fileInput = document.getElementById("pdfFile");

    if (!fileInput.files.length) {
        alert("Please select a PDF first");
        return;
    }

    const formData = new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    try {

        const response = await fetch(
            `${API_BASE}/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        document.getElementById(
            "uploadStatus"
        ).innerText = data.message;

    } catch (error) {

        console.error(error);

        document.getElementById(
            "uploadStatus"
        ).innerText = "Upload failed";
    }
}





async function askQuestion() {

    const question =
        document.getElementById("question").value;

    document.getElementById(
        "answer"
    ).innerText = "Thinking...";

    const response = await fetch(
        `${API_BASE}/ask`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        }
    );

    const data = await response.json();

    document.getElementById(
        "answer"
    ).innerText = data.answer;
}