import axios from "axios";

/*попробовать позже добавтиь в apiClient язык*/
export default class TranslatorService {
    /*this api will be on Nginx level and contains only json static data in different languages*/
    static async getMoonEventsDescription(language) {
        const response = await axios.get(`http://localhost:80/static/js/moon-events/${language}.json`,
            {headers: {'Content-Type': 'application/json'}})
        return response.data
    }
}