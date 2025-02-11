export function register() {
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            const swUrl = "/service-worker.js";
            navigator.serviceWorker
                .register(swUrl)
                .then((registration) => {
                    console.log('Сервис-воркер зарегистрирован: ', registration);

                    registration.onupdatefound = () => {
                        const installingWorker = registration.installing;
                        installingWorker.onstatechange = () => {
                            if (installingWorker.state === 'installed') {
                                if (navigator.serviceWorker.controller) {
                                    console.log('Новое содержимое доступно; обновите страницу.');
                                } else {
                                    console.log('Содержимое кэшировано для оффлайн-режима.');
                                }
                            }
                        };
                    };
                })
                .catch((error) => {
                    console.error('Ошибка при регистрации сервис-воркера: ', error);
                });
        });
    }
}


export function unregister() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.ready.then((registration) => {
            registration.unregister();
        });
    }
}
