import axios from "axios";


export default async function getImageList() {
    axios.defaults.baseURL = 'http://backend:8000';
    const response = await axios.get('/api/image/');
    const imageList = response.data;

    return imageList;
};
