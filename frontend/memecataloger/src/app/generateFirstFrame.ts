
export default async function generateFirstFrame(source: string) {
  let firstFrame: string;

  const video = document.createElement('video');
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');

  video.src = source;
  video.preload = 'metadata';

  await new Promise(resolve => video.addEventListener(
    'loadedmetadata', resolve
  ));

  video.currentTime = 0;

  await new Promise(resolve => video.addEventListener(
    'seeked', resolve
  ));

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context!.drawImage(video, 0, 0, canvas.width, canvas.height);

  firstFrame = canvas.toDataURL('image/jpeg');

  return firstFrame;
};
