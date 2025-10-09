"use client"

import { useRef } from 'react';

import TagPopper from "./TagPopper"
import { Tag } from '../interfaces';
import '@/app/_styles/TagButton.css';


export default function TagButton({tagsArray} : {tagsArray: Array<Tag>}) {

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
    
  }

  return(
    <div className="tag-editor-container">
      <TagPopper 
        dialogRef={tagPopperRef}
        tagsArray={tagsArray}
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
