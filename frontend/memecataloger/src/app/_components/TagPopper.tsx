"use client"

import { RefObject } from 'react';
import TagCheckbox from './TagCheckbox';
import Tag from '@/interfaces/Tag';
import '../_styles/TagPopper.css';
import ImageTag from '@/interfaces/ImageTag';
import { UUID } from 'crypto';


export default function TagPopper({
  dialogRef, imageId, tagsArray, imageTagArray
} : {
  dialogRef: RefObject<HTMLDialogElement | null>,
  imageId: UUID,
  tagsArray: Tag[],
  imageTagArray: ImageTag[]
}) {

  const checkTagAssignment = (tagId: UUID) => {

    const matchingImageTags: ImageTag[] = imageTagArray.filter((imageTag) => {
      return imageTag.image == imageId && imageTag.tag == tagId;
    });

    if (matchingImageTags?.length) {
      console.log(`Tag ${tagId} is checked!`);
      return true;
    };

    console.log(`Tag ${tagId} is NOT checked!`);
    return false;
  };

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
              checked={checkTagAssignment(tag.id)}
              />
            )
          })}
        </div>

      </dialog>
  )
};
