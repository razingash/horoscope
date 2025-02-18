import axios from "axios";
import {baseURL} from "../utils/constants";

export default class TranslatorService {
    /*this api will be on Nginx level and contains only json static data in different languages*/
    static async getMoonEventsDescription(language) {
        const response = await axios.get(`${baseURL}/static/json/moon-events/${language}.json`,
            {headers: {'Content-Type': 'application/json'}})
        return response.data
    }
}