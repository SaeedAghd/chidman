/**
 * ===== SIMPLE FORM JAVASCRIPT =====
 * Clean and effective JavaScript for form functionality
 * Inspired by successful websites like ChatGPT, Google, Apple
 */

class SimpleFormManager {
    constructor() {
        this.currentStep = 1;
        this.totalSteps = 7;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateStep();
    }

    setupEventListeners() {
        const nextBtn = document.getElementById('nextBtn');
        const prevBtn = document.getElementById('prevBtn');
        const submitBtn = document.getElementById('submitBtn');

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.goToNextStep());
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.goToPreviousStep());
        }

        if (submitBtn) {
            submitBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleFormSubmission();
            });
        }

        // Step navigation
        document.querySelectorAll('.step-item').forEach(item => {
            item.addEventListener('click', () => {
                const step = parseInt(item.dataset.step);
                if (step <= this.currentStep) {
                    this.goToStep(step);
                }
            });
        });

        // Form validation
        document.querySelectorAll('.form-control[required]').forEach(field => {
            field.addEventListener('blur', () => {
                this.validateField(field);
            });
        });

        // File upload handling
        this.setupFileUploads();
    }

    goToNextStep() {
        if (this.validateCurrentStep()) {
            if (this.currentStep < this.totalSteps) {
                this.currentStep++;
                this.updateStep();
            }
        }
    }

    goToPreviousStep() {
        if (this.currentStep > 1) {
            this.currentStep--;
            this.updateStep();
        }
    }

    goToStep(step) {
        if (step >= 1 && step <= this.totalSteps) {
            this.currentStep = step;
            this.updateStep();
        }
    }

    validateCurrentStep() {
        const currentSection = document.querySelector(`.form-section[data-step="${this.currentStep}"]`);
        if (!currentSection) return true;

        const requiredFields = currentSection.querySelectorAll('.form-control[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        if (!isValid) {
            this.showMessage('لطفاً تمام فیلدهای الزامی را پر کنید', 'error');
        }

        return isValid;
    }

    validateField(field) {
        const value = field.value.trim();
        const isValid = value.length > 0;

        if (isValid) {
            field.classList.remove('error');
            field.classList.add('success');
        } else {
            field.classList.remove('success');
            field.classList.add('error');
        }

        return isValid;
    }

    updateStep() {
        // Hide all sections
        document.querySelectorAll('.form-section').forEach(section => {
            section.classList.remove('active');
        });

        // Show current section
        const currentSection = document.querySelector(`.form-section[data-step="${this.currentStep}"]`);
        if (currentSection) {
            currentSection.classList.add('active');
        }

        // Update step navigation
        document.querySelectorAll('.step-item').forEach(item => {
            item.classList.remove('active', 'completed');
            const step = parseInt(item.dataset.step);
            
            if (step < this.currentStep) {
                item.classList.add('completed');
            } else if (step === this.currentStep) {
                item.classList.add('active');
            }
        });

        // Update progress bar
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const progressPercent = document.getElementById('progressPercent');

        if (progressFill) {
            const progress = (this.currentStep / this.totalSteps) * 100;
            progressFill.style.width = progress + '%';
        }

        if (progressText) {
            progressText.textContent = `مرحله ${this.currentStep} از ${this.totalSteps}`;
        }

        if (progressPercent) {
            const percent = Math.round((this.currentStep / this.totalSteps) * 100);
            progressPercent.textContent = percent + '%';
        }

        // Update navigation buttons
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const submitBtn = document.getElementById('submitBtn');

        if (prevBtn) {
            prevBtn.style.display = this.currentStep > 1 ? 'flex' : 'none';
        }

        if (nextBtn) {
            nextBtn.style.display = this.currentStep < this.totalSteps ? 'flex' : 'none';
        }

        if (submitBtn) {
            submitBtn.style.display = this.currentStep === this.totalSteps ? 'flex' : 'none';
        }

        // Show final message on last step
        const finalMotivation = document.getElementById('finalMotivation');
        if (finalMotivation) {
            finalMotivation.style.display = this.currentStep === this.totalSteps ? 'block' : 'none';
        }
    }

    async handleFormSubmission() {
        if (!this.validateCurrentStep()) {
            return;
        }

        const form = document.getElementById('storeAnalysisForm');
        const formData = new FormData(form);
        const submitBtn = document.getElementById('submitBtn');

        // نمایش حالت loading
        if (submitBtn) {
            submitBtn.innerHTML = '<span class="spinner"></span> در حال ارسال...';
            submitBtn.disabled = true;
        }

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                },
                redirect: 'manual' // برای کنترل redirect
            });

            if (response.ok) {
                // بررسی نوع پاسخ
                const contentType = response.headers.get('content-type');
                
                if (contentType && contentType.includes('application/json')) {
                    // پاسخ JSON
                    const data = await response.json();
                    if (data.success) {
                        this.showMessage('🎉 فرم با موفقیت ارسال شد! در حال هدایت به صفحه پرداخت...', 'success');
                        // هدایت به صفحه پرداخت
                        console.log('Redirect URL:', data.redirect_url);
                        setTimeout(() => {
                            const redirectUrl = data.redirect_url || '/store/dashboard/';
                            console.log('Redirecting to:', redirectUrl);
                            window.location.href = redirectUrl;
                        }, 1000);
                    } else {
                        this.showMessage(data.message || 'خطا در ارسال فرم', 'error');
                    }
                } else {
                    // پاسخ HTML - احتمالاً redirect
                    this.showMessage('🎉 فرم با موفقیت ارسال شد! در حال هدایت به صفحه پرداخت...', 'success');
                    // هدایت به صفحه پرداخت
                    setTimeout(() => {
                        // بررسی response URL برای payment page
                        console.log('Response URL:', response.url);
                        if (response.url && response.url.includes('/payment/')) {
                            console.log('Redirecting to payment page:', response.url);
                            window.location.href = response.url;
                        } else {
                            // در غیر این صورت، تلاش کن payment page را پیدا کنی
                            console.log('No payment URL found, redirecting to dashboard');
                            window.location.href = '/store/dashboard/';
                        }
                    }, 1000);
                }
            } else if (response.type === 'opaqueredirect') {
                // Redirect response
                this.showMessage('🎉 فرم با موفقیت ارسال شد! در حال هدایت به صفحه پرداخت...', 'success');
                setTimeout(() => {
                    // تلاش برای هدایت به صفحه پرداخت
                    window.location.href = '/store/dashboard/';
                }, 1000);
            } else {
                throw new Error(`خطا در سرور: ${response.status}`);
            }
        } catch (error) {
            console.error('Form submission error:', error);
            this.showMessage('خطایی در ارسال فرم رخ داد. لطفاً دوباره تلاش کنید.', 'error');
        } finally {
            // بازگردانی دکمه
            if (submitBtn) {
                submitBtn.innerHTML = '<span>ارسال فرم</span>';
                submitBtn.disabled = false;
            }
        }
    }

    setupFileUploads() {
        // Handle all file inputs
        document.querySelectorAll('input[type="file"]').forEach(input => {
            input.addEventListener('change', (e) => {
                this.handleFileUpload(e);
            });

            // Make upload area clickable
            const uploadArea = input.closest('.file-upload');
            if (uploadArea) {
                uploadArea.addEventListener('click', (e) => {
                    // Only trigger if clicking on the upload area itself, not on child elements
                    if (e.target === uploadArea || e.target.classList.contains('file-upload-text') || e.target.classList.contains('file-upload-hint')) {
                        input.click();
                    }
                });

                // Handle upload button clicks
                const uploadButton = uploadArea.querySelector('.file-upload-button');
                if (uploadButton) {
                    uploadButton.addEventListener('click', (e) => {
                        e.stopPropagation();
                        input.click();
                    });
                }

                // Drag and drop functionality
                uploadArea.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    uploadArea.classList.add('drag-over');
                });

                uploadArea.addEventListener('dragleave', () => {
                    uploadArea.classList.remove('drag-over');
                });

                uploadArea.addEventListener('drop', (e) => {
                    e.preventDefault();
                    uploadArea.classList.remove('drag-over');
                    input.files = e.dataTransfer.files;
                    this.handleFileUpload(e);
                });
            }
        });
    }

    handleFileUpload(event) {
        const files = event.target.files;
        const inputId = event.target.id;
        const previewContainer = document.getElementById(inputId + '-preview');
        
        console.log('File upload triggered:', files.length, 'files');
        
        if (!previewContainer) {
            console.error('Preview container not found for:', inputId);
            return;
        }

        // Clear previous previews
        previewContainer.innerHTML = '';

        if (files.length === 0) {
            console.log('No files selected');
            return;
        }

        // Handle multiple files
        Array.from(files).forEach((file, index) => {
            console.log('Processing file:', file.name, file.type);
            if (file.type.startsWith('image/')) {
                this.createImagePreview(file, previewContainer, index);
            } else if (file.type.startsWith('video/')) {
                this.createVideoPreview(file, previewContainer, index);
            } else {
                this.createFilePreview(file, previewContainer, index);
            }
        });

        this.showMessage(`${files.length} فایل با موفقیت انتخاب شد`, 'success');
    }

    createImagePreview(file, container, index) {
        const previewItem = document.createElement('div');
        previewItem.className = 'file-preview-item';
        previewItem.style.cssText = `
            position: relative;
            display: inline-block;
            margin: 8px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        `;

        const img = document.createElement('img');
        img.style.cssText = `
            width: 120px;
            height: 120px;
            object-fit: cover;
            display: block;
        `;
        
        // استفاده از FileReader برای نمایش بهتر تصاویر
        const reader = new FileReader();
        reader.onload = function(e) {
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
        
        // Fallback در صورت خطا
        img.onerror = function() {
            img.src = URL.createObjectURL(file);
        };

        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 4px 8px;
            font-size: 12px;
            text-align: center;
        `;
        overlay.textContent = this.formatFileSize(file.size);

        const removeBtn = document.createElement('button');
        removeBtn.innerHTML = '×';
        removeBtn.style.cssText = `
            position: absolute;
            top: 4px;
            right: 4px;
            width: 24px;
            height: 24px;
            border: none;
            border-radius: 50%;
            background: rgba(239, 68, 68, 0.9);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        removeBtn.onclick = () => {
            previewItem.remove();
        };

        previewItem.appendChild(img);
        previewItem.appendChild(overlay);
        previewItem.appendChild(removeBtn);
        container.appendChild(previewItem);
    }

    createVideoPreview(file, container, index) {
        const previewItem = document.createElement('div');
        previewItem.className = 'file-preview-item';
        previewItem.style.cssText = `
            position: relative;
            display: inline-block;
            margin: 8px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        `;

        const video = document.createElement('video');
        video.src = URL.createObjectURL(file);
        video.controls = true;
        video.preload = 'metadata';
        video.style.cssText = `
            width: 120px;
            height: 120px;
            object-fit: cover;
            display: block;
        `;
        
        // اضافه کردن poster برای ویدیو
        video.onloadedmetadata = function() {
            // ایجاد thumbnail از ویدیو
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = 120;
            canvas.height = 120;
            
            video.currentTime = 1; // گرفتن فریم در ثانیه 1
            video.onseeked = function() {
                ctx.drawImage(video, 0, 0, 120, 120);
                video.poster = canvas.toDataURL();
            };
        };

        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 4px 8px;
            font-size: 12px;
            text-align: center;
        `;
        overlay.textContent = this.formatFileSize(file.size);

        const removeBtn = document.createElement('button');
        removeBtn.innerHTML = '×';
        removeBtn.style.cssText = `
            position: absolute;
            top: 4px;
            right: 4px;
            width: 24px;
            height: 24px;
            border: none;
            border-radius: 50%;
            background: rgba(239, 68, 68, 0.9);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        removeBtn.onclick = () => {
            previewItem.remove();
        };

        previewItem.appendChild(video);
        previewItem.appendChild(overlay);
        previewItem.appendChild(removeBtn);
        container.appendChild(previewItem);
    }

    createFilePreview(file, container, index) {
        const previewItem = document.createElement('div');
        previewItem.className = 'file-preview-item';
        previewItem.style.cssText = `
            position: relative;
            display: inline-block;
            margin: 8px;
            padding: 16px;
            border: 2px dashed #d1d5db;
            border-radius: 8px;
            text-align: center;
            background: #f9fafb;
            min-width: 120px;
        `;

        const fileIcon = document.createElement('div');
        fileIcon.style.cssText = `
            font-size: 32px;
            margin-bottom: 8px;
        `;
        fileIcon.textContent = '📄';

        const fileName = document.createElement('div');
        fileName.style.cssText = `
            font-size: 12px;
            font-weight: 500;
            color: #374151;
            margin-bottom: 4px;
            word-break: break-all;
        `;
        fileName.textContent = file.name;

        const fileSize = document.createElement('div');
        fileSize.style.cssText = `
            font-size: 10px;
            color: #6b7280;
        `;
        fileSize.textContent = this.formatFileSize(file.size);

        const removeBtn = document.createElement('button');
        removeBtn.innerHTML = '×';
        removeBtn.style.cssText = `
            position: absolute;
            top: 4px;
            right: 4px;
            width: 20px;
            height: 20px;
            border: none;
            border-radius: 50%;
            background: rgba(239, 68, 68, 0.9);
            color: white;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        removeBtn.onclick = () => {
            previewItem.remove();
        };

        previewItem.appendChild(fileIcon);
        previewItem.appendChild(fileName);
        previewItem.appendChild(fileSize);
        previewItem.appendChild(removeBtn);
        container.appendChild(previewItem);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    showMessage(message, type = 'info') {
        // Create simple message element
        const messageEl = document.createElement('div');
        messageEl.className = `simple-message message-${type}`;
        messageEl.textContent = message;
        
        // Style the message
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transform: translateX(400px);
            transition: transform 0.3s ease-out;
        `;

        document.body.appendChild(messageEl);

        // Animate in
        setTimeout(() => {
            messageEl.style.transform = 'translateX(0)';
        }, 100);

        // Auto remove
        setTimeout(() => {
            messageEl.style.transform = 'translateX(400px)';
            setTimeout(() => {
                if (messageEl.parentNode) {
                    messageEl.parentNode.removeChild(messageEl);
                }
            }, 300);
        }, 5000);
    }
}

// Global functions for HTML onclick handlers
function hideUploadGuide() {
    const guide = document.getElementById('uploadGuide');
    if (guide) {
        guide.style.display = 'none';
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.simpleFormManager = new SimpleFormManager();
});
