import styles from '../_styles/Header.module.css';


export default function Header() {

  return(
    <div className={styles.headerOuterDiv}>
      <div className={styles.headerInnerDiv}>
        <h2 className={styles.headerTitle}>MemeCataloger</h2>
      </div>
    </div>
  );
};
