async function uploadImage() {
    const fileInput = document.getElementById('fileInput');
    const loader = document.querySelector('.loader');
    const originalImg = document.getElementById('originalImg');
    const resultImg = document.getElementById('resultImg');

    if (!fileInput.files[0]) {
        alert('Please select an image');
        return;
    }

    loader.style.display = 'block';
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/detect', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        originalImg.src = data.original;
        resultImg.src = data.result;
    } catch (error) {
        console.error('Error:', error);
        alert('Detection failed');
    } finally {
        loader.style.display = 'none';
    }
}