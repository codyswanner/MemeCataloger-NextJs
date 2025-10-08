import { default as NextJsImage } from "next/image";

import Image from "@/interfaces/Image";
import '@/app/_styles/Thumbnail.css';


export default function Thumbnail({image} : {image: Image}){

  const videoFileTypesRegex: RegExp = /.+\.(mp4|mov|avi|mkv|wmv|flv|webm)/i;
  const imageFileTypesRegex: RegExp = /.+\.(jpg|jpeg|png|webp|gif|bmp|svg)/i;

  if (videoFileTypesRegex.test(image.source)) {
    return(
      <div className="thumbnail-container" data-testid="video-thumbnail">
        <video className='thumbnail-img' src={`${image.source}#0`}/>
      </div>
    );
  } else if (imageFileTypesRegex.test(image.source)) {
    return(
      <div className="thumbnail-container" data-testid="image-thumbnail">
        {/* a tag points to a URL to be set up later.
          * Also should use next/headers (async) to get host,
          * rather than hard-coded 127.0.0.1; pending E2E testing setup.
          * See https://nextjs.org/docs/app/guides/testing/jest */}
        <a href={"http://127.0.0.1:3000/image/" + image.id}>
          <NextJsImage
            className="thumbnail-img"
            src={image.source}
            alt=""
            width={1000}
            height={1000}
          />
        </a>
      </div>
    );
  } else {
    console.error(`Source ${image.source} does not match expected file types`);
  };
};
