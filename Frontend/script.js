document.getElementById('upload-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const fileInput = document.getElementById('csv-file');
    const resultDiv = document.getElementById('result');

    if (!fileInput.files.length) {
        resultDiv.innerHTML = '<p style="color: #ef4444;">Please select a CSV file.</p>';
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    resultDiv.innerHTML = '<p style="color: #94a3b8;">Processing file...</p>';

    try {
        const response = await fetch('http://127.0.0.1:8000/process-dataset', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        
        // Build absolute URL for the backend file download
        const downloadUrl = `http://127.0.0.1:8000${data.download_url}`;

        // Render success message, download button, and JSON preview
        resultDiv.innerHTML = `
            <p style="color: #22c55e; font-weight: 600; margin-bottom: 12px;">Success! Pipeline finished.</p>
            
            <a href="${downloadUrl}" download style="
                display: inline-block;
                background: #10b981;
                color: #ffffff;
                padding: 10px 16px;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 500;
                margin-bottom: 16px;">
                📥 Download ML Matrix CSV
            </a>

            <pre style="background: #0f172a; padding: 12px; border-radius: 6px; overflow-x: auto; color: #cbd5e1; font-size: 0.85rem;">${JSON.stringify(data, null, 2)}</pre>
        `;
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: #ef4444;">Error: ${error.message}</p>`;
    }
});