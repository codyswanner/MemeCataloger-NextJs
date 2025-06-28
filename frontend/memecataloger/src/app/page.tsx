import { Suspense } from "react";

import ImageList from "./ImageList";
import styles from "./page.module.css";


export default async function Home() {

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <Suspense fallback={<div>Loading...</div>}>
          <ImageList/>
        </Suspense>
      </main>
    </div>
  );
};
