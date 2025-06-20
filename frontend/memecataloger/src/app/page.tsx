import axios from 'axios';

import ImageList from "./ImageList";
import styles from "./page.module.css";


interface Image {
  source: string,
  id: number
};

export default async function Home() {

  axios.defaults.baseURL = 'http://backend:8000';
  const response = await axios.get('/api/image');
  const imageList: Array<Image> = response.data;

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <ImageList imageList={imageList} />
      </main>
    </div>
  );
};
