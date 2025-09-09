import { render, screen } from "@testing-library/react";

import Header from "../app/header";


describe("Page-Header", () => {
  
  test("header title is visible", () => {
    render(
        <Header />
    );

    expect(screen.getByText("MemeCataloger")).toBeInTheDocument();
  });
});
