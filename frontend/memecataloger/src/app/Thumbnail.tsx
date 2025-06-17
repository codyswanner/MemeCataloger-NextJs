import { default as NextJsImage } from "next/image";
import { headers } from 'next/headers';

import './thumbnail.css';


export default async function Thumbnail({src, id} : {src: string, id: number}){

  const videoFileTypesRegex: RegExp = /.+\.(mp4|mov|avi|mkv|wmv|flv|webm)/i;
  const imageFileTypesRegex: RegExp = /.+\.(jpg|jpeg|png|webp|gif|bmp|svg)/i;

  if (videoFileTypesRegex.test(src)) {
    return(
      <div className="thumbnail-container" data-testid="video-thumbnail">
        <video className='thumbnail-img' src={`${src}#0`}/>
      </div>
    );
  } else if (imageFileTypesRegex.test(src)) {
    return(
      <div className="thumbnail-container" data-testid="image-thumbnail">
        <a href={"http://" + (await headers()).get('host') + "/image/" + id}>
          <NextJsImage
            className="thumbnail-img"
            src={src}
            alt=""
            width={1000}
            height={1000}
          />
        </a>
      </div>
    );
  } else {
    console.error(`Source ${src} does not match expected file types`);
  };
};
