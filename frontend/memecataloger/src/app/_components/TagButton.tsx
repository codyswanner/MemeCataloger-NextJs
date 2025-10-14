"use client"

import { useRef } from 'react';

import TagPopper from "./TagPopper"
import Tag from '@/interfaces/Tag';
import '@/app/_styles/TagButton.css';
import ImageTag from '@/interfaces/ImageTag';
import { UUID } from 'crypto';


export default function TagButton({
  imageId, tagsArray, imageTagArray
} : {
  imageId: UUID,
  tagsArray: Tag[],
  imageTagArray: ImageTag[]
}) {

  const tagPopperRef = useRef <HTMLDialogElement> (null);
  const handleClick = () => {
    if (tagPopperRef.current === null) {
      return
    } else if (!tagPopperRef.current.open) {
      const tagPopper: HTMLDialogElement = tagPopperRef.current!;
      tagPopper.show();
    } else if (tagPopperRef.current.open) {
      const tagPopper: HTMLDialogElement = tagPopperRef.current!;
      tagPopper.close();
    }
    
  };

  return(
    <div className="tag-editor-container">
      <TagPopper 
        dialogRef={tagPopperRef}
        imageId={imageId}
        tagsArray={tagsArray}
        imageTagArray={imageTagArray}
      />
      <button
        className="tag-button"
        type="button"
        onClick={() => handleClick()}
      >
        Tags
      </button>
    </div>
  )
};
