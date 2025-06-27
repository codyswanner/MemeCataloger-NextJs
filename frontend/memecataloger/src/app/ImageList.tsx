"use client"

import { use } from 'react';

import Thumbnail from './Thumbnail';
import './ImageList.css';
import getImageList from './getImageList';


interface Image {
  source: string,
  id: number
};

export default function ImageList() {
  const imageList: Image[] = use(getImageList());
  
  return (
    <div className='image-grid-container'>
      {imageList.map((image) => 
        <Thumbnail src={image.source} id={image.id} key={image.id}/>
      )}
    </div>
  );  
};
