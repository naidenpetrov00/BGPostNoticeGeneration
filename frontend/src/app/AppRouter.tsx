import { QueryClient, useQueryClient } from "@tanstack/react-query";
import { RouterProvider, createBrowserRouter } from "react-router-dom";

import { AppRootErrorBoundary } from "./pages/errors/AppRootErrorBoundary";
import { useMemo } from "react";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const convert = (queryClient: QueryClient) => (m: any) => {
  const { clientLoader, clientAction, default: Component, ...rest } = m;
  return {
    ...rest,
    loader: clientLoader?.(queryClient),
    action: clientAction?.(queryClient),
    Component,
  };
};

const createAppRouter = (queryClient: QueryClient) =>
  createBrowserRouter([
    {
      path: "/",
      lazy: async () => await import("./AppRoot").then(convert(queryClient)),
      ErrorBoundary: AppRootErrorBoundary,
      children: [
        {
          index: true,
          lazy: async () =>
            import("./pages/HomePage/HomePage").then(convert(queryClient)),
          ErrorBoundary: AppRootErrorBoundary,
        },
      ],
    },
    {
      path: "*",
      lazy: async () =>
        import("./pages/errors/NotFoundPage").then(convert(queryClient)),
      ErrorBoundary: AppRootErrorBoundary,
    },
  ]);

export const AppRouter = () => {
  const queryClient = useQueryClient();
  const router = useMemo(() => createAppRouter(queryClient), [queryClient]);

  return <RouterProvider router={router} />;
};
