"use client"

import { RefObject } from 'react';
import TagCheckbox from './TagCheckbox';
import { Tag } from '../interfaces';
import '../_styles/TagPopper.css';


export default function TagPopper({
  dialogRef, tagsArray
} : {
  dialogRef: RefObject<HTMLDialogElement | null>, tagsArray: Array<Tag>
}) {

  const handleTagPopperSubmit = () => {};

  const handleTagPopperClear = () => {};
  
  return(
      <dialog className='tag-popper' ref={dialogRef}>
        <div className='tag-search'>
        {/* search / text input */}  
        </div>
        
        <div className='tag-checkbox-list'>
          {tagsArray.map((tag) => {
            return(
              <TagCheckbox 
              tag={tag}
              key={tag.id}
              />
            )
          })}
        </div>

        <div className='form-controls'>
          {/* Submit / Clear */}
          <span>
            <button type='button' onClick={() => handleTagPopperSubmit()}>
              Submit
            </button>
          </span>
          <span>
            <button type='button' onClick={() => handleTagPopperClear()}>
              Clear
            </button>
          </span>
          
        </div>

      </dialog>
  )
};
