// Анимация появления элементов при прокрутке
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.animate-fade-in');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'all 0.6s ease-out';
        observer.observe(element);
    });
});

// Плавная прокрутка к секциям
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Анимация для карточек при наведении
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px)';
        this.style.boxShadow = '0 15px 30px rgba(0, 0, 0, 0.15)';
    });

    card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.1)';
    });
});

// Анимация для кнопок
document.querySelectorAll('.btn-primary').forEach(button => {
    button.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-3px)';
        this.style.boxShadow = '0 5px 15px rgba(255, 75, 141, 0.3)';
    });

    button.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = 'none';
    });
});

// Анимация для иконок в футере
document.querySelectorAll('.social-icons a').forEach(icon => {
    icon.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-3px)';
        this.style.backgroundColor = 'var(--primary-color)';
    });

    icon.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
    });
});

// Анимация появления элементов при скролле
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.master-card, .service-card, .review-item').forEach(el => {
    observer.observe(el);
});

// Инициализация табов в профиле
document.addEventListener('DOMContentLoaded', function() {
    const tabLinks = document.querySelectorAll('.profile-menu .list-group-item');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Удаляем активный класс у всех ссылок и панелей
            tabLinks.forEach(l => l.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('show', 'active'));
            
            // Добавляем активный класс к выбранной ссылке и соответствующей панели
            this.classList.add('active');
            const targetId = this.getAttribute('href');
            document.querySelector(targetId).classList.add('show', 'active');
        });
    });
});

// Валидация формы записи
const appointmentForm = document.querySelector('.appointment-form');
if (appointmentForm) {
    appointmentForm.addEventListener('submit', function(e) {
        const dateInput = this.querySelector('input[type="date"]');
        const timeInput = this.querySelector('input[type="time"]');
        
        if (dateInput && timeInput) {
            const selectedDate = new Date(dateInput.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate < today) {
                e.preventDefault();
                alert('Пожалуйста, выберите будущую дату');
                return;
            }
            
            const selectedTime = timeInput.value;
            const [hours, minutes] = selectedTime.split(':');
            const selectedDateTime = new Date(selectedDate);
            selectedDateTime.setHours(parseInt(hours), parseInt(minutes), 0, 0);
            
            if (selectedDateTime < new Date()) {
                e.preventDefault();
                alert('Пожалуйста, выберите будущее время');
                return;
            }
        }
    });
}

// Предварительный просмотр загружаемого фото профиля
const photoInput = document.querySelector('input[type="file"]');
if (photoInput) {
    photoInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.querySelector('.profile-photo img') || 
                              document.querySelector('.no-photo');
                if (preview) {
                    if (preview.classList.contains('no-photo')) {
                        preview.innerHTML = `<img src="${e.target.result}" class="rounded-circle" style="width: 150px; height: 150px; object-fit: cover;">`;
                    } else {
                        preview.src = e.target.result;
                    }
                }
            };
            reader.readAsDataURL(file);
        }
    });
}

// Управление боковым меню
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebarClose = document.getElementById('sidebar-close');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    const overlay = document.querySelector('.sidebar-overlay');

    function openSidebar() {
        sidebar.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeSidebar() {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', openSidebar);
    }

    if (sidebarClose) {
        sidebarClose.addEventListener('click', closeSidebar);
    }

    if (overlay) {
        overlay.addEventListener('click', closeSidebar);
    }

    // Закрытие меню при клике на ссылку
    const sidebarLinks = sidebar.querySelectorAll('.nav-link');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', closeSidebar);
    });

    // Закрытие меню при изменении размера окна
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            closeSidebar();
        }
    });

    // Анимация появления элементов при прокрутке
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-on-scroll');
        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementBottom = element.getBoundingClientRect().bottom;
            
            if (elementTop < window.innerHeight && elementBottom > 0) {
                element.classList.add('visible');
            }
        });
    };

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Запускаем анимацию при загрузке страницы

    // Плавная прокрутка к секциям
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Анимация при наведении на карточки
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Анимация кнопок
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Анимация социальных иконок
    const socialIcons = document.querySelectorAll('.social-links a');
    socialIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.2)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
});

// Инициализация карты на главной странице
function initMap() {
    const mapElement = document.getElementById('salon-map');
    if (mapElement) {
        // Координаты салона (замените на реальные)
        const salonLocation = { lat: 55.7558, lng: 37.6173 };

        const map = new google.maps.Map(mapElement, {
            center: salonLocation,
            zoom: 15,
            styles: [
                {
                    "featureType": "all",
                    "elementType": "geometry",
                    "stylers": [{"color": "#f5f5f5"}]
                },
                {
                    "featureType": "all",
                    "elementType": "labels.text.fill",
                    "stylers": [{"color": "#616161"}]
                },
                {
                    "featureType": "all",
                    "elementType": "labels.text.stroke",
                    "stylers": [{"color": "#f5f5f5"}]
                },
                {
                    "featureType": "administrative.land_parcel",
                    "elementType": "labels.text.fill",
                    "stylers": [{"color": "#bdbdbd"}]
                },
                {
                    "featureType": "poi",
                    "elementType": "geometry",
                    "stylers": [{"color": "#eeeeee"}]
                },
                {
                    "featureType": "poi",
                    "elementType": "labels.text.fill",
                    "stylers": [{"color": "#757575"}]
                },
                {
                    "featureType": "poi.park",
                    "elementType": "geometry",
                    "stylers": [{"color": "#e5e5e5"}]
                },
                {
                    "featureType": "poi.park",
                    "elementType": "labels.text.fill",
                    "stylers": [{"color": "#9e9e9e"}]
                },
                {
                    "featureType": "road",
                    "elementType": "geometry",
                    "stylers": [{"color": "#ffffff"}]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "labels.text.fill",
                    "stylers": [{"color": "#757575"}]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "geometry",
                    "stylers": [{"color": "#dadada"}]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "labels.text.fill",
                    "stylers": [{"color": "#616161"}]
                },
                {
                    "featureType": "road.local",
                    "elementType": "labels.text.fill",
                    "stylers": [{"color": "#9e9e9e"}]
                },
                {
                    "featureType": "transit.line",
                    "elementType": "geometry",
                    "stylers": [{"color": "#e5e5e5"}]
                },
                {
                    "featureType": "transit.station",
                    "elementType": "geometry",
                    "stylers": [{"color": "#eeeeee"}]
                },
                {
                    "featureType": "water",
                    "elementType": "geometry",
                    "stylers": [{"color": "#c9c9c9"}]
                },
                {
                    "featureType": "water",
                    "elementType": "labels.text.fill",
                    "stylers": [{"color": "#9e9e9e"}]
                }
            ]
        });

        // Маркер салона
        const marker = new google.maps.Marker({
            position: salonLocation,
            map: map,
            title: 'Наш салон красоты',
            icon: {
                url: '/static/images/marker.png',
                scaledSize: new google.maps.Size(40, 40)
            }
        });

        // Информационное окно
        const infoWindow = new google.maps.InfoWindow({
            content: `
                <div class="map-info-window">
                    <h5>Салон красоты</h5>
                    <p>Адрес: ул. Примерная, 123</p>
                    <p>Телефон: +7 (999) 123-45-67</p>
                    <p>Режим работы: 9:00 - 21:00</p>
                </div>
            `
        });

        marker.addListener('click', () => {
            infoWindow.open(map, marker);
        });
    }
} 