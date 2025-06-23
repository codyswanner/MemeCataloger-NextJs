import Thumbnail from './Thumbnail';
import './ImageList.css';


interface Image {
  source: string,
  id: number
};

export default function ImageList({imageList}: {imageList: Array<Image>}) {
  return (
    <div className='image-grid-container'>
      {imageList.map((image) => 
        <Thumbnail src={image.source} id={image.id} key={image.id}/>
      )}
    </div>
  );  
};
