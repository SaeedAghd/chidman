document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('storeAnalysisForm');
    const sections = document.querySelectorAll('.form-section');
    const stepItems = document.querySelectorAll('.step-item');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    let currentStep = 1;
    const totalSteps = sections.length;
    
    // Initialize form
    updateStepDisplay();
    
    // Debug: Check if all sections exist
    console.log('Available sections:');
    sections.forEach((section, index) => {
        console.log(`Section ${index + 1}:`, section.dataset.step);
    });
    
    // Step navigation click handlers
    stepItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            if (index + 1 <= currentStep) {
                goToStep(index + 1);
            }
        });
    });
    
    // Navigation button handlers
    prevBtn.addEventListener('click', () => {
        if (currentStep > 1) {
            goToStep(currentStep - 1);
        }
    });
    
    nextBtn.addEventListener('click', () => {
        console.log('Next button clicked, current step:', currentStep);
        // Temporarily disable validation for testing
        if (currentStep < totalSteps) {
            console.log('Moving to step:', currentStep + 1);
            goToStep(currentStep + 1);
        }
        
        // Original validation code (commented out for testing)
        /*
        if (validateCurrentStep()) {
            if (currentStep < totalSteps) {
                console.log('Moving to step:', currentStep + 1);
                goToStep(currentStep + 1);
            }
        } else {
            console.log('Validation failed for step:', currentStep);
        }
        */
    });
    
    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateAllSteps()) {
            // Show loading state
            submitBtn.innerHTML = '<span class="spinner"></span> در حال ارسال...';
            submitBtn.disabled = true;
            
            // Submit form
            const formData = new FormData(form);
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showSuccessMessage();
                } else {
                    showErrorMessage(data.message || 'خطا در ارسال فرم');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showErrorMessage('خطا در ارتباط با سرور');
            })
            .finally(() => {
                submitBtn.innerHTML = '<span>ارسال فرم</span><span>🚀</span>';
                submitBtn.disabled = false;
            });
        }
    });
    
    function goToStep(step) {
        // Hide current section
        const currentSection = document.querySelector('.form-section.active');
        if (currentSection) {
            currentSection.classList.remove('active');
        }
        
        // Show target section
        const targetSection = document.querySelector(`.form-section[data-step="${step}"]`);
        if (targetSection) {
            targetSection.classList.add('active');
        }
        
        // Update step navigation
        stepItems.forEach((item, index) => {
            item.classList.remove('active', 'completed');
            if (index + 1 < step) {
                item.classList.add('completed');
            } else if (index + 1 === step) {
                item.classList.add('active');
            }
        });
        
        currentStep = step;
        updateStepDisplay();
        
        // نمایش راهنمای آپلود در گام‌های مربوطه
        if (typeof checkCurrentStepForUploadGuide === 'function') {
            checkCurrentStepForUploadGuide();
        }
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        // Debug log
        console.log(`Switched to step ${step}`);
    }
    
    function updateStepDisplay() {
        // Update navigation buttons
        prevBtn.style.display = currentStep > 1 ? 'flex' : 'none';
        nextBtn.style.display = currentStep < totalSteps ? 'flex' : 'none';
        submitBtn.style.display = currentStep === totalSteps ? 'flex' : 'none';
        
        // Show final motivation message on last step
        const finalMotivation = document.getElementById('finalMotivation');
        if (finalMotivation) {
            finalMotivation.style.display = currentStep === totalSteps ? 'block' : 'none';
        }
        
        // Update step labels
        if (currentStep < totalSteps) {
            nextBtn.innerHTML = '<span>بعدی</span><span>→</span>';
        }
        
        // Update progress bar
        updateProgressBar();
    }
    
    function updateProgressBar() {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        const progressPercent = document.getElementById('progressPercent');
        
        const progress = (currentStep / totalSteps) * 100;
        
        progressFill.style.width = progress + '%';
        progressText.textContent = `مرحله ${currentStep} از ${totalSteps}`;
        progressPercent.textContent = Math.round(progress) + '%';
        
        // Add celebration effect for milestones
        if (currentStep === Math.ceil(totalSteps / 2)) {
            showMilestoneMessage('نیمه راه را طی کردید! 🎉');
        } else if (currentStep === totalSteps - 1) {
            showMilestoneMessage('تقریباً تمام شد! 🔥');
        }
    }
    
    function showMilestoneMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
            z-index: 1000;
            font-family: 'Vazirmatn', 'Estedad', 'Shabnam', 'Samim', sans-serif;
            font-weight: 600;
            animation: fadeInUp 0.5s ease;
        `;
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }
    
    function validateCurrentStep() {
        const currentSection = document.querySelector('.form-section.active');
        if (!currentSection) {
            console.log('No active section found');
            return false;
        }
        
        const requiredFields = currentSection.querySelectorAll('[required]');
        let isValid = true;
        
        console.log('Validating step', currentStep, 'with', requiredFields.length, 'required fields');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('error');
                isValid = false;
                console.log('Field validation failed:', field.name);
            } else {
                field.classList.remove('error');
            }
        });
        
        // Special validation for checkboxes
        const checkboxGroups = currentSection.querySelectorAll('.checkbox-group');
        checkboxGroups.forEach(group => {
            const checkboxes = group.querySelectorAll('input[type="checkbox"]');
            const hasChecked = Array.from(checkboxes).some(cb => cb.checked);
            
            if (!hasChecked) {
                group.classList.add('error');
                isValid = false;
                console.log('Checkbox group validation failed');
            } else {
                group.classList.remove('error');
            }
        });
        
        if (!isValid) {
            showValidationMessage('لطفاً تمام فیلدهای اجباری را پر کنید');
        }
        
        console.log('Step validation result:', isValid);
        return isValid;
    }
    
    function validateAllSteps() {
        let isValid = true;
        
        sections.forEach(section => {
            const requiredFields = section.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('error');
                    isValid = false;
                }
            });
            
            const checkboxGroups = section.querySelectorAll('.checkbox-group');
            checkboxGroups.forEach(group => {
                const checkboxes = group.querySelectorAll('input[type="checkbox"]');
                const hasChecked = Array.from(checkboxes).some(cb => cb.checked);
                
                if (!hasChecked) {
                    group.classList.add('error');
                    isValid = false;
                }
            });
        });
        
        if (!isValid) {
            showValidationMessage('لطفاً تمام فیلدهای اجباری را پر کنید');
            // Go to first invalid step
            const firstError = document.querySelector('.form-section .error');
            if (firstError) {
                const errorSection = firstError.closest('.form-section');
                const stepNumber = parseInt(errorSection.dataset.step);
                goToStep(stepNumber);
            }
        }
        
        return isValid;
    }
    
    function showValidationMessage(message) {
        // Remove existing messages
        const existingMessage = document.querySelector('.validation-message');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        // Create new message
        const messageDiv = document.createElement('div');
        messageDiv.className = 'validation-message';
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ef4444;
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
            z-index: 1000;
            font-family: 'Vazirmatn', 'Estedad', 'Shabnam', 'Samim', sans-serif;
            font-weight: 600;
            animation: fadeInUp 0.3s ease;
        `;
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
    
    function showSuccessMessage() {
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 3rem;
            border-radius: 24px;
            box-shadow: 0 32px 64px rgba(16, 185, 129, 0.3);
            z-index: 1000;
            font-family: 'Vazirmatn', 'Estedad', 'Shabnam', 'Samim', sans-serif;
            text-align: center;
            animation: fadeInUp 0.5s ease;
        `;
        messageDiv.innerHTML = `
            <div style="font-size: 3rem; margin-bottom: 1rem;">✅</div>
            <h2 style="font-size: 2rem; font-weight: 700; margin-bottom: 1rem;">فرم با موفقیت ارسال شد!</h2>
            <p style="font-size: 1.2rem; opacity: 0.9;">گزارش تحلیل فروشگاه شما در کمتر از 30 دقیقه آماده خواهد شد.</p>
        `;
        
        document.body.appendChild(messageDiv);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
            // Reset form
            form.reset();
            goToStep(1);
        }, 5000);
    }
    
    function showErrorMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ef4444;
            color: white;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
            z-index: 1000;
            font-family: 'Vazirmatn', 'Estedad', 'Shabnam', 'Samim', sans-serif;
            font-weight: 600;
            animation: fadeInUp 0.3s ease;
        `;
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
    
    // File upload handlers
    const fileUploads = document.querySelectorAll('.file-upload');
    fileUploads.forEach(upload => {
        const input = upload.querySelector('input[type="file"]');
        const text = upload.querySelector('.file-upload-text');
        
        input.addEventListener('change', function() {
            if (this.files.length > 0) {
                const fileName = this.files[0].name;
                text.textContent = `📎 ${fileName}`;
                upload.style.borderColor = '#10b981';
                upload.style.background = 'rgba(16, 185, 129, 0.1)';
            }
        });
        
        upload.addEventListener('click', () => {
            input.click();
        });
    });
    
    // Form field focus effects
    const formFields = document.querySelectorAll('.form-field');
    formFields.forEach(field => {
        const input = field.querySelector('.form-control');
        if (input) {
            input.addEventListener('focus', () => {
                field.classList.add('focused');
            });
            
            input.addEventListener('blur', () => {
                field.classList.remove('focused');
            });
        }
    });
    
    // Ripple effect for buttons
    function createRipple(event) {
        const button = event.currentTarget;
        const circle = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;
        
        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
        circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
        circle.classList.add('ripple');
        
        const ripple = button.getElementsByClassName('ripple')[0];
        if (ripple) {
            ripple.remove();
        }
        
        button.appendChild(circle);
    }
    
    const buttons = document.querySelectorAll('.nav-button, .submit-button');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
    });
});

// Add error styles
const style = document.createElement('style');
style.textContent = `
    .form-control.error {
        border-color: #ef4444 !important;
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1) !important;
    }
    
    .checkbox-group.error {
        border: 2px solid #ef4444 !important;
        background: rgba(239, 68, 68, 0.05) !important;
    }
    
    .validation-message {
        animation: fadeInUp 0.3s ease;
    }
`;
document.head.appendChild(style);
