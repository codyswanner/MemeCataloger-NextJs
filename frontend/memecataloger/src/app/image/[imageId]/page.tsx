import { default as NextJsImage } from "next/image";

import "./page.css";


export default async function Home({
  params,
} : {
  params: Promise<{imageId: string}>
}) {
  // params is a NextJS object for storing information from dynamic segments.
  // Learn more about dynamic segments here: https://nextjs.org/docs/app/getting-started/layouts-and-pages#creating-a-dynamic-segment
  const {imageId} = await params  

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
        </div>
      </main>
    </div>
  );
};
