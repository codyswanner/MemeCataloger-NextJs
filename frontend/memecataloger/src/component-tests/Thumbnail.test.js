import { render, screen } from '@testing-library/react';

import Thumbnail from '../app/_components/Thumbnail';


describe('Thumbnail', () => {
  let testImage;
  let testVideo;
  let testUnsupportedType;
  beforeAll(() => {
    testImage = {
      id: '44fc80c3-8751-43ae-abea-f8b83c551024',
      source: '/test-image.jpg',
      description: 'this is the test image description'
    };
    testVideo = {
      id: '95a4e36f-c280-4121-afa4-fe2650c9a9fc',
      source: '/test-image.mp4',
      description: 'this is the test video description'
    };
    testUnsupportedType = {
      id: '3eebef6e-a471-4fc6-8bc0-1385d6a2f40f',
      source: '/cow.moo',
      description: "it a cow farm... there's gonna be cows outside"
    };
  });

  test('renders ImageThumbnail for images', () => {
    render(
      <Thumbnail image={testImage} />
    );

    expect(screen.getByRole('presentation')).toBeInTheDocument();
  });

  test('renders VideoThumbnail for videos', () => {
    render(
      <Thumbnail image={testVideo} />
    );

    expect(screen.getByTestId('video-thumbnail')).toBeInTheDocument();  
  });

  test('renders error for unknown filetype', () => {
    const errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    try {
      render(
        <Thumbnail image={testUnsupportedType} />
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
