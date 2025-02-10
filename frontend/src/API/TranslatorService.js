import axios from "axios";

export default class TranslatorService {
    /*this api will be on Nginx level and contains only json static data in different languages*/
    static async getMoonEventsDescription(language) {
        const response = await axios.get(`http://localhost:80/static/json/moon-events/${language}.json`,
            {headers: {'Content-Type': 'application/json'}})
        return response.data
    }
}