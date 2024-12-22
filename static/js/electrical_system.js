// DOM Elements
const layoutCanvas = document.getElementById('layout-canvas');
const addComponentBtn = document.getElementById('btn-add-component');
const saveLayoutBtn = document.getElementById('btn-save-layout');
const downloadBtn = document.getElementById('btn-download');
const loadingOverlay = document.getElementById('loading-overlay');
const progressBar = document.querySelector('.progress-bar');
const loadingText = document.getElementById('loading-text');

// Component drag and drop functionality
document.querySelectorAll('.electrical-component').forEach(component => {
    component.addEventListener('dragstart', handleDragStart);
    component.addEventListener('dragend', handleDragEnd);
});

layoutCanvas.addEventListener('dragover', handleDragOver);
layoutCanvas.addEventListener('drop', handleDrop);

function handleDragStart(e) {
    e.dataTransfer.setData('text/plain', e.target.dataset.type);
    e.target.classList.add('dragging');
}

function handleDragEnd(e) {
    e.target.classList.remove('dragging');
}

function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
}

function handleDrop(e) {
    e.preventDefault();
    const componentType = e.dataTransfer.getData('text/plain');
    const component = createComponent(componentType, e.offsetX, e.offsetY);
    layoutCanvas.appendChild(component);
}

function createComponent(type, x, y) {
    const component = document.createElement('div');
    component.className = 'electrical-component positioned';
    component.style.left = `${x}px`;
    component.style.top = `${y}px`;
    component.textContent = type.charAt(0).toUpperCase() + type.slice(1);
    component.dataset.type = type;
    
    // Make positioned components draggable
    component.draggable = true;
    component.addEventListener('dragstart', handleComponentDragStart);
    component.addEventListener('dragend', handleComponentDragEnd);
    
    return component;
}

// Save layout functionality
saveLayoutBtn.addEventListener('click', async () => {
    showLoading('Saving layout...');
    try {
        const layout = getLayoutData();
        // TODO: Implement API call to save layout
        await simulateOperation(1500);
        showSuccess('Layout saved successfully');
    } catch (error) {
        showError('Failed to save layout');
    }
    hideLoading();
});

// Download functionality
downloadBtn.addEventListener('click', async () => {
    showLoading('Generating diagram...');
    try {
        // TODO: Implement diagram generation and download
        await simulateOperation(2000);
        showSuccess('Diagram downloaded successfully');
    } catch (error) {
        showError('Failed to generate diagram');
    }
    hideLoading();
});

// Helper functions
function showLoading(message) {
    loadingText.textContent = message;
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
    progressBar.style.width = '0%';
}

function showSuccess(message) {
    // TODO: Implement success notification
    console.log(message);
}

function showError(message) {
    // TODO: Implement error notification
    console.error(message);
}

function getLayoutData() {
    const components = Array.from(layoutCanvas.querySelectorAll('.electrical-component.positioned'));
    return components.map(component => ({
        type: component.dataset.type,
        x: parseInt(component.style.left),
        y: parseInt(component.style.top)
    }));
}

// Simulate async operations
function simulateOperation(duration) {
    return new Promise((resolve) => {
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            progressBar.style.width = `${progress}%`;
            if (progress >= 100) {
                clearInterval(interval);
                resolve();
            }
        }, duration / 10);
    });
}
