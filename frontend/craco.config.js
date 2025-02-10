const HtmlWebpackPlugin = require("html-webpack-plugin");

const routesConfig = [
    {
        path: "/",
        key: "main",
        languages: [
            {
                lang: "en",
                title: "Main - English",
                description: "Main page in English",
            },
            {
                lang: "ru",
                title: "Главная - Русский",
                description: "Главная страница на русском",
            },
            {
                lang: "pl",
                title: "132 - 132",
                description: "132",
            },
        ]
    },
    {
        path: "/horoscope/daily/",
        key: "horoscope-daily",
        languages: [
            {
                lang: "en",
                title: "Horoscope - daily",
                description: "daily",
            },
            {
                lang: "ru",
                title: "Ежедневный",
                description: "ежедневный",
            },
            {
                lang: "pl",
                title: "132 - 132",
                description: "132",
            },
        ]
    },
    {
        path: "/horoscope/weekly/",
        key: "horoscope-weekly",
        languages: [
            {
                lang: "en",
                title: "Horoscope - weekly",
                description: "weekly",
            },
            {
                lang: "ru",
                title: "еженедельный",
                description: "Главная страница на русском",
            },
            {
                lang: "pl",
                title: "132 - 132",
                description: "132",
            },
        ]
    },
    {
        path: "/horoscope/monthly/",
        key: "horoscope-monthly",
        languages: [
            {
                lang: "en",
                title: "Horoscope - montly",
                description: "monthly",
            },
            {
                lang: "ru",
                title: "Ежемесячный гороскоп",
                description: "Главная страница на русском",
            },
            {
                lang: "pl",
                title: "132 - 132",
                description: "132",
            },
        ]
    },
    {
        path: "/horoscope/annual/",
        key: "horoscope-annual",
        languages: [
            {
                lang: "en",
                title: "Horoscope - annual",
                description: "Horoscope - annual",
            },
            {
                lang: "ru",
                title: "Ежегодный гороскоп",
                description: "Главная страница на русском",
            },
            {
                lang: "pl",
                title: "132 - 132",
                description: "132",
            },
        ]
    },
    {
        path: "/moon/calendar/",
        key: "moon-calendar",
        languages: [
            {
                lang: "en",
                title: "Moon Calendar",
                description: "Moon Calendar",
            },
            {
                lang: "ru",
                title: "Лунный календарь",
                description: "Лунный календарь",
            },
            {
                lang: "pl",
                title: "132 - 132",
                description: "132",
            },
        ]
    },
    {
        path: "/moon-events/",
        key: "moon-events",
        languages: [
            {
                lang: "en",
                title: "Moon Events",
                description: "Moon events",
            },
            {
                lang: "ru",
                title: "Лунные ...",
                description: "Лунные ...",
            },
            {
                lang: "pl",
                title: "132 - 132",
                description: "132",
            },
        ]
    },
    {
        path: "/solar-system/",
        key: "solar-system-bydate",
        languages: [
            {
                lang: "en",
                title: "The Planets Today",
                description: "The Planets Today",
            },
            {
                lang: "ru",
                title: "Планеты Сегодня",
                description: "Планеты Сегодня",
            },
            {
                lang: "pl",
                title: "132 - 132",
                description: "132",
            },
        ]
    },
]

const isProduction = process.env.IS_PROD ? process.env.IS_PROD === "true" : false;

module.exports = {
    webpack: {
        configure: (webpackConfig) => {
            webpackConfig.plugins = webpackConfig.plugins.filter(
                plugin => !(plugin instanceof HtmlWebpackPlugin)
            );

            if (isProduction) {
                const htmlPlugins = routesConfig.flatMap(route =>
                    route.languages.map(langConfig => new HtmlWebpackPlugin({
                        filename: `${langConfig.lang}${route.path === "/" ? "/index.html" : `${route.path}/index.html`}`,
                        template: './public/index.html',
                        templateParameters: {
                            title: langConfig.title,
                            description: langConfig.description,
                            language: langConfig.lang,
                            canonicalLink: `https://localhost${langConfig.lang === "en" ? route.path : `/${langConfig.lang}${route.path}`}`,
                            alternateLinks: route.languages.map(l => ({
                                hreflang: l.lang,
                                href: `https://localhost/${l.lang}${route.path}`
                            }))
                        },
                        inject: true,
                    }))
                );

                webpackConfig.plugins.push(...htmlPlugins);
            } else { // npm start
                webpackConfig.plugins.push(
                    new HtmlWebpackPlugin({
                        filename: 'index.html',
                        template: './public/index.html',
                        templateParameters: {
                            title: "defaultTitle",
                            description: "defaultDescription",
                            language: "en",
                            canonicalLink: `https://localhost/en/`,
                            alternateLinks: [{
                                hreflang: "en",
                                href: `https://localhost/en/`,
                            }],
                        },
                        inject: true,
                    })
                );
            }

            return webpackConfig;
        },
    },
};
