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
        this.setupGoalsInteractions();
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
            if (this.currentStep === this.totalSteps) {
                finalMotivation.style.display = 'block';
                // Add animation effect
                setTimeout(() => {
                    finalMotivation.style.opacity = '1';
                    finalMotivation.style.transform = 'translateY(0)';
                }, 100);
                
                // Scroll to final message
                setTimeout(() => {
                    finalMotivation.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'center' 
                    });
                }, 500);
            } else {
                finalMotivation.style.display = 'none';
                finalMotivation.style.opacity = '0';
                finalMotivation.style.transform = 'translateY(20px)';
            }
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
            // تنظیمات fetch برای سازگاری با مرورگرها
            const fetchOptions = {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                },
                credentials: 'same-origin', // برای session cookies
                redirect: 'manual' // برای کنترل redirect
            };

            // بررسی پشتیبانی از fetch
            if (!window.fetch) {
                // Fallback به XMLHttpRequest
                return this.handleFormSubmissionXHR(formData);
            }

            const response = await fetch(form.action, fetchOptions);

            if (response.ok) {
                // بررسی نوع پاسخ
                const contentType = response.headers.get('content-type');
                
                if (contentType && contentType.includes('application/json')) {
                    // پاسخ JSON
                    const data = await response.json();
                    if (data.success) {
                        this.showMessage(data.message || '🎉 فرم با موفقیت ارسال شد! در حال هدایت به صفحه پرداخت...', 'success');
                        // هدایت به صفحه پرداخت
                        console.log('Redirect URL:', data.redirect_url);
                        setTimeout(() => {
                            if (data.redirect_url) {
                                console.log('Redirecting to:', data.redirect_url);
                                window.location.href = data.redirect_url;
                            } else {
                                console.log('No redirect URL provided, staying on page');
                                this.showMessage('فرم با موفقیت ارسال شد! لطفاً منتظر بمانید...', 'success');
                            }
                        }, 1500);
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
                    }, 2000);
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
            
            // بررسی نوع خطا
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                this.showMessage('خطا در اتصال به سرور. لطفاً اتصال اینترنت خود را بررسی کنید.', 'error');
            } else if (error.message.includes('CSRF')) {
                this.showMessage('خطا در احراز هویت. لطفاً صفحه را رفرش کنید و دوباره تلاش کنید.', 'error');
            } else {
                this.showMessage('خطایی در ارسال فرم رخ داد. لطفاً دوباره تلاش کنید.', 'error');
            }
        } finally {
            // بازگردانی دکمه
            if (submitBtn) {
                submitBtn.innerHTML = '<span>ارسال فرم</span>';
                submitBtn.disabled = false;
            }
        }
    }

    handleFormSubmissionXHR(formData) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4) {
                    if (xhr.status >= 200 && xhr.status < 300) {
                        try {
                            const contentType = xhr.getResponseHeader('content-type');
                            if (contentType && contentType.includes('application/json')) {
                                const data = JSON.parse(xhr.responseText);
                                if (data.success) {
                                    this.showMessage(data.message || '🎉 با تشکر! در حال آپلود عکس و فیلم هستیم، منتظر بمانید...', 'success');
                                    setTimeout(() => {
                                        if (data.redirect_url) {
                                            window.location.href = data.redirect_url;
                                        } else {
                                            window.location.href = '/store/dashboard/';
                                        }
                                    }, 2000);
                                } else {
                                    this.showMessage(data.message || 'خطا در ارسال فرم', 'error');
                                }
                            } else {
                                this.showMessage('🎉 با تشکر! در حال آپلود عکس و فیلم هستیم، منتظر بمانید...', 'success');
                                setTimeout(() => {
                                    window.location.href = '/store/dashboard/';
                                }, 2000);
                            }
                            resolve();
                        } catch (error) {
                            reject(error);
                        }
                    } else {
                        reject(new Error(`خطا در سرور: ${xhr.status}`));
                    }
                }
            };
            
            xhr.onerror = () => {
                reject(new Error('خطا در اتصال به سرور'));
            };
            
            xhr.open('POST', document.getElementById('storeAnalysisForm').action);
            xhr.setRequestHeader('X-CSRFToken', document.querySelector('[name=csrfmiddlewaretoken]').value);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.send(formData);
        });
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

    setupGoalsInteractions() {
        // Goal cards interactions
        document.querySelectorAll('.goal-card').forEach(card => {
            const checkbox = card.querySelector('input[type="checkbox"]');
            
            // Card click handler
            card.addEventListener('click', (e) => {
                if (e.target.closest('.goal-checkbox')) return;
                checkbox.checked = !checkbox.checked;
                this.updateGoalCard(card, checkbox.checked);
                this.updateGoalsProgress();
            });

            // Checkbox change handler
            checkbox.addEventListener('change', () => {
                this.updateGoalCard(card, checkbox.checked);
                this.updateGoalsProgress();
            });

            // Initial state
            this.updateGoalCard(card, checkbox.checked);
        });

        // Select all functionality
        const selectAllCheckbox = document.getElementById('select_all_goals');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', () => {
                const isChecked = selectAllCheckbox.checked;
                document.querySelectorAll('.goal-card input[type="checkbox"]').forEach(checkbox => {
                    checkbox.checked = isChecked;
                    const card = checkbox.closest('.goal-card');
                    this.updateGoalCard(card, isChecked);
                });
                this.updateGoalsProgress();
            });
        }

        // Smart suggestions
        this.setupSmartSuggestions();
        
        // Initial progress update
        this.updateGoalsProgress();
    }

    updateGoalCard(card, isSelected) {
        if (isSelected) {
            card.classList.add('selected');
        } else {
            card.classList.remove('selected');
        }
    }

    updateGoalsProgress() {
        const selectedGoals = document.querySelectorAll('.goal-card input[type="checkbox"]:checked');
        const totalGoals = document.querySelectorAll('.goal-card input[type="checkbox"]').length;
        const progressText = document.querySelector('.progress-text');
        const progressFill = document.querySelector('.progress-fill');
        
        if (progressText && progressFill) {
            const percentage = (selectedGoals.length / totalGoals) * 100;
            progressText.textContent = `${selectedGoals.length} هدف انتخاب شده`;
            progressFill.style.width = `${percentage}%`;
        }

        // Update select all checkbox
        const selectAllCheckbox = document.getElementById('select_all_goals');
        if (selectAllCheckbox) {
            selectAllCheckbox.checked = selectedGoals.length === totalGoals;
        }
    }

    setupSmartSuggestions() {
        const suggestionsContainer = document.getElementById('smartSuggestions');
        if (!suggestionsContainer) return;

        // Get store type from form
        const storeTypeSelect = document.querySelector('select[name="store_type"]');
        if (!storeTypeSelect) return;

        const suggestions = {
            'پوشاک': ['افزایش فروش و درآمد', 'تقویت برندینگ', 'بهبود تجربه مشتری'],
            'مواد غذایی': ['بهینه‌سازی عملیات', 'تقویت امنیت', 'افزایش فروش و درآمد'],
            'الکترونیک': ['دیجیتال‌سازی', 'بهبود تجربه مشتری', 'تقویت امنیت'],
            'کتاب و لوازم تحریر': ['بهبود تجربه مشتری', 'تقویت برندینگ', 'افزایش فروش و درآمد'],
            'لوازم خانگی': ['بهینه‌سازی عملیات', 'افزایش فروش و درآمد', 'بهبود تجربه مشتری']
        };

        const updateSuggestions = () => {
            const selectedType = storeTypeSelect.value;
            const typeSuggestions = suggestions[selectedType] || [];
            
            suggestionsContainer.innerHTML = typeSuggestions.map(suggestion => 
                `<span class="suggestion-tag" data-goal="${suggestion}">${suggestion}</span>`
            ).join('');

            // Add click handlers to suggestion tags
            suggestionsContainer.querySelectorAll('.suggestion-tag').forEach(tag => {
                tag.addEventListener('click', () => {
                    const goalName = tag.dataset.goal;
                    const goalCard = document.querySelector(`[data-goal="${goalName}"]`);
                    if (goalCard) {
                        const checkbox = goalCard.querySelector('input[type="checkbox"]');
                        checkbox.checked = true;
                        this.updateGoalCard(goalCard, true);
                        this.updateGoalsProgress();
                        
                        // Scroll to goal card
                        goalCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        
                        // Highlight effect
                        goalCard.style.animation = 'pulse 0.6s ease-in-out';
                        setTimeout(() => {
                            goalCard.style.animation = '';
                        }, 600);
                    }
                });
            });
        };

        storeTypeSelect.addEventListener('change', updateSuggestions);
        updateSuggestions(); // Initial load
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
    // بررسی پشتیبانی از fetch
    if (!window.fetch) {
        console.warn('Fetch API not supported, loading polyfill...');
        // بارگذاری polyfill برای fetch
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/whatwg-fetch@3.6.2/dist/fetch.umd.js';
        script.onload = () => {
            console.log('Fetch polyfill loaded');
            window.simpleFormManager = new SimpleFormManager();
        };
        script.onerror = () => {
            console.error('Failed to load fetch polyfill');
            // Fallback to XMLHttpRequest
            window.simpleFormManager = new SimpleFormManager();
        };
        document.head.appendChild(script);
    } else {
        window.simpleFormManager = new SimpleFormManager();
    }
});
