import axios from "axios";
import { default as NextJsImage } from "next/image";

import "./page.css";
import Tag from "@/interfaces/Tag";
import TagButton from "@/app/_components/TagButton";
import ImageTag from "@/interfaces/ImageTag";
import { UUID } from "crypto";


export default async function Home({
  params,
} : {
  params: Promise<{imageId: UUID}>
}) {
  // params is a NextJS object for storing information from dynamic segments.
  // Learn more about dynamic segments here: https://nextjs.org/docs/app/getting-started/layouts-and-pages#creating-a-dynamic-segment
  const {imageId} = await params

  axios.defaults.baseURL = 'http://backend:8000';
  const tagResponse = await axios.get('/api/tag/');
  const tagsArray: Tag[] = tagResponse.data;
  const imageTagResponse = await axios.get('/api/image-tag/');
  const imageTagArray: ImageTag[] = imageTagResponse.data;


  return (
    <div>
      <main>
        {/* Stuff goes here, like:
          * the actual image
          * Options for editing tags, description, etc
          * 
          * But a lot of that will come later, for now
          * let's just get an image displaying.
          */}
        <div className="image-container">
          <NextJsImage
            className="image-display"
            src={"http://backend:8000/api/image/" + imageId}
            alt=""
            width={4000}
            height={4000}
          />
          <div className="footer">
            <TagButton
              imageId={imageId}
              tagsArray={tagsArray}
              imageTagArray={imageTagArray}
            />
          </div>
        </div>
      </main>
    </div>
  );
};
