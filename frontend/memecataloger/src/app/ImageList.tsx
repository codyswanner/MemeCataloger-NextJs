import Thumbnail from './Thumbnail';
import './ImageList.css';


interface Image {
  source: string,
  id: number
};

export default async function ImageList() {

  const response = await fetch('http://backend:8000/api/image/');
  const imageList: Image[] = await response.json();

  return (
    <div className='image-grid-container'>
      {imageList.map((image) => 
        <Thumbnail src={image.source} id={image.id} key={image.id}/>
      )}
    </div>
  );  
};
