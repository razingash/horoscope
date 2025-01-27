import apiClient from "../utils/constants";

export default class LunarService {
    static async getMoonInfoByTimezone(year) { /*now timezone is UTC*/
        const response = await apiClient.get(`/moon/lunar-forecast/${year}/`)
        return response.data
    }
}