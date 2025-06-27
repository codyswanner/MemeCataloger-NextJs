"use client"

import { use } from 'react';

import Thumbnail from './Thumbnail';
import './ImageList.css';


interface Image {
  source: string,
  id: number
};

export default function ImageList({imagePromise} : {imagePromise: Promise<Image[]>}) {
  const imageList = use(imagePromise);
  
  return (
    <div className='image-grid-container'>
      {imageList.map((image) => 
        <Thumbnail src={image.source} id={image.id} key={image.id}/>
      )}
    </div>
  );  
};
