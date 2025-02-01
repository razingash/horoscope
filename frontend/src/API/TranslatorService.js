import apiClient from "../utils/constants";

/*попробовать позже добавтиь в apiClient язык*/
export default class TranslatorService {
    /*this api will be on Nginx level and contains only json static data in different languages*/
    static async getMoonEventsDescription(language) {
        const response = await apiClient.get(`/locales/moon-events/${language}.json/`)
        return response.data
    }
}