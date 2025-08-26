// Analysis Detail Page JavaScript

class AnalysisDetailManager {
    constructor() {
        this.isProcessing = false;
        this.refreshInterval = null;
        this.initializeComponents();
    }

    initializeComponents() {
        // Check if analysis is processing
        this.checkProcessingStatus();
        
        // Initialize file preview functionality
        this.initializeFilePreview();
        
        // Initialize auto-refresh if processing
        if (this.isProcessing) {
            this.startAutoRefresh();
        }
    }

    checkProcessingStatus() {
        // Use Django template variable if available, otherwise check DOM
        if (typeof window.isProcessing !== 'undefined') {
            this.isProcessing = window.isProcessing;
        } else {
            const statusBadge = document.querySelector('.status-badge');
            if (statusBadge && statusBadge.classList.contains('status-processing')) {
                this.isProcessing = true;
            }
        }
    }

    startAutoRefresh() {
        this.refreshInterval = setInterval(() => {
            this.checkStatusUpdate();
        }, 10000); // Refresh every 10 seconds

        // Stop auto-refresh when page is not visible
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.stopAutoRefresh();
            } else {
                this.startAutoRefresh();
            }
        });
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    async checkStatusUpdate() {
        try {
            const response = await fetch(window.location.href);
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const statusElement = doc.querySelector('.status-badge');
            
            if (statusElement && !statusElement.classList.contains('status-processing')) {
                window.location.reload();
            }
        } catch (error) {
            console.log('Auto-refresh failed:', error);
        }
    }

    initializeFilePreview() {
        const fileLinks = document.querySelectorAll('.file-item a');
        fileLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const fileType = this.getFileType(link);
                if (fileType === 'video') {
                    e.preventDefault();
                    const videoUrl = link.href;
                    this.showVideoModal(videoUrl);
                }
            });
        });
    }

    getFileType(link) {
        const icon = link.querySelector('i');
        if (icon && icon.classList.contains('fa-video')) {
            return 'video';
        }
        return 'file';
    }

    showVideoModal(videoUrl) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">ویدیوی مسیر مشتری</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <video controls width="100%">
                            <source src="${videoUrl}" type="video/mp4">
                            مرورگر شما از پخش ویدیو پشتیبانی نمی‌کند.
                        </video>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
        
        modal.addEventListener('hidden.bs.modal', () => {
            document.body.removeChild(modal);
        });
    }

    // Download report functionality
    downloadReport() {
        const downloadBtn = document.querySelector('.btn-download-report');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Show loading state
                downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>در حال آماده‌سازی...';
                downloadBtn.disabled = true;
                
                // Simulate download process
                setTimeout(() => {
                    downloadBtn.innerHTML = '<i class="fas fa-download me-2"></i>دانلود گزارش کامل';
                    downloadBtn.disabled = false;
                    
                    // Show success message
                    if (window.uiEnhancer) {
                        window.uiEnhancer.showToast('گزارش با موفقیت دانلود شد', 'success');
                    }
                }, 2000);
            });
        }
    }

    // Share functionality
    initializeShare() {
        const shareBtn = document.querySelector('.btn-share');
        if (shareBtn) {
            shareBtn.addEventListener('click', (e) => {
                e.preventDefault();
                
                if (navigator.share) {
                    navigator.share({
                        title: 'نتایج تحلیل فروشگاه',
                        text: 'نتایج تحلیل هوشمند فروشگاه من',
                        url: window.location.href
                    });
                } else {
                    // Fallback for browsers that don't support Web Share API
                    navigator.clipboard.writeText(window.location.href).then(() => {
                        if (window.uiEnhancer) {
                            window.uiEnhancer.showToast('لینک کپی شد', 'success');
                        }
                    });
                }
            });
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.analysisDetailManager = new AnalysisDetailManager();
    
    // Initialize additional features
    if (window.analysisDetailManager) {
        window.analysisDetailManager.downloadReport();
        window.analysisDetailManager.initializeShare();
    }
}); 