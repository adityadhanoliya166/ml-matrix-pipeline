async function uploadDataset(event) {
    if (event) event.preventDefault();

    const fileInput = document.getElementById('csvFile');
    const statusMessage = document.getElementById('statusMessage');
    const alertBox = document.getElementById('alertBox');
    const resultsDiv = document.getElementById('results');

    alertBox.classList.add('hidden');
    alertBox.innerText = "";
    statusMessage.innerText = "";
    resultsDiv.classList.add('hidden');

    if (!fileInput.files[0]) {
        showAlert("Select a CSV file first.");
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    statusMessage.innerText = "Processing dataset and evaluating matrix...";

    try {
        const response = await fetch('/process-dataset', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Upload failed.");
        }

        statusMessage.innerText = "";
        resultsDiv.classList.remove('hidden');

        document.getElementById('rowCount').innerText = `Total Rows: ${data.rows}`;
        document.getElementById('featureCount').innerText = `Encoded Features: ${data.features}`;
        document.getElementById('qualityScore').innerText = `Matrix Quality Score: ${data.quality_score}`;
        
        document.getElementById('downloadML').href = data.download_url;

        renderTable(data.preview, 'mlTable');

    } catch (error) {
        statusMessage.innerText = "";
        showAlert(error.message);
    }
}

function showAlert(msg) {
    const alertBox = document.getElementById('alertBox');
    alertBox.innerText = msg;
    alertBox.classList.remove('hidden');
}

function renderTable(data, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = "";

    if (!data || data.length === 0) {
        container.innerHTML = "<p style='padding: 10px;'>No preview available.</p>";
        return;
    }

    const table = document.createElement('table');
    const headers = Object.keys(data[0]);

    let thead = "<thead><tr>";
    headers.forEach(h => { thead += `<th>${h}</th>`; });
    thead += "</tr></thead>";

    let tbody = "<tbody>";
    data.forEach(row => {
        tbody += "<tr>";
        headers.forEach(h => {
            tbody += `<td>${row[h] !== null ? row[h] : ''}</td>`;
        });
        tbody += "</tr>";
    });
    tbody += "</tbody>";

    table.innerHTML = thead + tbody;
    container.appendChild(table);
}