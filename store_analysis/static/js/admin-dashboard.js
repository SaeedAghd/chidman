// Admin Dashboard JavaScript - بهبود یافته
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Admin Dashboard loaded');
    
    // Error handling برای تمام AJAX requests
    function handleAjaxError(xhr, status, error) {
        console.error('AJAX Error:', {xhr, status, error});
        
        let errorMessage = 'خطا در ارتباط با سرور';
        if (xhr.responseJSON && xhr.responseJSON.error) {
            errorMessage = xhr.responseJSON.error;
        } else if (xhr.status === 500) {
            errorMessage = 'خطای داخلی سرور';
        } else if (xhr.status === 404) {
            errorMessage = 'صفحه مورد نظر یافت نشد';
        } else if (xhr.status === 403) {
            errorMessage = 'دسترسی غیرمجاز';
        }
        
        showNotification(errorMessage, 'error');
    }
    
    // نمایش اعلان‌ها
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'}"></i>
                <span>${message}</span>
            </div>
            <button class="notification-close">&times;</button>
        `;
        
        document.body.appendChild(notification);
        
        // حذف خودکار بعد از 5 ثانیه
        setTimeout(() => {
            notification.remove();
        }, 5000);
        
        // حذف دستی
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.remove();
        });
    }
    
    // بهبود نمودارها
    function initializeCharts() {
        try {
            // نمودار کاربران و پرداخت‌ها
            const chartData = window.chartData || [];
            const chartLabels = window.chartLabels || [];
            
            if (chartData.length > 0 && typeof Chart !== 'undefined') {
                const ctx = document.getElementById('adminChart');
                if (ctx) {
                    new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: chartLabels,
                            datasets: [{
                                label: 'کاربران جدید',
                                data: chartData.map(d => d.users),
                                borderColor: '#3b82f6',
                                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                                tension: 0.4
                            }, {
                                label: 'پرداخت‌ها',
                                data: chartData.map(d => d.payments),
                                borderColor: '#10b981',
                                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                                tension: 0.4
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'top',
                                }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                }
            }
        } catch (error) {
            console.error('Chart initialization error:', error);
        }
    }
    
    // بهبود جداول
    function initializeTables() {
        try {
            // اضافه کردن قابلیت جستجو به جداول
            const tables = document.querySelectorAll('.admin-table');
            tables.forEach(table => {
                const searchInput = table.querySelector('.table-search');
                if (searchInput) {
                    searchInput.addEventListener('input', function() {
                        const searchTerm = this.value.toLowerCase();
                        const rows = table.querySelectorAll('tbody tr');
                        
                        rows.forEach(row => {
                            const text = row.textContent.toLowerCase();
                            row.style.display = text.includes(searchTerm) ? '' : 'none';
                        });
                    });
                }
            });
        } catch (error) {
            console.error('Table initialization error:', error);
        }
    }
    
    // بهبود فرم‌ها
    function initializeForms() {
        try {
            const forms = document.querySelectorAll('.admin-form');
            forms.forEach(form => {
                form.addEventListener('submit', function(e) {
                    const submitBtn = form.querySelector('button[type="submit"]');
                    if (submitBtn) {
                        submitBtn.disabled = true;
                        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> در حال پردازش...';
                    }
                });
            });
        } catch (error) {
            console.error('Form initialization error:', error);
        }
    }
    
    // بهبود دکمه‌ها
    function initializeButtons() {
        try {
            // دکمه‌های حذف
            const deleteButtons = document.querySelectorAll('.btn-delete');
            deleteButtons.forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    const confirmMessage = this.dataset.confirm || 'آیا مطمئن هستید؟';
                    if (confirm(confirmMessage)) {
                        const url = this.href || this.dataset.url;
                        if (url) {
                            fetch(url, {
                                method: 'DELETE',
                                headers: {
                                    'X-CSRFToken': getCookie('csrftoken'),
                                    'Content-Type': 'application/json',
                                }
                            })
                            .then(response => response.json())
                            .then(data => {
                                if (data.success) {
                                    showNotification('عملیات با موفقیت انجام شد', 'success');
                                    setTimeout(() => location.reload(), 1000);
                                } else {
                                    showNotification(data.error || 'خطا در انجام عملیات', 'error');
                                }
                            })
                            .catch(error => {
                                console.error('Delete error:', error);
                                showNotification('خطا در حذف', 'error');
                            });
                        }
                    }
                });
            });
        } catch (error) {
            console.error('Button initialization error:', error);
        }
    }
    
    // بهبود منو
    function initializeMenu() {
        try {
            const menuToggle = document.querySelector('.menu-toggle');
            const sidebar = document.querySelector('.admin-sidebar');
            
            if (menuToggle && sidebar) {
                menuToggle.addEventListener('click', function() {
                    sidebar.classList.toggle('collapsed');
                    localStorage.setItem('sidebar-collapsed', sidebar.classList.contains('collapsed'));
                });
                
                // بازگردانی وضعیت منو
                const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
                if (isCollapsed) {
                    sidebar.classList.add('collapsed');
                }
            }
        } catch (error) {
            console.error('Menu initialization error:', error);
        }
    }
    
    // بهبود responsive
    function initializeResponsive() {
        try {
            function handleResize() {
                const sidebar = document.querySelector('.admin-sidebar');
                if (window.innerWidth < 768 && sidebar) {
                    sidebar.classList.add('collapsed');
                }
            }
            
            window.addEventListener('resize', handleResize);
            handleResize();
        } catch (error) {
            console.error('Responsive initialization error:', error);
        }
    }
    
    // تابع کمکی برای دریافت CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // اجرای تمام توابع
    try {
        initializeCharts();
        initializeTables();
        initializeForms();
        initializeButtons();
        initializeMenu();
        initializeResponsive();
        
        console.log('✅ Admin Dashboard initialized successfully');
    } catch (error) {
        console.error('❌ Admin Dashboard initialization error:', error);
        showNotification('خطا در بارگذاری داشبورد', 'error');
    }
});

// اضافه کردن CSS برای اعلان‌ها
// Check if notificationCSS is already defined
if (typeof notificationCSS === 'undefined') {
    const notificationCSS = `
.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    padding: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    z-index: 10000;
    min-width: 300px;
    animation: slideIn 0.3s ease;
}

.notification-error {
    border-left: 4px solid #ef4444;
}

.notification-success {
    border-left: 4px solid #10b981;
}

.notification-info {
    border-left: 4px solid #3b82f6;
}

.notification-content {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
}

.notification-close {
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    color: #666;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
`;

// اضافه کردن CSS به صفحه
const style = document.createElement('style');
style.textContent = notificationCSS;
document.head.appendChild(style);
}
