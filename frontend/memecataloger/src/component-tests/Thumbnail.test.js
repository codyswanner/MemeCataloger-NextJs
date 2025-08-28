import { render, screen } from '@testing-library/react';

import Thumbnail from '../app/Thumbnail';


describe('Thumbnail', () => {

  test('renders ImageThumbnail for images', () => {
    render(
      <Thumbnail src={'/test-image.jpg'} id={1} />
    );

    expect(screen.getByRole('presentation')).toBeInTheDocument();
  });

  test('renders VideoThumbnail for videos', () => {
    render(
      <Thumbnail src={'/test-video.mp4'} id={1} />
    );

    expect(screen.getByTestId('video-thumbnail')).toBeInTheDocument();  
  });

  test('renders error for unknown filetype', () => {
    const errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    try {
      render(
        <Thumbnail src={'/cow.moo'} id={1} />
      );
    } catch {
      // error expected; do nothing, confirm in asserts
    };

    expect(errorSpy).toHaveBeenCalledTimes(1);
    expect(errorSpy).toHaveBeenCalledWith(
      'Source /cow.moo does not match expected file types'
    );

    errorSpy.mockRestore();
  });
});
