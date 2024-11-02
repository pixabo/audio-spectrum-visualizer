document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const progressDiv = document.getElementById('progress');
    const fileInput = document.getElementById('audioFile');
    const dropZone = document.querySelector('.upload-area');
    const progressBar = document.createElement('div');
    
    // Add progress bar styling
    progressBar.className = 'progress-bar';
    progressDiv.appendChild(progressBar);

    // Add drag and drop styling
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        fileInput.files = e.dataTransfer.files;
        showFileName(e.dataTransfer.files[0]);
    });

    // Show selected filename with animation
    function showFileName(file) {
        const fileNameDisplay = document.getElementById('fileName') || document.createElement('div');
        fileNameDisplay.id = 'fileName';
        fileNameDisplay.className = 'file-name';
        fileNameDisplay.textContent = file.name;
        fileNameDisplay.style.animation = 'fadeIn 0.3s';
        if (!document.getElementById('fileName')) {
            dropZone.appendChild(fileNameDisplay);
        }
    }

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            showFileName(file);
        }
    });

    // Handle form submission
    uploadForm.onsubmit = async (e) => {
        e.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            showToast('Please select a file first.', 'error');
            return;
        }

        // Validate file size (20MB max)
        if (file.size > 20 * 1024 * 1024) {
            showToast('File is too large. Maximum size is 20MB.', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        
        document.getElementById('progress').style.display = 'block';
        
        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.status === 'success') {
                    window.location.href = `/download/${data.file_id}`;
                    setTimeout(() => {
                        document.getElementById('progress').style.display = 'none';
                    }, 1000);
                } else {
                    alert('Error processing file');
                }
            } else {
                alert('Error uploading file');
            }
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            document.getElementById('progress').style.display = 'none';
        }
    };
}); 