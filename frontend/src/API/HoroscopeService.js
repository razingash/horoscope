import apiClient from "../utils/constants";

export default class HoroscopeService {
    static async getDailyHoroscope(date, language) {
        const response = await apiClient.get("horoscope/daily/", {params: {date: date, language: language}})
        return response.data
    }
    static async getWeeklyHoroscope(date, language) {
        const response = await apiClient.get("horoscope/weekly/", {params: {date: date, language: language}})
        return response.data
    }
    static async getMonthlyHoroscope(date, language) {
        const response = await apiClient.get("horoscope/monthly/", {params: {date: date, language: language}})
        return response.data
    }
    static async getAnnualHoroscope(date, language) {
        const response = await apiClient.get("horoscope/annual/", {params: {date: date, language: language}})
        return response.data
    }
}
