import ImageList from "./ImageList";
import Thumbnail from "./Thumbnail";
import styles from "./page.module.css";

interface Image {
  source: string,
  id: number
};

export default function Home() {
  const imageList: Array<Image> = [
    {
      source: "/20201109_113624.jpg",
      id: 1
    },
    {
      source: "/51c17b6e602aa2cb540a73af1c40c493.mp4",
      id: 2
    },
    {
      source: "/537c24c406ac264d4a9c027e18f39c24.png",
      id: 3
    },
    {
      source: "/1000026073.jpg",
      id: 4
    },
    {
      source: "/1000026100.jpg",
      id: 5
    },
    {
      source: "/1000026763.png",
      id: 6
    },
    {
      source: "/1000027177.png",
      id: 7
    },
    {
      source: "/1000027195.jpg",
      id: 8
    },
    {
      source: "/finish a creative project you filthy casual.jpeg",
      id: 9
    },
    {
      source: "/millionaires.png",
      id: 10
    }
  ];
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <ImageList imageList={imageList} />
        {/* <Thumbnail src="/20201109_113624.jpg" id={1}/> */}
      </main>
    </div>
  );
};
