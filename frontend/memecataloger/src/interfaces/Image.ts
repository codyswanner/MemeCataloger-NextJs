import { UUID } from 'crypto';


export default interface Image {
  id: UUID,
  source: string,
  description: string
};
