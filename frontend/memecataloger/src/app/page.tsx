import { Suspense } from "react";

import ImageList from "./ImageList";
import styles from "./page.module.css";
import getImageList from "./getImageList";


export default async function Home() {
  const imageList = getImageList();

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <Suspense fallback={<div>Loading...</div>}>
          <ImageList imagePromise={imageList}/>
        </Suspense>
      </main>
    </div>
  );
};
