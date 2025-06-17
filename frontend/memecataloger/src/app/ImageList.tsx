import Thumbnail from './Thumbnail';
import './ImageList.css';


interface Image {
  source: string,
  id: number
};

export default function ImageList({imageList}: {imageList: Array<Image>}) {
  console.log(imageList);

  imageList.map((image) => console.log(image.source));

  return (
    <div className='image-grid-container'>
      {imageList.map((image) => 
        <Thumbnail src={image.source} id={image.id} key={image.id}/>
      )}
    </div>
  );  
};
