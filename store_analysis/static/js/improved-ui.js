// Improved UI/UX JavaScript for Chidmano

class UIEnhancer {
    constructor() {
        this.initializeComponents();
        this.bindEvents();
    }

    initializeComponents() {
        // Initialize loading spinner
        this.createLoadingSpinner();
        
        // Initialize toast container
        this.createToastContainer();
        
        // Initialize form enhancements
        this.enhanceForms();
        
        // Initialize conditional fields
        this.initializeConditionalFields();
        
        // Initialize file upload areas
        this.initializeFileUploads();
        
        // Initialize progress tracking
        this.initializeProgressTracking();
    }

    createLoadingSpinner() {
        const spinner = document.createElement('div');
        spinner.id = 'loadingSpinner';
        spinner.className = 'loading-spinner';
        spinner.innerHTML = `
            <div class="text-center">
                <div class="spinner"></div>
                <div class="loading-text">در حال بارگذاری...</div>
            </div>
        `;
        document.body.appendChild(spinner);
    }

    createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    showLoading(message = 'در حال بارگذاری...') {
        const spinner = document.getElementById('loadingSpinner');
        const loadingText = spinner.querySelector('.loading-text');
        loadingText.textContent = message;
        spinner.style.display = 'flex';
    }

    hideLoading() {
        const spinner = document.getElementById('loadingSpinner');
        spinner.style.display = 'none';
    }

