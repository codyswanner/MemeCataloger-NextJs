import axios from 'axios';

import Thumbnail from './Thumbnail';
import './ImageList.css';


interface Image {
  source: string,
  id: number
};

export default async function ImageList() {

  axios.defaults.baseURL = 'http://127.0.0.1:8000';
  const response = await axios.get('/api/image/');
  const imageList: Image[] = response.data;

  return (
    <div className='image-grid-container'>
      {imageList.map((image) => 
        <Thumbnail src={image.source} id={image.id} key={image.id}/>
      )}
    </div>
  );  
};
