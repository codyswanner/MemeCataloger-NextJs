import ImageList from "./ImageList";
import styles from "./page.module.css";


export default function Home() {

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <ImageList/>
        {/* <Thumbnail src="/20201109_113624.jpg" id={1}/> */}
      </main>
    </div>
  );
};
