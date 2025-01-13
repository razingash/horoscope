import apiClient from "../utils/constants";

export default class HoroscopeService {
    static async getDailyHoroscope(date) {
        const response = await apiClient.get("horoscope/daily/")
        return response.data
    }
    static async getWeeklyHoroscope() {
        const response = await apiClient.get("horoscope/weekly/")
        return response.data
    }
    static async getMonthlyHoroscope() {
        const response = await apiClient.get("horoscope/monthly/")
        return response.data
    }
    static async getAnnualHoroscope() {
        const response = await apiClient.get("horoscope/annual/")
        return response.data
    }
}
