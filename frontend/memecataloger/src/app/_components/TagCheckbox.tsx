"use client"

import { useRef } from 'react';

import Tag from '@/interfaces/Tag';


export default function TagCheckbox({
  tag, checked
} : {
  tag: Tag,
  checked: boolean
}) {

  const inputRef = useRef(null);

  function handleCheckboxChange() {};

  function handleLabelClick() {};

  return(
    <div>
      <input
        type='checkbox'
        name={tag.id}
        id={`checkbox-${tag.id}`}
        value={tag.name}
        checked={checked}
        ref={inputRef}
        onChange={() => handleCheckboxChange()}
      />
      <label
        htmlFor={tag.id}
        onClick={handleLabelClick}
      >
        {tag.name}
      </label>
    </div>
  )

};
