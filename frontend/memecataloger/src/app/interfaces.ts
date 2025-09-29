import { UUID } from 'crypto';


export interface Image {
  id: UUID,
  source: string,
  description: string
};

export interface Tag {
  id: UUID,
  name: string
}

export interface ImageTag {
  id: UUID,
  image: UUID,
  tag: UUID
}
