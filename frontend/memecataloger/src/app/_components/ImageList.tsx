import axios from 'axios';

import Thumbnail from './Thumbnail';
import Image from '@/interfaces/Image';
import '@/app/_styles/ImageList.css';


export default async function ImageList() {

  axios.defaults.baseURL = 'http://backend:8000';
  const response = await axios.get('/api/image/');
  const imageList: Image[] = response.data;

  return (
    <div className='image-grid-container'>
      {imageList.map((image) => 
        <Thumbnail image={image} key={image.id}/>
      )}
    </div>
  );  
};
