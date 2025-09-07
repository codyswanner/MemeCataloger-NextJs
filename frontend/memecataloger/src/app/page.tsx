import ImageList from "./ImageList";
import styles from "./page.module.css";


export default function Home() {

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <ImageList/>
      </main>
    </div>
  );
};
