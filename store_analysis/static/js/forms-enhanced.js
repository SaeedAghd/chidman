// پیش‌نمایش فایل‌های آپلود
document.addEventListener('DOMContentLoaded', function() {
    
    // تابع عمومی برای پیش‌نمایش عکس‌ها
    function setupImagePreview(inputId, previewId) {
        const input = document.getElementById(inputId);
        const previewContainer = document.getElementById(previewId);
        
        if (input && previewContainer) {
            // اطمینان از وجود multiple attribute
            if (!input.hasAttribute('multiple')) {
                input.setAttribute('multiple', 'multiple');
            }
            
            input.addEventListener('change', function(e) {
                const files = Array.from(e.target.files);
                console.log(`Selected ${files.length} files for ${inputId}`);
                previewContainer.innerHTML = '';
                
                files.forEach((file, index) => {
                    if (file.type.startsWith('image/')) {
                        const reader = new FileReader();
                        
                        reader.onload = function(e) {
                            const previewItem = document.createElement('div');
                            previewItem.className = 'image-preview-item';
                            previewItem.innerHTML = `
                                <img src="${e.target.result}" alt="پیش‌نمایش عکس ${index + 1}">
                                <button type="button" class="image-preview-remove" onclick="removeImagePreview('${inputId}', ${index})">×</button>
                            `;
                            previewContainer.appendChild(previewItem);
                        };
                        
                        reader.readAsDataURL(file);
                    } else {
                        console.warn(`File ${file.name} is not an image`);
                    }
                });
            });
        }
    }
    
    // تابع عمومی برای پیش‌نمایش ویدیوها
    function setupVideoPreview(inputId, previewId) {
        const input = document.getElementById(inputId);
        const previewContainer = document.getElementById(previewId);
        
        if (input && previewContainer) {
            input.addEventListener('change', function(e) {
                const file = e.target.files[0];
                previewContainer.innerHTML = '';
                
                if (file && file.type.startsWith('video/')) {
                    const url = URL.createObjectURL(file);
                    const previewItem = document.createElement('div');
                    previewItem.className = 'video-preview-item';
                    previewItem.innerHTML = `
                        <video src="${url}" controls></video>
                        <div class="video-info">${file.name}</div>
                        <button type="button" class="video-preview-remove" onclick="removeVideoPreview('${inputId}')">×</button>
                    `;
                    previewContainer.appendChild(previewItem);
                }
            });
        }
    }
    
    // تابع عمومی برای پیش‌نمایش فایل‌ها
    function setupFilePreview(inputId, previewId) {
        const input = document.getElementById(inputId);
        const previewContainer = document.getElementById(previewId);
        
        if (input && previewContainer) {
            input.addEventListener('change', function(e) {
                const file = e.target.files[0];
                previewContainer.innerHTML = '';
                
                if (file) {
                    const fileIcon = getFileIcon(file.type);
                    const fileSize = formatFileSize(file.size);
                    
                    const previewItem = document.createElement('div');
                    previewItem.className = 'file-preview-item';
                    previewItem.innerHTML = `
                        <div class="file-icon">${fileIcon}</div>
                        <div class="file-info">
                            <div class="file-name">${file.name}</div>
                            <div class="file-size">${fileSize}</div>
                        </div>
                        <button type="button" class="file-preview-remove" onclick="removeFilePreview('${inputId}')">×</button>
                    `;
                    previewContainer.appendChild(previewItem);
                }
            });
        }
    }
    
    // راه‌اندازی همه پیش‌نمایش‌ها
    setupImagePreview('design-photos-input', 'design-photos-preview');
    setupImagePreview('structure-photos-input', 'structure-photos-preview');
    setupImagePreview('store-photos-input', 'store-photos-preview');
    setupImagePreview('product-photos-input', 'product-photos-preview');
    
    setupVideoPreview('customer-flow-video-input', 'customer-flow-video-preview');
    setupVideoPreview('store-video-input', 'store-video-preview');
    setupVideoPreview('surveillance-footage-input', 'surveillance-footage-preview');
    
    setupFilePreview('store-plan-input', 'store-plan-preview');
    setupFilePreview('product-catalog-input', 'product-catalog-preview');
    setupFilePreview('sales-file-input', 'sales-file-preview');
});

// تابع برای دریافت آیکون فایل
function getFileIcon(fileType) {
    if (fileType.includes('pdf')) return '📄';
    if (fileType.includes('excel') || fileType.includes('spreadsheet')) return '📊';
    if (fileType.includes('word')) return '📝';
    if (fileType.includes('image')) return '🖼️';
    if (fileType.includes('video')) return '🎥';
    if (fileType.includes('audio')) return '🎵';
    return '📁';
}

// تابع برای فرمت کردن حجم فایل
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// حذف عکس از پیش‌نمایش
function removeImagePreview(inputId, index) {
    const input = document.getElementById(inputId);
    const previewContainer = document.getElementById(inputId.replace('-input', '-preview'));
    
    // حذف از DOM
    const previewItems = previewContainer.querySelectorAll('.image-preview-item');
    if (previewItems[index]) {
        previewItems[index].remove();
    }
    
    // به‌روزرسانی فایل‌های انتخاب شده
    const dt = new DataTransfer();
    const files = Array.from(input.files);
    
    files.forEach((file, i) => {
        if (i !== index) {
            dt.items.add(file);
        }
    });
    
    input.files = dt.files;
}

// حذف ویدیو از پیش‌نمایش
function removeVideoPreview(inputId) {
    const input = document.getElementById(inputId);
    const previewContainer = document.getElementById(inputId.replace('-input', '-preview'));
    
    previewContainer.innerHTML = '';
    input.value = '';
}

// حذف فایل از پیش‌نمایش
function removeFilePreview(inputId) {
    const input = document.getElementById(inputId);
    const previewContainer = document.getElementById(inputId.replace('-input', '-preview'));
    
    previewContainer.innerHTML = '';
    input.value = '';
}

// نمایش راهنمای آپلود
function showUploadGuide() {
    const guide = document.getElementById('uploadGuide');
    if (guide) {
        guide.style.display = 'block';
    }
}

// مخفی کردن راهنمای آپلود
function hideUploadGuide() {
    const guide = document.getElementById('uploadGuide');
    if (guide) {
        guide.style.display = 'none';
    }
}

// بررسی گام فعلی و نمایش راهنما در صورت نیاز
function checkCurrentStepForUploadGuide() {
    const currentStep = document.querySelector('.form-section.active');
    if (currentStep) {
        const stepNumber = currentStep.getAttribute('data-step');
        // گام‌هایی که فیلد آپلود دارند: 2, 3, 4, 5, 6
        if (['2', '3', '4', '5', '6'].includes(stepNumber)) {
            showUploadGuide();
        } else {
            hideUploadGuide();
        }
    }
}
