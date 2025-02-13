import apiClient from "../utils/constants";

export default class HoroscopeService {
    static async getDailyHoroscope(date, language) {
        const response = await apiClient.get("horoscope/daily/", {params: {language: language, date: date}})
        return response.data
    }
    static async getWeeklyHoroscope(date, language) {
        const response = await apiClient.get("horoscope/weekly/", {params: {language: language, date: date}})
        return response.data
    }
    static async getMonthlyHoroscope(date, language) {
        const response = await apiClient.get("horoscope/monthly/", {params: {language: language, date: date}})
        return response.data
    }
    static async getAnnualHoroscope(date, language) {
        const response = await apiClient.get("horoscope/annual/", {params: {language: language, date: date}})
        return response.data
    }
}
