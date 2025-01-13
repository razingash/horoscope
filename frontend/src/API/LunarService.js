import apiClient from "../utils/constants";

export default class LunarService {
    static async getMoonInfoByTimezone(year, month) { /*now timezone is UTC*/
        const response = await apiClient.get(`/lunar-forecast/${year}/${month}`)
        return response.data
    }
}