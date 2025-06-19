import "bootstrap/dist/css/bootstrap.min.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./main.css";
import HomePage from "./pages/HomePage.tsx";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import NotFoundPage from "./pages/not-found-page/NotFoundPage.tsx";
import SearchPage from "./pages/not-found-page/search-page/SearchPage.tsx";

const queryClient = new QueryClient();

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
    errorElement: <NotFoundPage />,
  },
  {
    path: "/search/:itemName",
    element: <SearchPage />,
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>
);
