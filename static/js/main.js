/**
 * SGEA - Sistema de Gestão de Eventos Acadêmicos
 * Main JavaScript file
 */

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all components
    initPhoneMask();
    initDatePickers();
    initFormValidation();
    initAnimations();
});

/**
 * Phone mask for Brazilian format: (XX) XXXXX-XXXX
 */
function initPhoneMask() {
    const phoneInputs = document.querySelectorAll('input[type="tel"], input[name="phone"], input.phone-mask');

    phoneInputs.forEach(input => {
        input.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.length > 11) {
                value = value.slice(0, 11);
            }

            if (value.length > 0) {
                value = '(' + value;
            }
            if (value.length > 3) {
                value = value.slice(0, 3) + ') ' + value.slice(3);
            }
            if (value.length > 10) {
                value = value.slice(0, 10) + '-' + value.slice(10);
            }

            e.target.value = value;
        });

        // Add placeholder
        input.placeholder = '(XX) XXXXX-XXXX';
    });
}

/**
 * Initialize date and time pickers
 * Using native HTML5 date/time inputs with fallback
 */
function initDatePickers() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const timeInputs = document.querySelectorAll('input[type="time"]');
    const datetimeInputs = document.querySelectorAll('input[type="datetime-local"]');

    // Set minimum date to today for event start dates
    const today = new Date().toISOString().split('T')[0];

    dateInputs.forEach(input => {
        if (input.classList.contains('future-only') || input.name.includes('start')) {
            input.min = today;
        }
    });

    // Validate end date is after start date
    document.querySelectorAll('form').forEach(form => {
        const startDate = form.querySelector('input[name="start_date"]');
        const endDate = form.querySelector('input[name="end_date"]');

        if (startDate && endDate) {
            startDate.addEventListener('change', function () {
                endDate.min = this.value;
                if (endDate.value && endDate.value < this.value) {
                    endDate.value = this.value;
                }
            });
        }
    });
}

/**
 * Form validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form[data-validate]');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            let isValid = true;

            // Clear previous errors
            form.querySelectorAll('.form-error').forEach(el => el.remove());
            form.querySelectorAll('.form-control.error').forEach(el => {
                el.classList.remove('error');
            });

            // Validate required fields
            form.querySelectorAll('[required]').forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    showFieldError(field, 'Este campo é obrigatório');
                }
            });

            // Validate email
            form.querySelectorAll('input[type="email"]').forEach(field => {
                if (field.value && !isValidEmail(field.value)) {
                    isValid = false;
                    showFieldError(field, 'Por favor, insira um e-mail válido');
                }
            });

            // Validate password confirmation
            const password = form.querySelector('input[name="password"]');
            const confirmPassword = form.querySelector('input[name="password_confirm"]');

            if (password && confirmPassword) {
                if (password.value !== confirmPassword.value) {
                    isValid = false;
                    showFieldError(confirmPassword, 'As senhas não coincidem');
                }

                if (!isValidPassword(password.value)) {
                    isValid = false;
                    showFieldError(password, 'A senha deve ter no mínimo 8 caracteres, incluindo letras, números e caracteres especiais');
                }
            }

            // Validate phone
            form.querySelectorAll('input[name="phone"]').forEach(field => {
                if (field.value && !isValidPhone(field.value)) {
                    isValid = false;
                    showFieldError(field, 'Telefone no formato (XX) XXXXX-XXXX');
                }
            });

            // Validate number fields
            form.querySelectorAll('input[type="number"]').forEach(field => {
                const min = parseInt(field.min);
                const max = parseInt(field.max);
                const value = parseInt(field.value);

                if (field.value && (isNaN(value) || (min && value < min) || (max && value > max))) {
                    isValid = false;
                    showFieldError(field, `Valor deve ser ${min ? 'no mínimo ' + min : ''} ${max ? 'e no máximo ' + max : ''}`);
                }
            });

            // Validate image files
            form.querySelectorAll('input[type="file"][accept*="image"]').forEach(field => {
                if (field.files && field.files[0]) {
                    const file = field.files[0];
                    const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

                    if (!validTypes.includes(file.type)) {
                        isValid = false;
                        showFieldError(field, 'Por favor, selecione uma imagem válida (JPEG, PNG, GIF ou WebP)');
                    }

                    // Max 5MB
                    if (file.size > 5 * 1024 * 1024) {
                        isValid = false;
                        showFieldError(field, 'A imagem deve ter no máximo 5MB');
                    }
                }
            });

            if (!isValid) {
                e.preventDefault();
                // Scroll to first error
                const firstError = form.querySelector('.form-control.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    });
}

/**
 * Show error message for a field
 */
function showFieldError(field, message) {
    field.classList.add('error');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

/**
 * Validation helpers
 */
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function isValidPhone(phone) {
    const cleaned = phone.replace(/\D/g, '');
    return cleaned.length === 10 || cleaned.length === 11;
}

function isValidPassword(password) {
    // At least 8 chars, with letters, numbers, and special characters
    const hasLetter = /[a-zA-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    return password.length >= 8 && hasLetter && hasNumber && hasSpecial;
}

/**
 * Initialize fade-in animations
 */
function initAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.card, .menu-card, .event-card').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}

/**
 * Show confirmation dialog
 */
function confirmAction(message) {
    return confirm(message || 'Tem certeza que deseja realizar esta ação?');
}

/**
 * Format date to Brazilian format
 */
function formatDate(dateString) {
    const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
    return new Date(dateString).toLocaleDateString('pt-BR', options);
}

/**
 * Format time
 */
function formatTime(timeString) {
    return timeString.slice(0, 5);
}