    showToast(message, type = 'info', duration = 5000) {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = 'toast show';
        
        const bgClass = type === 'success' ? 'bg-success' : 
                       type === 'error' ? 'bg-danger' : 
                       type === 'warning' ? 'bg-warning' : 'bg-info';
        
        const title = type === 'success' ? 'موفقیت' : 
                     type === 'error' ? 'خطا' : 
                     type === 'warning' ? 'هشدار' : 'اطلاعات';
        
        toast.innerHTML = `
            <div class="toast-header ${bgClass} text-white">
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;
        
        container.appendChild(toast);
        
        // Auto-remove after duration
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, duration);
        
        // Manual close functionality
        const closeBtn = toast.querySelector('.btn-close');
        closeBtn.addEventListener('click', () => {
            toast.remove();
        });
    }

    enhanceForms() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            // Add enhanced validation
            this.addFormValidation(form);
            
            // Add auto-save functionality
            this.addAutoSave(form);
            
            // Add submit enhancement
            this.addSubmitEnhancement(form);
        });
    }

    addFormValidation(form) {
        const inputs = form.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            // Real-time validation
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
            
            // Show validation on input
            input.addEventListener('input', () => {
                if (input.classList.contains('is-invalid')) {
                    this.validateField(input);
                }
            });
        });
    }

    validateField(field) {
        const value = field.value.trim();
        const isRequired = field.hasAttribute('required');
        const minLength = field.getAttribute('minlength');
        const maxLength = field.getAttribute('maxlength');
        const pattern = field.getAttribute('pattern');
        
        let isValid = true;
        let errorMessage = '';
        
        // Required validation
        if (isRequired && !value) {
            isValid = false;
            errorMessage = 'این فیلد الزامی است';
        }
        
        // Length validation
        if (value) {
            if (minLength && value.length < parseInt(minLength)) {
                isValid = false;
                errorMessage = `حداقل ${minLength} کاراکتر وارد کنید`;
            }
            
            if (maxLength && value.length > parseInt(maxLength)) {
                isValid = false;
                errorMessage = `حداکثر ${maxLength} کاراکتر مجاز است`;
            }
        }
        
        // Pattern validation
        if (pattern && value && !new RegExp(pattern).test(value)) {
            isValid = false;
            errorMessage = 'فرمت وارد شده صحیح نیست';
        }
        
        // Update field state
        this.updateFieldState(field, isValid, errorMessage);
    }

    updateFieldState(field, isValid, errorMessage) {
        const feedback = field.parentNode.querySelector('.invalid-feedback') || 
                        this.createFeedbackElement(field);
        
        if (isValid) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
            feedback.style.display = 'none';
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            feedback.textContent = errorMessage;
            feedback.style.display = 'block';
        }
    }

    createFeedbackElement(field) {
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        field.parentNode.appendChild(feedback);
        return feedback;
    }

    addAutoSave(form) {
        let autoSaveTimer;
        const formData = new FormData(form);
        
        const startAutoSave = () => {
            autoSaveTimer = setInterval(() => {
                const currentData = new FormData(form);
                // Here you could implement auto-save to localStorage or send to server
                console.log('Auto-saving form data...');
                localStorage.setItem('form_auto_save', JSON.stringify({
                    timestamp: Date.now(),
                    data: Object.fromEntries(currentData)
                }));
            }, 30000); // Auto-save every 30 seconds
        };
        
        const stopAutoSave = () => {
            if (autoSaveTimer) {
                clearInterval(autoSaveTimer);
            }
        };
        
        // Start auto-save when user starts typing
        form.addEventListener('input', () => {
            stopAutoSave();
            startAutoSave();
        });
        
        // Stop auto-save when form is submitted
        form.addEventListener('submit', stopAutoSave);
        
        // Restore auto-saved data on page load
        this.restoreAutoSavedData(form);
    }

    restoreAutoSavedData(form) {
        const inputs = form.querySelectorAll('input, textarea, select');
        const savedData = this.getAutoSavedData(form);
        if (!savedData) return;
        inputs.forEach(input => {
            if (input.type === 'file') {
                // Do not set value for file inputs
                return;
            }
            if (input.type === 'checkbox' || input.type === 'radio') {
                input.checked = savedData[input.name] === 'on' || savedData[input.name] === true;
            } else if (input.type !== 'file' && input.type !== 'checkbox' && input.type !== 'radio') {
                input.value = savedData[input.name] || '';
            }
        });
    }

    addSubmitEnhancement(form) {
        form.addEventListener('submit', (e) => {
            const submitBtn = form.querySelector('button[type="submit"]');
            
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>در حال ارسال...';
                
                // Re-enable button after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });
    }

    initializeConditionalFields() {
        console.log('Initializing conditional fields...');
        
        // Wait a bit to ensure DOM is fully loaded
        setTimeout(() => {
            // Handle surveillance camera conditional fields (checkbox or radio)
            const surveillanceInputs = document.querySelectorAll('input[name="has_surveillance"]');
            surveillanceInputs.forEach((input, index) => {
                const updateCameraSection = () => {
                    let show = false;
                    if (input.type === 'checkbox') {
                        show = input.checked;
                    } else if (input.type === 'radio') {
                        show = input.checked && (input.value === 'True' || input.value === '1' || input.value === 'on');
                    }
                    this.toggleConditionalSection('cameraSettings', show);
                };
                input.addEventListener('change', updateCameraSection);
                // Initialize on page load
                updateCameraSection();
            });

            // Handle customer video conditional fields (checkbox or radio)
            const customerVideoInputs = document.querySelectorAll('input[name="has_customer_video"]');
            customerVideoInputs.forEach((input, index) => {
                const updateVideoSection = () => {
                    let show = false;
                    if (input.type === 'checkbox') {
                        show = input.checked;
                    } else if (input.type === 'radio') {
                        show = input.checked && (input.value === 'True' || input.value === '1' || input.value === 'on');
                    }
                    this.toggleConditionalSection('videoSettings', show);
                };
                input.addEventListener('change', updateVideoSection);
                // Initialize on page load
                updateVideoSection();
            });
            
            // Handle other conditional fields with data-conditional attribute
            const conditionalTriggers = document.querySelectorAll('[data-conditional]');
            conditionalTriggers.forEach(trigger => {
                const targetField = trigger.getAttribute('data-conditional');
                const targetElement = document.getElementById(targetField);
                
                if (targetElement) {
                    const toggleField = () => {
                        if (trigger.type === 'checkbox') {
                            if (trigger.checked) {
                                targetElement.classList.add('show');
                            } else {
                                targetElement.classList.remove('show');
                            }
                        } else if (trigger.type === 'select-one') {
                            const selectedValue = trigger.value;
                            const requiredValue = trigger.getAttribute('data-conditional-value');
                            
                            if (selectedValue === requiredValue) {
                                targetElement.classList.add('show');
                            } else {
                                targetElement.classList.remove('show');
                            }
                        }
                    };
                    
                    trigger.addEventListener('change', toggleField);
                    toggleField(); // Initial state
                }
            });
            
            // Check if sections exist
            const cameraSection = document.getElementById('cameraSettings');
            const videoSection = document.getElementById('videoSettings');
            console.log('Camera section exists:', !!cameraSection);
            console.log('Video section exists:', !!videoSection);
            
                    // Also log all input elements to see what's available
        const allInputs = document.querySelectorAll('input');
        console.log('All input elements:', allInputs);
        
        // Test click events on all checkboxes
        const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
        console.log('All checkboxes:', allCheckboxes);
        
        allCheckboxes.forEach((checkbox, index) => {
            console.log(`Checkbox ${index}:`, checkbox.name, checkbox.checked);
            checkbox.addEventListener('click', (e) => {
                console.log(`Checkbox ${index} clicked:`, e.target.name, e.target.checked);
            });
            
            // Also add change event
            checkbox.addEventListener('change', (e) => {
                console.log(`Checkbox ${index} changed:`, e.target.name, e.target.checked);
            });
        });
        
        // Test direct manipulation
        const surveillanceCheckbox = document.querySelector('input[name="has_surveillance"]');
        if (surveillanceCheckbox) {
            console.log('Found surveillance checkbox, testing direct manipulation');
            surveillanceCheckbox.addEventListener('change', (e) => {
                console.log('Direct surveillance checkbox change:', e.target.checked);
                this.toggleConditionalSection('cameraSettings', e.target.checked);
            });
        }
        
        const customerVideoCheckbox = document.querySelector('input[name="has_customer_video"]');
        if (customerVideoCheckbox) {
            console.log('Found customer video checkbox, testing direct manipulation');
            customerVideoCheckbox.addEventListener('change', (e) => {
                console.log('Direct customer video checkbox change:', e.target.checked);
                this.toggleConditionalSection('videoSettings', e.target.checked);
            });
        }
        }, 100);
    }

    toggleConditionalSection(sectionId, show) {
        const section = document.getElementById(sectionId);
        console.log(`Toggling ${sectionId}:`, show);
        console.log('Section element:', section);
        
        if (section) {
            if (show) {
                console.log(`Showing ${sectionId}`);
                section.style.display = 'block';
                section.classList.add('show');
                // Add animation
                section.style.opacity = '0';
                setTimeout(() => {
                    section.style.opacity = '1';
                }, 10);
            } else {
                console.log(`Hiding ${sectionId}`);
                section.style.opacity = '0';
                setTimeout(() => {
                    section.style.display = 'none';
                    section.classList.remove('show');
                }, 300);
            }
        } else {
            console.error(`Section ${sectionId} not found!`);
        }
    }

    initializeFileUploads() {
        const fileUploadAreas = document.querySelectorAll('.file-upload-area');
        
        fileUploadAreas.forEach(area => {
            const fileInput = area.querySelector('input[type="file"]');
            
            if (fileInput) {
                // Drag and drop functionality
                area.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    area.classList.add('dragover');
                });
                
                area.addEventListener('dragleave', (e) => {
                    e.preventDefault();
                    area.classList.remove('dragover');
                });
                
                area.addEventListener('drop', (e) => {
                    e.preventDefault();
                    area.classList.remove('dragover');
                    const files = e.dataTransfer.files;
                    if (files.length > 0) {
                        fileInput.files = files;
                        this.updateFileDisplay(area, files[0]);
                    }
                });
                
                // Click to upload
                area.addEventListener('click', () => {
                    fileInput.click();
                });
                
                // File selection
                fileInput.addEventListener('change', (e) => {
                    if (e.target.files.length > 0) {
                        this.updateFileDisplay(area, e.target.files[0]);
                    }
                });
            }
        });
    }

    updateFileDisplay(area, file) {
        const icon = area.querySelector('.file-upload-icon i');
        const title = area.querySelector('h5');
        const description = area.querySelector('p');
        
        if (icon) {
            if (file.type.startsWith('image/')) {
                icon.className = 'fas fa-image';
            } else if (file.type.startsWith('video/')) {
                icon.className = 'fas fa-video';
            } else if (file.type.includes('pdf')) {
                icon.className = 'fas fa-file-pdf';
            } else {
                icon.className = 'fas fa-file';
            }
        }
        
        if (title) {
            title.textContent = file.name;
        }
        
        if (description) {
            description.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
        }
        
        this.showToast(`فایل ${file.name} با موفقیت انتخاب شد`, 'success', 3000);
    }

    initializeProgressTracking() {
        const progressBars = document.querySelectorAll('.progress-bar-custom');
        
        progressBars.forEach(bar => {
            const targetWidth = bar.getAttribute('data-progress') || '0';
            const currentWidth = parseInt(targetWidth);
            
            // Animate progress bar
            setTimeout(() => {
                bar.style.width = `${currentWidth}%`;
            }, 500);
        });
    }

    bindEvents() {
        // Global error handling
        window.addEventListener('error', (e) => {
            console.error('Global error:', e.error);
            this.showToast('خطایی رخ داده است. لطفاً صفحه را مجدداً بارگذاری کنید.', 'error');
        });
        
        // Network status monitoring
        window.addEventListener('online', () => {
            this.showToast('اتصال به اینترنت برقرار شد', 'success', 3000);
        });
        
        window.addEventListener('offline', () => {
            this.showToast('اتصال به اینترنت قطع شد', 'warning');
        });
        
        // Page visibility API for auto-refresh
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                // Page is hidden, pause auto-refresh
                this.pauseAutoRefresh();
            } else {
                // Page is visible, resume auto-refresh
                this.resumeAutoRefresh();
            }
        });
    }

    pauseAutoRefresh() {
        // Implementation for pausing auto-refresh
        console.log('Auto-refresh paused');
    }

    resumeAutoRefresh() {
        // Implementation for resuming auto-refresh
        console.log('Auto-refresh resumed');
    }

    // Retrieve auto-saved data for a form (dummy implementation to prevent error)
    getAutoSavedData(form) {
        // You can implement localStorage retrieval here if needed
        return null;
    }

    // Unused Area Section Enhancement
    initializeUnusedAreaSection() {
        // فقط tooltips و اعتبارسنجی را فعال نگه می‌داریم و هیچ کد دیگری اجرا نشود.
        try {
            this.initializeTooltips();
            // هیچ کد دیگری اجرا نشود و هیچ المنتی برای unused-area بررسی نشود.
        } catch (e) {
            // اگر المنتی نبود، هیچ خطایی ��مایش داده نشود
        }
    }

    updateUnusedAreaSelection() {
        const selectedOption = document.querySelector('.unused-area-radio:checked');
        const allOptions = document.querySelectorAll('.unused-area-option');
        
        // Remove selected class from all options
        allOptions.forEach(option => {
            option.classList.remove('selected');
        });
        
        // Add selected class to current option
        if (selectedOption) {
            const currentOption = selectedOption.closest('.unused-area-option');
            currentOption.classList.add('selected');
            
            // Show relevant fields based on selection
            this.showRelevantFields(selectedOption.value);
        }
    }

    showRelevantFields(selectedType) {
        const fieldsContainer = document.querySelector('.unused-area-fields');
        if (!fieldsContainer) return;
        
        // Show/hide fields based on selection
        const sizeField = fieldsContainer.querySelector('input[name="unused_area_size"]');
        const reasonField = fieldsContainer.querySelector('textarea[name="unused_area_reason"]');
        const descField = fieldsContainer.querySelector('textarea[name="unused_areas"]');
        
        if (selectedType === 'empty') {
            this.showField(sizeField);
            this.showField(reasonField);
            this.showField(descField);
        } else if (selectedType === 'low_traffic') {
            this.showField(sizeField);
            this.showField(reasonField);
            this.showField(descField);
        } else if (selectedType === 'storage') {
            this.showField(sizeField);
            this.showField(reasonField);
            this.hideField(descField);
        } else if (selectedType === 'staff') {
            this.showField(sizeField);
            this.showField(reasonField);
            this.showField(descField);
        } else if (selectedType === 'other') {
            this.showField(sizeField);
            this.showField(reasonField);
            this.showField(descField);
        }
    }

    showField(field) {
        if (field) {
            const fieldGroup = field.closest('.unused-area-field-group');
            if (fieldGroup) {
                fieldGroup.style.display = 'flex';
                fieldGroup.style.opacity = '1';
            }
        }
    }

    hideField(field) {
        if (field) {
            const fieldGroup = field.closest('.unused-area-field-group');
            if (fieldGroup) {
                fieldGroup.style.opacity = '0.5';
            }
        }
    }

    initializeTooltips() {
        const tooltipElements = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipElements.forEach(element => {
            if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
                new bootstrap.Tooltip(element, {
                    placement: 'top',
                    trigger: 'hover focus'
                });
            }
        });
    }

    addUnusedAreaValidation() {
        const form = document.querySelector('form');
        if (!form) return;
        
        const sizeField = form.querySelector('input[name="unused_area_size"]');
        const reasonField = form.querySelector('textarea[name="unused_area_reason"]');
        
        if (sizeField) {
            sizeField.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                if (value < 0) {
                    e.target.value = 0;
                }
            });
        }
        
        if (reasonField) {
            reasonField.addEventListener('input', (e) => {
                if (e.target.value.length > 500) {
                    e.target.value = e.target.value.substring(0, 500);
                    this.showToast('حداکثر 500 کاراکتر مجاز است', 'warning');
                }
            });
        }
    }
}

// Initialize UI Enhancer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Initializing UI Enhancer');
    window.uiEnhancer = new UIEnhancer();
    
    // Initialize unused area section
    if (window.uiEnhancer) {
        window.uiEnhancer.initializeUnusedAreaSection();
    }
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Also initialize when window loads (for cases where DOMContentLoaded fires too early)
window.addEventListener('load', () => {
    console.log('Window Loaded - Re-initializing conditional fields');
    if (window.uiEnhancer) {
        // Re-initialize conditional fields
        window.uiEnhancer.initializeConditionalFields();
    }
});

// Also try to initialize after a longer delay
setTimeout(() => {
    console.log('Delayed initialization - Re-initializing conditional fields');
    if (window.uiEnhancer) {
        // Re-initialize conditional fields
        window.uiEnhancer.initializeConditionalFields();
    }
}, 2000);

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UIEnhancer;
} 