import { test, expect } from '@playwright/test';


test('has title', async ({ page }) => {
  await page.goto('http://127.0.0.1:3000');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/MemeCataloger/);
});

test('four thumbnails visible', async ({ page }) => {
  await page.goto('http://127.0.0.1:3000');

  await expect(page.getByRole('link')).toHaveCount(4);

});






//   test('renders ImageThumbnail for images', async ({ page }) => {

//     expect(page.getByRole('presentation')).toBe;
//   });

//   test('renders VideoThumbnail for videos', () => {
//     render(
//       <Thumbnail src={'/test-video.mp4'} id={1} />
//     );

//     expect(screen.getByTestId('video-thumbnail')).toBeInTheDocument();  
//   });

//   test('renders error for unknown filetype', () => {
//     const errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

//     try {
//       render(
//         <Thumbnail src={'/cow.moo'} id={1} />
//       );
//     } catch {
//       // error expected; do nothing, confirm in asserts
//     };

//     expect(errorSpy).toHaveBeenCalledTimes(1);
//     expect(errorSpy).toHaveBeenCalledWith(
//       'Source /cow.moo does not match expected file types'
//     );

//     errorSpy.mockRestore();
//   });
