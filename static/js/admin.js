// ===========================================
// Admin Panel JavaScript
// ===========================================

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 992) {
                if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                    sidebar.classList.remove('active');
                }
            }
        });
    }

    // Progress circle animation
    const progressCircles = document.querySelectorAll('.progress-circle');
    progressCircles.forEach(circle => {
        const percentage = circle.dataset.percentage || 0;
        circle.style.setProperty('--percentage', percentage);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Confirm delete actions
    const deleteForms = document.querySelectorAll('form[data-confirm]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const message = this.dataset.confirm || 'Are you sure you want to delete this item?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Data table search functionality
    const searchInput = document.getElementById('tableSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const table = document.querySelector('.data-table');
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    // Live results update (if on results page)
    if (document.querySelector('.admin-result')) {
        setInterval(updateResults, 30000); // Update every 30 seconds
    }
});

// Modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        // Focus first input in modal
        const firstInput = modal.querySelector('input, select, textarea');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 100);
        }
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        // Reset form in modal
        const form = modal.querySelector('form');
        if (form) {
            form.reset();
        }
    }
}

// Close modal on outside click
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// Close modal on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
        });
    }
});

// Update results via AJAX
async function updateResults() {
    try {
        const response = await fetch('/admin/results/data');
        if (response.ok) {
            const data = await response.json();
            // Update charts and data would go here
            console.log('Results updated:', data);
        }
    } catch (error) {
        console.error('Error updating results:', error);
    }
}

// Export results to CSV
function exportResults() {
    const table = document.querySelector('.data-table');
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = [];
        cols.forEach(col => {
            rowData.push('"' + col.textContent.trim().replace(/"/g, '""') + '"');
        });
        csv.push(rowData.join(','));
    });

    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'voting_results.csv';
    link.click();
}

// Print results
function printResults() {
    window.print();
}
