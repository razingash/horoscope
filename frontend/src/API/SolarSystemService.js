import apiClient from "../utils/constants";

export default class SolarSystemService {
    static async getSolarSystemForecast() {
        const response = await apiClient('solar-system/map/')
        return response.data
    }
}